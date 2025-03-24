# Steam Specials Scraper

## Overview
This Python script scrapes discounted games from the Steam Specials page and saves the extracted data to a CSV file. It extracts relevant information such as game titles, discounts, prices, review scores, and tags using web scraping techniques.

## Features
- Scrapes the latest game deals from [Steam Specials](https://store.steampowered.com/specials)
- Extracts:
  - Game title
  - Release date
  - Review score and review count
  - Original and discounted price
  - Discount percentage
  - Game tags (up to 5)
  - Thumbnail image URL
- Saves the extracted data in a structured CSV format

## Folder Structure

```plaintext
web-scraping-scripts/
├── scrapers/        # Contains individual scraper scripts
├── outputs/         # Stores scraped data (CSV)
├── README.md        # Documentation
├── requirements.txt # Python dependencies
└── .gitignore       # Files to ignore in version control
```

## Installation & Setup

### Clone the Repository
```bash
git clone https://github.com/xMattC/web-scraping-scripts.git
cd web-scraping-scripts

# Windows
python -m venv .env
venv\Scripts\Activate

# macOS/Linux
python3 -m venv .env
source venv/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage
Run the script using Python:

```bash
python steam_specials_scraper.py
```

This will generate an output CSV file at:

```
../outputs/steam_deal.csv
```

## Code Explanation
- `scrape_steam_specials()`: Scrapes the Steam Specials page and processes each game listing.
- `extract_attributes(css_div)`: Extracts specific game details from the HTML structure.
- `extract_full_body_html(url, key_selector)`: Extracts the full HTML content from the Steam Specials page (implemented in `tools.py`).

## Output Format
The script generates a CSV file with the following columns:

| Title | Release Date | Review Score | Review Count | Original Price | Sale Price | Discount | Tags | Thumbnail URL |
|--------|--------------|-------------|-------------|----------------|------------|-----------|------|--------------|
| Game 1 | YYYY-MM-DD   | Very Positive | 10,000 | $59.99 | $29.99 | -50% | Action, RPG | Image URL |

## Notes
- The script relies on `extract_full_body_html` from `tools.py`, which should be implemented to fetch the relevant HTML content.
- If Steam changes its website structure, the CSS selectors may need updates.

## License
This project is released under the MIT License.
