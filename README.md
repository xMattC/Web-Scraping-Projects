
# Web Scraping projects

This repository contains various web scraping projects for different websites. Each project is contained within its own
folder, and you can find specific documentation (README.md) and relevant files for each scraper inside the respective
folders.

The goal of this project is to provide reusable scraping solutions for common use cases and to demonstrate web scraping techniques.


## Tools & Technologies

This project uses the following tools and technologies:

- **Python**: The primary programming language used for writing the web scraping scripts.
- **Scrapy**: For handling web scraping tasks.
- **Playwright**: For scraping websites with dynamic content (JavaScript rendering).
- **BeautifulSoup**: A library for parsing HTML and XML documents, used to extract data from web pages.
- **requests**: A library to send HTTP requests and retrieve data from websites.
- **Selectolax**: A fast HTML parser.
- **HTTPX**: A library for making HTTP requests.
- **SQLite**: A lightweight, serverless, self-contained SQL database engine.
- **pandas**: A data manipulation library to structure and save scraped data into CSV format.

## Installation & Setup

Follow these steps to get the project up and running.

```bash
# Download repo
git clone https://github.com/xMattC/web-scraping-scripts.git

# Move to dir
cd web-scraping-scripts

# Create the virtual environment:
python -m venv .env

# Activate the virtual environment:
.\\.env\\Scripts\\Activate  # windows
    "or"
source .env/Scripts/Activate  # windows with git-bash
    "or"
source .env/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
playwright install chromium
```
## Usage

- Ensure virtual environment (.env) has been activated.
- cd to required dir and run code in accordance with scrapers README.md

```bash
# Move to unsplash dir:
cd unsplash

# Run script in accordance with scraper README.py
python scrape_unsplash_with_api.py
```

## Caveat: Selectors and Website Changes

Please note that the web scraping scripts in this repository rely on extracting specific HTML elements (selectors) from the target websites. Web pages can change their structure over time, meaning that the HTML tags, classes, or attributes used to locate the required data may no longer be valid. If a website changes its layout or structure, the current selectors may not work, leading to errors or incomplete data extraction.



### How to Handle Selector Issues:
1. **Inspect the Website**: Use the browser's developer tools (right-click → "Inspect") to view the HTML structure of the page. Look for the relevant data you want to scrape and check for any changes in the structure, class names, or tags.

2. **Update the Scraper**: Once you've identified any changes, update the scraping logic in the script (e.g., change the CSS selectors, update the parsing logic).

3. **Test the Script**: After making updates, thoroughly test the script to ensure it works as expected. Verify that all necessary data is extracted and that the program doesn't break with new changes.
