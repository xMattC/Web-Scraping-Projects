import pandas as pd
from selectolax.parser import Node
from datetime import datetime
import re


def format_and_transform(attrs: dict):
    transforms = {
        "release_data": lambda date: reformat_date(date, '%b %d, %Y', '%Y-%m-%d'),
        "thumbnail": lambda n: get_attrs_from_node(n, "src"),
        "tags": lambda l: get_first_n(l, 5),
        "review_score": lambda l: index(l, 0),
        "review_count": lambda l: int(''.join(regex(index(l, 1), r'\d+'))),
        "orig_price": lambda l: index(l, 0),
        "sale_price": lambda l: index(l, 0),
        "discount_pct": lambda l: index(l, 0),
        # "price_currency": lambda l: float(regex(index(l, 0), r'\s', "split")[0]),
        # "orig_price": lambda l: float(regex(index(l, 0), r'\s', "split")[1]),
        # "sale_price": lambda l: float(regex(index(l, 0), r'\s', "split")[1]),

    }
    for key, value in transforms.items():
        if key in attrs:
            attrs[key] = value(attrs[key])

    return attrs


def get_attrs_from_node(node: Node, attr: str):
    if node is None or not issubclass(Node, type(node)):
        raise ValueError("The function expects a selecolax node to be provided")

    return node.attributes.get(attr)


def get_first_n(input_list: list, n: int = 5):
    return input_list[:n]


def index(input_list: list, i: int = 0):
    try:
        return input_list[i]

    except:
        return "None"


def reformat_date(date_raw: str, input_format: str = '%b %d, %Y', output_format: str = '%Y-%m-%d'):
    dt_obj = datetime.strptime(date_raw, input_format)
    return datetime.strftime(dt_obj, output_format)


def regex(input_str: str, pattern: str, do_what: str = "findall"):
    if do_what == "findall":
        return re.findall(pattern, input_str)

    elif do_what == "split":
        return re.split(pattern, input_str)

    else:
        raise ValueError("The function expects 'findall' or 'split' to be provided")


def save_to_file(filename="extract", data: list[dict] = None):
    if data is None:
        raise ValueError("The function expects data to be provided as a list of dictionaries")

    df = pd.DataFrame(data)
    filename = f"outputs/{datetime.now().strftime('%Y_%m_%d')}_{filename}.csv"
    df.to_csv(filename, index=False)
