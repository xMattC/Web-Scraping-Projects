from selectolax.parser import Node
import logging


def parse_raw_attributes(node: Node, selectors: list):
    """
    Parses raw attributes from an HTML node based on selector configurations.

    Args:
        node (Node): A Selectolax Node object representing an HTML element.
        selectors (list): A list of dictionaries specifying attributes to extract.
            Each dictionary should have the following keys:
                - "match" (str): Either "all" or "first", specifying whether to extract all matching elements or just the first one.
                - "type" (str): The type of content to extract, either "text" (text content) or "node" (raw node).
                - "selector" (str): The CSS selector used to locate elements within the node.
                - "name" (str): The key under which extracted data will be stored.

    Returns:
        dict: A dictionary where keys are attribute names, and values are extracted content.
              If an error occurs or a selector is invalid, the corresponding key will have a value of `None`.

    Raises:
        ValueError: If the `selectors` list contains improperly formatted dictionaries.
    """
    parsed = {}

    for s in selectors:
        match = s.get("match")
        type_ = s.get("type")
        selector = s.get("selector")
        name = s.get("name")

        if not all([match, type_, selector, name]):
            logging.warning(f"Skipping invalid selector: {s}")
            continue  # Skip malformed selectors

        try:
            if match == "all":
                matched = node.css(selector) or []

                if type_ == "text":
                    parsed[name] = [n.text() for n in matched if n is not None]

                elif type_ == "node":
                    parsed[name] = matched

                logging.info(f"Extracted {len(parsed[name])} items for '{name}'.")

            elif match == "first":
                matched = node.css_first(selector)

                if type_ == "text":
                    parsed[name] = matched.text() if matched else ""

                elif type_ == "node":
                    parsed[name] = matched if matched else None

                logging.info(f"Extracted '{parsed[name]}' for '{name}'.")

        except Exception as e:
            logging.error(f"Error parsing {name}: {e}")
            parsed[name] = None  # Ensure the key exists even if an error occurs

    return parsed
