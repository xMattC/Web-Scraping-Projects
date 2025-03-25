import json
import logging

# Configure logging to display warning messages
logging.basicConfig(level=logging.INFO)

# Default configuration for scraping Steam specials page
_config = {
    "url": "https://store.steampowered.com/specials",  # URL of the Steam specials page
    "container": {  # Defines the container that holds all sale items for a specific game
        "name": "store_sales_divs",  # Selector for the container:
        "selector": 'div[class*="_2hhNOdcC6yLwL_rugP3YLf _37iggltdgh0RtNIECJCfOj Focusable"]',
        "match": "all",  # Extract "all" or "first" element
        "type": "node"  # type "node" or "text
    },
    "item": [  # List of individual data fields to extract from each sale item game
        {
            "name": "title",  # Selector for the game title
            "selector": 'div[class*="StoreSaleWidgetTitle"]',
            "match": "first",
            "type": "text"
        },
        {
            "name": "tags",  # Selector for category tags (e.g., "Action", "RPG")
            "selector": 'div[class*="_2bkP-3b7dvr0a_qPdZEfHY"] > a',
            "match": "all",
            "type": "text"
        },
        {
            "name": "release_date",  # Selector for the release date
            "selector": 'div[class*="_1qvTFgmehUzbdYM9cw0eS7"]',
            "match": "first",
            "type": "text"
        },
        {
            "name": "review_score",  # Selector for the review score
            "selector": 'a[class*="ReviewScore"] > div > div',
            "match": "all",
            "type": "text"
        },
        {
            "name": "review_count",  # Selector for review count (same as review_score)
            "selector": 'a[class*="ReviewScore"] > div > div',
            "match": "all",
            "type": "text"
        },
        {
            "name": "sale_price",  # Selector for the discounted price
            "selector": 'div[class*=_3j4dI1yA7cRfCvK8h406OB]',
            "match": "all",
            "type": "text"
        },
        {
            "name": "currency",  # Selector for the currency symbol (same as sale_price)
            "selector": 'div[class*=_3j4dI1yA7cRfCvK8h406OB]',
            "match": "all",
            "type": "text"
        },
        {
            "name": "orig_price",  # Selector for the original (non-discounted) price
            "selector": 'div[class*=_3fFFsvII7Y2KXNLDk_krOW]',
            "match": "all",
            "type": "text"
        },
        {
            "name": "discount_pct",  # Selector for the discount percentage
            "selector": 'div[class*=cnkoFkzVCby40gJ0jGGS4]',
            "match": "all",
            "type": "text"
        },
        {
            "name": "thumbnail",  # Selector for the game thumbnail image
            "selector": 'img[class*="_2eQ4mkpf4IzUp1e9NnM2Wr"]',
            "match": "first",
        },
    ]
}


def get_config(load_from_file=False):
    """ Retrieves the configuration.
    If load_from_file is True, it attempts to load the configuration from config.json. If the file is missing or
    contains invalid JSON, it logs a warning and returns None. Otherwise, it returns the default _config dictionary.
    """
    if load_from_file:
        try:
            with open("config.json", "r") as f:
                return json.load(f)

        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.warning(f"Error loading config: {e}")
            return None  # Return nothing if loading fails

    return _config


def generate_config():
    """ Saves the default configuration (_config) to a JSON file named config.json.
    This function ensures that the configuration can be persistently stored.
    """
    with open("config.json", "w") as f:
        json.dump(_config, f, indent=4)


if __name__ == "__main__":
    # When run as a standalone script, generate the config file
    generate_config()
