from utilities.tools import extract_full_body_html
from selectolax.parser import HTMLParser
import pandas as pd


def scrape_steam_specials():
    """Scrapes the Steam Specials page for discounted games and saves the extracted data to a CSV file."""

    url = "https://store.steampowered.com/specials"  # URL of the Steam Specials page

    # CSS selector for identifying each game listing in the sale section
    key_selector = 'div[class*="_2hhNOdcC6yLwL_rugP3YLf _37iggltdgh0RtNIECJCfOj Focusable"]'

    # Extract the full HTML body of the webpage based on the key selector
    html = extract_full_body_html(url, key_selector)

    tree = HTMLParser(html)  # Parse the extracted HTML using Selectolax

    data = []  # List to store extracted game details

    # Select all sale item divs that match the key selector
    divs = tree.css(key_selector)

    # Iterate through each sale item div and extract relevant attributes
    for div in divs:
        attributes = extract_attributes(div)  # Extract attributes like game title, discount, price, etc.
        data.append(attributes)  # Append extracted game details to the list

    # Convert the extracted game data into a Pandas DataFrame
    df = pd.DataFrame(data)

    # Define the output file path and save the DataFrame as a CSV file
    file_name = '../outputs/steam_deal.csv'
    df.to_csv(file_name, index=False)

    print(f"Scraped data saved to {file_name}")


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
    scrape_steam_specials()
