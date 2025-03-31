from itemadapter import ItemAdapter
import sqlite3
import csv
import json


class JobSitePipeline:
    def process_item(self, item, spider):
        return item


# Pipeline to save scraped data to an SQLite database
class SaveToDatabasePipeline:
    def __init__(self):
        self.con = sqlite3.connect("jobs.db")  # Connect to SQLite database
        self.cur = self.con.cursor()  # Create a cursor object for executing SQL queries

    def open_spider(self, spider):
        """Creates the database table when the spider starts running."""
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS job_listings (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                job_name TEXT,
                job_link TEXT UNIQUE,  -- Ensure unique job links to prevent duplicates
                company_name TEXT,
                job_location TEXT,
                work_type TEXT,
                salary TEXT,
                tags TEXT  -- Tags will be stored as a comma-separated string
            )
            """
        )
        self.con.commit()

    def process_item(self, item, spider):
        """Processes each extracted job item and saves it to the database."""
        tags_str = ", ".join(item.get("tags", []))  # Convert tags list to a string

        try:
            self.cur.execute(
                """
                INSERT INTO job_listings 
                (job_name, job_link, company_name, job_location, work_type, salary, tags) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    item.get("job_name", ""),
                    item.get("job_link", ""),
                    item.get("company_name", ""),
                    item.get("job_location", ""),
                    item.get("work_type", ""),
                    item.get("salary", ""),
                    tags_str
                )
            )
            self.con.commit()
        except sqlite3.IntegrityError:
            spider.logger.info(f"Duplicate job found: {item.get('job_link')} - Skipping.")

        return item

    def close_spider(self, spider):
        """Closes the database connection when the spider finishes."""
        self.con.close()


class CsvExportPipeline:
    def __init__(self):
        self.file_name = "jobs.csv"
        self.file = None
        self.writer = None
        self.header_written = False

    def open_spider(self, spider):
        """Open the CSV file and prepare the CSV writer."""
        self.file = open(self.file_name, mode='a', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)

    def process_item(self, item, spider):
        """Process each item and write it to the CSV file."""
        # Ensure all required fields, including 'salary', are present
        job_data = {
            "job_name": item.get("job_name", ""),
            "job_link": item.get("job_link", ""),
            "company_name": item.get("company_name", ""),
            "job_location": item.get("job_location", ""),
            "work_type": item.get("work_type", ""),
            "salary": item.get("salary", ""),  # Ensure salary is included
            "tags": ", ".join(item.get("tags", []))  # Join tags into a single string
        }

        # Write the header if it's the first item
        if not self.header_written:
            header = job_data.keys()  # Use the keys from job_data as the header row
            self.writer.writerow(header)
            self.header_written = True

        # Write the job data to the CSV
        self.writer.writerow(job_data.values())

        return item

    def close_spider(self, spider):
        """Close the CSV file when the spider finishes."""
        if self.file:
            self.file.close()


class JsonExportPipeline:
    def __init__(self):
        self.file_name = "jobs.json"
        self.file = None

    def open_spider(self, spider):
        """Open the JSON file and prepare to write data."""
        self.file = open(self.file_name, mode='w', encoding='utf-8')
        self.file.write('[')  # Start the JSON array

    def process_item(self, item, spider):
        """Process each item and write it to the JSON file."""
        # Convert item to a dictionary
        item_dict = dict(item)

        # Convert tags list to a comma-separated string if it's a list
        if "tags" in item_dict:
            item_dict["tags"] = ", ".join(item_dict["tags"])

        # Write item data to the JSON file
        json.dump(item_dict, self.file, ensure_ascii=False, separators=(',', ':'))

        # Add a comma if it's not the last item
        self.file.write(',\n')

        return item

    def close_spider(self, spider):
        """Close the JSON file when the spider finishes."""
        self.file.write(']')  # End the JSON array
        self.file.close()