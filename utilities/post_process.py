import pandas as pd
from selectolax.parser import Node
from datetime import datetime
import re


# # Store extracted data in a dictionary
# attrs = {
#     "title": title,
#     "release_data": release_data,
#     "review_score": review_score,
#     "review_count": review_count,
#     "price_orig": price_orig,
#     "price_sale": price_sale,
#     "reduction_percent": reduction_percent,
#     "tags": tags,
#     "thumbnail": thumbnail
# }

def format_and_transform(attrs: dict):
    transforms = {
        # "release_data": lambda date: reformat_date(date, '%b %d, %Y', '%Y-%m-%d'),
        "thumbnail": lambda n: get_attrs_from_node(n, "src"),
        "tags": lambda input_list: get_first_n(input_list, 5),
        "release_date": lambda date: reformat_date(date, '%b %d, %Y', '%Y-%m-%d'),

        # # Extract review score and count
        # "review_score" = [div.text() for div in d.css('a[class*="ReviewScore"] > div > div')][0]
        # "review_count" = [div.text() for div in d.css('a[class*="ReviewScore"] > div > div')][1]
        #
        "review_score": lambda input_list: get_list_item_by_index(input_list, 0),
        "review_count": lambda input_list: get_list_item_by_index(input_list, 1),

        #     "price_orig": price_orig,
        #     "price_sale": price_sale,
        #     "reduction_percent": reduction_percent,
        "currency": lambda input_list: process_price_data(input_list, "currency"),
        "sale_price": lambda input_list: process_price_data(input_list, "currency"),
        "orig_price": lambda input_list: process_price_data(input_list, "currency"),
        "discount_pct": lambda input_list: process_price_data(input_list, "currency"),
        # "price_sale": lambda input_list: get_list_item_by_index(input_list, 1),
        # "reduction_percent": lambda raw: float(regex(raw, r'\s', "split")[1])
        # price_sale = [div.text() for div in d.css('div[class*=StoreSalePriceWidgetContainer] > div > div')][1]
        # price_orig = [div.text() for div in d.css('div[class*=StoreSalePriceWidgetContainer] > div > div')][0]
        # reduction_percent = d.css_first('div[class*=StoreSalePriceWidgetContainer] > div').text()

        # "price_currency": lambda raw: regex(raw, r'\s', "split")[0],
        # "sale_price": lambda raw: float(regex(raw, r'\s', "split")[1]),
        # "original_price": lambda raw: float(regex(raw, r'\s', "split")[1])
    }
    for key, value in transforms.items():
        if key in attrs:
            attrs[key] = value(attrs[key])

    # attrs["discount_pct"] = round((attrs["original_price"] - attrs["sale_price"]) / attrs["original_price"] * 100, 3)

    return attrs


def process_price_data(input_list: list, method: str):
    if method == "currency":
        pass

    if method == "currency":
        pass

    if method == "currency":
        pass

    if method == "currency":
        pass

def get_attrs_from_node(node: Node, attr: str):
    if node is None or not issubclass(Node, type(node)):
        raise ValueError("The function expects a selecolax node to be provided")

    return node.attributes.get(attr)


def get_first_n(input_list: list, n: int = 5):
    return input_list[:n]


def get_list_item_by_index(input_list: list, i: int = 0):
    return input_list[i]


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
    filename = f"{datetime.now().strftime('%Y_%m_%d')}_{filename}.csv"
    df.to_csv(filename, index=False)
