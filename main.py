import logging
from config.tools import get_config
from utilities.extract import extract_full_body_html
from utilities.parse import parse_raw_attributes
from utilities.post_process import format_and_transform, save_to_file


def main():
    """ Main function to extract game data from a webpage and save it to a file.
        This function performs the following steps:
            1. Loads the configuration settings (e.g., target URL, selectors).
            2. Extracts the webpage's HTML content.
            3. Parses relevant elements based on provided CSS selectors.
            4. Extracts, formats, and processes the necessary data.
            5. Saves the extracted data to a CSV file.
    """
    try:
        # Load configuration settings (contains URL, selectors, and extraction rules)
        config = get_config()

        if not config:
            logging.error("Failed to load configuration. Exiting...")
            return

        # Retrieve the full HTML content from the specified URL
        logging.info("Extracting HTML content from the page...")
        html = extract_full_body_html(
            from_url=config.get('url'),
            # Ensures page has loaded the container holding all the game deals (12 per page).
            wait_for_element=config.get('container').get('selector')
        )

        # Extract the main container that holds All 'store_sales_divs' css nodes and store as a dict containing game
        # nodes  i.e. {'store_sales_divs': [<Node div>, <Node div>,...]} - 12 per page on for the steam specials
        container = parse_raw_attributes(html, [config.get('container')])

        # Iterate through all game container nodes an extract required information
        game_data = []
        for node in container.get('store_sales_divs'):
            attrs = parse_raw_attributes(node, config.get('item'))  # Extract game attributes
            attrs = format_and_transform(attrs)  # Format and clean extracted data
            game_data.append(attrs)

        # Check if any game data was successfully extracted
        if not game_data:
            logging.warning("No game data extracted. Skipping file save.")
            return

        # Save the extracted data to a CSV file
        save_to_file("steam_specials", game_data)
        logging.info("Data successfully saved to file.")

    except Exception as e:
        # Log any unexpected exceptions that may occur
        logging.exception(f"An error occurred: {e}")


# Run the script when executed directly
if __name__ == "__main__":
    main()
