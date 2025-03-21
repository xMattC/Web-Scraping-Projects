from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
import pandas as pd

# Ensure Playwright is installed and Chromium is set up before running the script.
URL = "https://store.steampowered.com/specials"  # Target webpage URL for scraping
FILE_NAME = "steam_deals"  # Output filename


def extract_full_body_html(from_url, wait_for_key_selector=None):
    """Launches a headless browser, navigates to the given URL, scrolls to load content,
    and extracts the full HTML of the page body.

    Args:
        from_url (str): The webpage URL to scrape.
        wait_for_key_selector (str, optional): CSS selector to wait for before extracting HTML.

    Returns:
        str: The full HTML content of the page body.
    """
    with sync_playwright() as p:
        # Launch a headless Chromium browser session (set headless=True for background execution)
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(URL)

        # Wait for the page to fully load (DOM content, network requests, and other resources)
        page.wait_for_load_state("domcontentloaded")  # Ensures initial DOM is ready
        page.wait_for_load_state("networkidle", timeout=1000000)  # Ensures no ongoing network requests
        page.wait_for_load_state("load")  # Ensures all assets are fully loaded

        # Scroll to the bottom of the page to load dynamically loaded content
        page.evaluate("() => window.scroll(0, document.body.scrollHeight)")

        # Wait for a specific element (game item container) to ensure content is present
        if wait_for_key_selector:
            page.wait_for_selector(wait_for_key_selector)

        # Extract and return the full HTML content of the page body
        html = page.inner_html("body")
        return html


def extract_attributes(css_div):
    """Extracts relevant game information from a parsed HTML element.

    Args:
        css_div (HTMLParser): A parsed HTML element representing a game listing.

    Returns:
        dict: A dictionary containing extracted attributes of the game.
    """
    # Scrape game title
    title = css_div.css_first('div[class*="StoreSaleWidgetTitle"]').text()

    # Scrape game thumbnail image URL
    thumbnail = css_div.css_first('img[class*="_2eQ4mkpf4IzUp1e9NnM2Wr"]').attributes.get("src")

    # Scrape up to 5 tags associated with the game (e.g., genre, category)
    tags = [a.text() for a in css_div.css('div[class*="_2bkP-3b7dvr0a_qPdZEfHY"] > a')[:5]]

    # Scrape release date
    release_data = css_div.css_first('div[class*="_1qvTFgmehUzbdYM9cw0eS7"]').text()

    # Scrape review score and review count (handling cases where they are missing)
    try:
        review_score = css_div.css_first('div[class*="_2nuoOi5kC2aUI12z85PneA"]').text()
        review_count = css_div.css_first('div[class*="_1wXL_MfRpdKQ3wZiNP5lrH"]').text()
    except AttributeError:
        review_score = "None"  # Default value if missing
        review_count = "None"

    # Scrape original and discounted sale prices
    price_elements = [_div.text() for _div in css_div.css('div[class*=StoreSalePriceWidgetContainer] > div > div')]
    price_orig = price_elements[0]  # Original price
    price_sale = price_elements[1]  # Discounted price

    # Scrape price reduction percentage
    price_reduction = css_div.css_first('div[class*=StoreSalePriceWidgetContainer] > div').text()

    # Store extracted data in a dictionary
    attrs = {
        "title": title,
        "release_data": release_data,
        "review_score": review_score,
        "review_count": review_count,
        "price_orig": price_orig,
        "price_sale": price_sale,
        "price_reduction": price_reduction,
        "tags": tags,
        "thumbnail": thumbnail
    }
    return attrs


if __name__ == "__main__":
    """Main script execution: Scrapes Steam specials, extracts game details, and saves to CSV."""

    # The main selector for identifying each game listing in the sale section
    key_selector = 'div[class*="_2hhNOdcC6yLwL_rugP3YLf _37iggltdgh0RtNIECJCfOj Focusable"]'

    # Extract the HTML content of the webpage
    html = extract_full_body_html(URL, key_selector)

    # Parse the extracted HTML using Selectolax
    tree = HTMLParser(html)

    # List to store extracted game data
    data = []

    # Select all sale item divs using CSS selectors
    divs = tree.css(key_selector)

    # Iterate through and extract game data: 
    for div in divs:
        attributes = extract_attributes(div)
        data.append(attributes)

    # Convert extracted data into a Pandas DataFrame
    df = pd.DataFrame(data)

    # Save the DataFrame to a CSV file in the "outputs" directory
    df.to_csv(f'../outputs/{FILE_NAME}.csv', index=False)

    print(f"Scraped data saved to '../outputs/{FILE_NAME}.csv'")
