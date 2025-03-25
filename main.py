import logging
from config.tools import get_config
from utilities.extract import extract_full_body_html
from selectolax.parser import HTMLParser
from utilities.parse import parse_raw_attributes
from utilities.post_process import format_and_transform, save_to_file


def main():
    """ Main function to extract game data from a webpage and save it to a file.
        This function:
            - Loads the configuration settings.
            - Extracts the webpage's HTML.
            - Parses relevant elements using CSS selectors.
            - Extracts and processes the necessary data.
            - Saves the extracted data to a CSV file.
    """
    try:
        # Load configuration settings (URL, selectors, etc.)
        config = get_config()

        # Retrieve the full HTML content from the specified URL
        logging.info("Extracting HTML content from the page...")
        html = extract_full_body_html(
            from_url=config.get('url'),
            wait_for_element=config.get('container', {}).get('selector')  # Wait for a specific element if provided
        )

        # Check if HTML was successfully retrieved
        if not html:
            logging.error("Failed to retrieve HTML. Exiting...")
            return

        # Parse the extracted HTML using Selectolax
        tree = HTMLParser(html)
        # Select elements based on the provided CSS selector
        divs = tree.css(config.get('container', {}).get('selector'))

        # Check if any elements were found
        if not divs:
            logging.warning("No elements found using the provided selector.")
            return

        logging.info(f"Found {len(divs)} elements. Extracting attributes...")

        # Iterate through each extracted element and process the data
        game_data = []
        for d in divs:
            attrs = parse_raw_attributes(d, config.get('item'))  # Extract raw attributes from HTML elements
            attrs = format_and_transform(attrs)  # Apply transformations to format the data
            game_data.append(attrs)

        # Check if any game data was successfully extracted
        if not game_data:
            logging.warning("No game data extracted. Skipping file save.")
            return

        # Save extracted data to a CSV file
        save_to_file("steam_specials", game_data)
        logging.info("Data successfully saved.")

    except Exception as e:
        # Catch and log any exceptions that occur
        logging.exception(f"An error occurred: {e}")


# Run the script when executed directly
if __name__ == "__main__":
    main()
