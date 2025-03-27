from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import sqlite3


# Pipeline to validate and process GDP data
class CountriesGdpPipeline:
    def process_item(self, item, spider):
        gdp_value = item.get('gdp')  # Use .get() to avoid KeyError

        # Check if GDP value is missing or not a float, then drop the item
        if gdp_value is None or not isinstance(gdp_value, float):
            raise DropItem(f"Missing or invalid GDP value: {gdp_value}. Item excluded.")

        return item  # Return the item if valid


# Pipeline to remove duplicate country entries
class RemoveDuplicatesPipeline:
    def __init__(self):
        self.countries_seen = set()  # Set to track already processed country names

    def process_item(self, item, spider):
        for country in item['country_name']:  # Iterate over country names (if multiple)
            # Check if the country is already in the set
            if item['country_name'] in self.countries_seen:
                raise DropItem(f"Removing Duplicates: {item}. Item excluded.")

            else:
                self.countries_seen.add(item['country_name'])  # Add country to set
                return item  # Return the item if unique


# Pipeline to save scraped data to an SQLite database
class SaveToDatabasePipeline:
    def __init__(self):
        self.con = sqlite3.connect("countries_gdp.db")  # Connect to SQLite database
        self.cur = self.con.cursor()  # Create a cursor object for executing SQL queries

    def open_spider(self, spider):
        # Create the database table if it doesn't exist
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS countries_gdp
            (country_name TEXT PRIMARY KEY,  -- Primary key to avoid duplicates
            gdp REAL,  -- GDP value stored as a floating-point number
            year INTEGER)  -- Year stored as an integer
            """
        )
        self.con.commit()  # Commit the changes

    def process_item(self, item, spider):
        # Insert the scraped data into the database
        self.con.execute(""" INSERT INTO countries_gdp (country_name, year, gdp) VALUES(?, ?, ?) """,
                         (item["country_name"], item["year"], item["gdp"]))

        self.con.commit()  # Commit after inserting each item

    def close_spider(self, spider):
        self.con.close()  # Close the database connection when the spider finishes
