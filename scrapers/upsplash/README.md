
# Unsplash Scraper

## Overview
Scrapes website: [Unsplash.com](https://unsplash.com/)

This project provides two different methods to scrape images from Unsplash and download them based on search terms (or list of search learms). Each method has its advantages and limitations.

Both methods organize downloaded images into separate folders based on search terms.

### 1. API-Based Scraper (`scrape_upsplash_with_api.py`)

The API-based scraper interacts directly with the Unsplash API to fetch high-quality image URLs and download them efficiently.  This method ensures accurate search results and allows users to request as many images as needed, up to the API limits.

- The number of image to download is set by the user.

### 2. HTML-Based Scraper (`scrape_upsplash_with_html.py`)

The HTML-based scraper parses Unsplash's website structure and extracts image URLs from the search results page. This method does not interact with the sites API and it is limited to only retrieving the images displayed on the first search results page. Additionally, since this method relies on the current HTML structure of Unsplash, it may break if Unsplash updates its webpage layout.

- The number of image to download is set by the websits first loading page.


## Installation

### Prerequisites

Ensure you have the required dependencies installed:

```bash
pip install scrapy httpx playwright selectolax
playwright install chromium
```

## Usage

### 1. API-Based Scraper

The API-based scraper retrieves images using HTTP requests and saves them to local storage.

Run the script:

```bash
python scrape_upsplash_with_api.py
```

Example usage in Python:

```python
from scrape_upsplash_with_api import scrape_upsplash_using_api
scrape_upsplash_using_api(["nature", "sunset"], result=30)
```

### 2. HTML-Based Scraper

The HTML-based scraper fetches images by parsing Unsplash’s webpage structure.

Run the script:

```bash
python scrape_upsplash_with_html.py
```

Example usage in Python:

```python
from scrape_upsplash_with_html import scrape_up_splash
scrape_up_splash(["mountains", "forests"])
```
## Output

Downloaded images are stored in:

```
outputs/up-splash/<search_term>/ 
```

## Notes

- The API-based scraper is more efficient and allows downloading a large number of images but is subject to API rate limits.
- The HTML-based scraper does not require an API key but is limited to the fixed number of images displayed on the first search results page.
- Playwright is required for extracting full HTML content.


## Tools & Technologies Used

- **Python**: The primary programming language for both scrapers.
- **Playwright**: For headless browser interaction, used in HTML scraping.
- **Selectolax**: A fast HTML parser for extracting image URLs.
- **HTTPX**: A library for making HTTP requests to download images.
- **Logging**: For real-time tracking of scraper progress and error handling.
- **Scrapy**: For handling web scraping tasks.
