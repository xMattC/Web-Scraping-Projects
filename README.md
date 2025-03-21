# Web Scraping Scripts

This repository contains various web scraping scripts for different websites. Each script extracts specific data and saves it in a CSV.

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

### Running a Scraper
```bash
python scrapers/google_finance.py
```

### Legal Disclaimer
Scraping websites may violate their Terms of Service. Always check a website's robots.txt file before scraping and ensure you are not breaking any rules.

- ✅ Allowed: Public data, API endpoints with permission.
- ❌ Not Allowed: Personal data, login-protected content.
