import json

_config = {
    "url": "https://store.steampowered.com/specials",
    "container":
        {
            "name": "store_sales_divs",
            "selector": 'div[class*="_2hhNOdcC6yLwL_rugP3YLf _37iggltdgh0RtNIECJCfOj Focusable"]',
            "match": "all",
            "type": "node"
        },
    "item":
        [
            {
                "name": "title",
                "selector": 'div[class*="StoreSaleWidgetTitle"]',
                "match": "first",
                "type": "text"
            },
            {
                "name": "thumbnail",
                "selector": 'img[class*="_2eQ4mkpf4IzUp1e9NnM2Wr"]',
                "match": "first",
                "type": "node"
            },
            {
                "name": "tags",
                "selector": 'div[class*="_2bkP-3b7dvr0a_qPdZEfHY"] > a',
                "match": "all",
                "type": "text"
            },
            {
                "name": "release_date",
                "selector": 'div[class*="_1qvTFgmehUzbdYM9cw0eS7"]',
                "match": "all",
                "type": "node"
            },
            {
                "name": "review_score",
                "selector": 'a[class*="ReviewScore"] > div > div',
                "match": "all",
                "type": "text"
            },
            {
                "name": "review_count",
                "selector": 'a[class*="ReviewScore"] > div > div',
                "match": "all",
                "type": "text"
            },
            {
                "name": "currency",
                "selector": 'div[class*=StoreSalePriceWidgetContainer] > div',
                "match": "all",
                "type": "text"
            },
            {
                "name": "sale_price",
                "selector": 'div[class*=StoreSalePriceWidgetContainer] > div',
                "match": "all",
                "type": "text"
            },
            {
                "name": "orig_price",
                "selector": 'div[class*=StoreSalePriceWidgetContainer] > div',
                "match": "all",
                "type": "text"
            },
            {
                "name": "discount_pct",
                "selector": 'div[class*=StoreSalePriceWidgetContainer] > div',
                "match": "all",
                "type": "text"
            },
        ]
}


def get_config(load_from_file=False):
    if load_from_file:
        with open("config.json", "r") as f:
            return json.load(f)

    return _config


def generate_config():
    with open("config.json", "w") as f:
        json.dump(_config, f, indent=4)


if __name__ == "__main__":
    generate_config()
