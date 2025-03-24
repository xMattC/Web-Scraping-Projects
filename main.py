from utilities.extract import extract_full_body_html
from selectolax.parser import HTMLParser
from config.tools import get_config
from utilities.parse import parse_raw_attributes
from utilities.post_process import format_and_transform


def main():
    config = get_config()

    html = extract_full_body_html(
        from_url=config.get('url'),
        wait_for_element=config.get('container').get('selector')
    )

    tree = HTMLParser(html)
    divs = tree.css(config.get('container').get('selector'))

    for d in divs:
        attrs = parse_raw_attributes(d, config.get('item'))
        attrs = format_and_transform(attrs)
        print(attrs)

        # # Extract original price, sale prices and reduction percentage
        # price_sale = [div.text() for div in d.css('div[class*=StoreSalePriceWidgetContainer] > div > div')][1]
        # price_orig = [div.text() for div in d.css('div[class*=StoreSalePriceWidgetContainer] > div > div')][0]
        # reduction_percent = d.css_first('div[class*=StoreSalePriceWidgetContainer] > div').text()


if __name__ == "__main__":
    main()
