import logging
from utilities.extract import extract_full_body_html
from selectolax.parser import HTMLParser
from config.tools import get_config
from utilities.parse import parse_raw_attributes
from utilities.post_process import format_and_transform, save_to_file

# Setup basic logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def main():
    try:
        config = get_config()

        logging.info("Extracting HTML content from the page...")
        html = extract_full_body_html(
            from_url=config.get('url'),
            wait_for_element=config.get('container', {}).get('selector')
        )

        if not html:
            logging.error("Failed to retrieve HTML. Exiting...")
            return

        tree = HTMLParser(html)
        divs = tree.css(config.get('container', {}).get('selector'))

        if not divs:
            logging.warning("No elements found using the provided selector.")
            return

        logging.info(f"Found {len(divs)} elements. Extracting attributes...")

        game_data = []
        for d in divs:
            attrs = parse_raw_attributes(d, config.get('item'))
            attrs = format_and_transform(attrs)
            game_data.append(attrs)

        if not game_data:
            logging.warning("No game data extracted. Skipping file save.")
            return

        save_to_file("steam_specials", game_data)
        logging.info("Data successfully saved.")

    except Exception as e:
        logging.exception(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
