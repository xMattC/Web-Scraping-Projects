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

## Installation & Setup

### Clone the Repository
```bash
git clone https://github.com/xMattC/steam_offers_scraper.git
cd steam_offers_scraper

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
playwright install chromium
```

## Usage
Run the script using Python:

```bash
python main.py
```

This will generate an output CSV file at:

```
../outputs/steam_deals_(todays-date).csv
```

## Output Format
The script generates a CSV file with the following columns:

| Title  | Tags                                     | Release Date | Review Score  | Review Count | Original Price | Currency | Sale Price | Discount | Thumbnail URL |
|--------|-----------------------------------------|-------------|--------------|--------------|---------------|----------|------------|----------|--------------|
| Game 1 | Action, RPG, Casual, Simulation, Automobile Sim | YYYY-MM-DD  | Very Positive | 10,000       | 59.99         | £        | 29.99      | 50%      | Image URL    |


## Notes
- If Steam changes its website structure, the CSS selectors may need updates (i.e. in config --> tools)
