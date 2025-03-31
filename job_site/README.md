
# Job site Scraper

## Overview
Scrapes website: [WorkingNomads.com](https://www.workingnomads.com/jobs)

Target data example - Job listings scraped from the website:

![Job Scraping Overview](job_scraping.png)

This project scrapes job listings from **WorkingNomads.com**, a site dedicated to remote job opportunities. It extracts key data such as job titles, company names, job locations, work types, job links, and tags. The extracted data is structured and ready for further analysis or storage.

### Tools & Technologies Used

- **Python**: The primary programming language for the scraper.
- **Scrapy**: A powerful web scraping framework for extracting data from websites.
- **Playwright**: For headless browser interaction, used in dynamic content scraping.
- **Item Loaders**: For processing and cleaning the scraped data.
- **SQLite** (Optional): For storing the scraped data in a local database.
- **CSV**: For exporting scraped data into CSV files for easy analysis.

## Usage

### Scraper (`get_jobs.py`)

The main scraper interacts with the **Working Nomads** website and extracts job listings data. The scraper uses **Playwright** for headless browser interaction to handle dynamic content.

- The number of job listings to scrape is set by the user in the `n_listings` parameter (default is 200).

### Run the script:

First, configure the script as needed, then run the following:

```bash
python get_jobs.py
```

The scraper will collect job listings, process them using item loaders, and output the data in CSV format or save it to a database (optional).

### Example usage in Python:

```python
from get_jobs import GetJobsSpider
# Define the number of listings to scrape
spider = GetJobsSpider(n_listings=100)
```

## Output

The scraped job listings are stored in:

```
working_nomads_jobs.csv
```

Or, if you choose to store data in a database, the data will be saved in an SQLite database (default filename: `jobs.db`).
