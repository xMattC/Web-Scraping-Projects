import pandas as pd
from selectolax.parser import Node
from datetime import datetime
import re
from typing import List, Dict, Union


def format_and_transform(attrs: Dict[str, Union[str, list, Node]]) -> Dict:
    """Applies transformations to scraped attributes."""
    transforms = {
        "release_date": lambda date: reformat_date(date, '%b %d, %Y', '%Y-%m-%d'),
        "thumbnail": lambda n: get_attrs_from_node(n, "src"),
        "tags": lambda l: get_first_n(l, 5),
        "review_score": lambda l: index(l, 0),  # indexing with function instead of inline to catch exceptions.
        "review_count": lambda l: int(''.join(regex(index(l, 1) or '', r'\d+')) or 0),
        "currency": lambda l: extract_currency(index(l, 0)),
        "orig_price": lambda l: extract_price(index(l, 0)),
        "sale_price": lambda l: extract_price(index(l, 0)),
        "discount_pct": lambda l: index(l, 0),
    }

    for key, func in transforms.items():
        if key in attrs:
            attrs[key] = func(attrs[key])

    return attrs


def get_attrs_from_node(node: Node, attr: str) -> Union[str, None]:
    """Extracts an attribute from a Selectolax node."""
    if node is None or not isinstance(node, Node):
        return None
    return node.attributes.get(attr)


def get_first_n(input_list: List, n: int = 5) -> List:
    """Returns the first `n` elements of a list."""
    return input_list[:n] if isinstance(input_list, list) else []


def index(input_list: List, i: int = 0) -> Union[str, None]:
    """Safely retrieves an index from a list."""
    try:
        return input_list[i]
    except (IndexError, TypeError):
        return None


def reformat_date(date_raw: str, input_format: str = '%b %d, %Y', output_format: str = '%Y-%m-%d') -> Union[str, None]:
    """Reformat a date string from one format to another."""
    if not date_raw:
        return None
    try:
        dt_obj = datetime.strptime(date_raw, input_format)
        return datetime.strftime(dt_obj, output_format)
    except ValueError:
        return None


def regex(input_str: str, pattern: str, do_what: str = "findall") -> Union[List[str], None]:
    """Performs regex operations on a string."""
    if not input_str:
        return None

    if do_what == "findall":
        return re.findall(pattern, input_str)

    elif do_what == "split":
        return re.split(pattern, input_str)

    else:
        raise ValueError("Expected 'findall' or 'split'")


def extract_currency(price_str: str) -> str:
    """Extracts the currency symbol from a price string."""
    if not price_str:
        return ""

    match = re.search(r"[^\d.,\s]+", price_str)  # Matches first non-numeric character(s)

    return match.group() if match else ""


def extract_price(price_str: str) -> float:
    """Extracts the numerical price from a string, handling European decimal commas."""
    if not price_str:
        return 0.0

    # If in Euro format, replace decimal comma (,) with dot (.)
    cleaned_price_str = price_str.replace(',', '.')

    # Extract numerical price
    match = re.search(r"\d+(\.\d+)?", cleaned_price_str)
    return float(match.group()) if match else 0.0


def save_to_file(filename: str = "extract", data: List[Dict] = None) -> None:
    """Saves extracted data to a CSV file with UTF-8 encoding for Excel compatibility."""
    if data is None:
        raise ValueError("Data must be provided as a list of dictionaries.")

    df = pd.DataFrame(data)
    filename = f"outputs/{datetime.now().strftime('%Y_%m_%d')}_{filename}.csv"

    # Save as UTF-8 with BOM to fix encoding issues in Excel
    df.to_csv(filename, index=False, encoding="utf-8-sig")

    print(f"File saved: {filename}")
