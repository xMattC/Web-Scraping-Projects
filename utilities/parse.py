from selectolax.parser import Node, HTMLParser
import logging
from typing import Union


def parse_raw_attributes(node: Union[Node, str], selectors: list[dict]):
    """
    Extracts attributes from an HTML node based on a list of selector configurations. If a html string is provided,
    it will be converted into an HTMLParser object. In this code this will only be for the top level game container
    i.e. "store_sales_divs". All other node instances should be of type Node and be a child/descendant of
    "dict:store_sales_divs"

    selectors (list[dict]): A list of dictionaries defining what attributes to extract
    """

    if not issubclass(Node, type(node)):
        node = HTMLParser(node)

    parsed = {}

    for s in selectors:
        # Extract configuration values
        match = s.get("match")
        type_ = s.get("type")
        selector = s.get("selector")
        name = s.get("name")

        # Validate selector configuration
        if not all([match, type_, selector, name]):
            logging.warning(f"Skipping invalid selector: {s}")
            continue  # Skip malformed selectors

        try:
            if match == "all":
                # Extract all matching elements
                matched = node.css(selector)

                if type_ == "text":
                    # Extract text from each matched element
                    parsed[name] = [n.text() for n in matched if n is not None]

                elif type_ == "node":
                    # Store raw node objects
                    parsed[name] = matched

                logging.info(f"Extracted {len(parsed[name])} items for '{name}'.")

            elif match == "first":
                # Extract the first matching element
                matched = node.css_first(selector)

                if type_ == "text":
                    # Extract text if element exists
                    parsed[name] = matched.text() if matched else ""

                elif type_ == "node":
                    # Store raw node or None if not found
                    parsed[name] = matched if matched else None

                logging.info(f"Extracted '{parsed[name]}' for '{name}'.")

        except Exception as e:
            # Handle parsing errors
            logging.error(f"Error parsing '{name}': {e}")
            parsed[name] = None  # Ensure the key exists even if an error occurs

    return parsed
