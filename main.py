from utilities.extract import extract_full_body_html
from selectolax.parser import HTMLParser
from config.tools import get_config
from utilities.parse import parse_raw_attributes
# URL = "https://store.steampowered.com/specials"

if __name__ == "__main__":
    config = get_config()

    html = extract_full_body_html(
        from_url=config.get('url'),
        wait_for_element=config.get('container').get('selector')
    )

    tree = HTMLParser(html)
    divs = tree.css(config.get('container').get('selector'))

    for d in divs:
        attrs = parse_raw_attributes(d, config.get('item'))
        # # Extract game title
        # title = d.css_first('div[class*="StoreSaleWidgetTitle"]').text()
        #
        # # Extract game thumbnail image URL
        # thumbnail = d.css_first('img[class*="_2eQ4mkpf4IzUp1e9NnM2Wr"]').attributes.get("src")
        #
        # # Extract up to 5 tags associated with the game
        # tags = [a.text() for a in d.css('div[class*="_2bkP-3b7dvr0a_qPdZEfHY"] > a')[:5]]
        #
        # # Extract release date
        # release_data = d.css_first('div[class*="_1qvTFgmehUzbdYM9cw0eS7"]').text()
        #
        # # Extract review score and count
        # review_score = [div.text() for div in d.css('a[class*="ReviewScore"] > div > div')][0]
        # review_count = [div.text() for div in d.css('a[class*="ReviewScore"] > div > div')][1]
        #
        # # Extract original price, sale prices and reduction percentage
        # price_sale = [div.text() for div in d.css('div[class*=StoreSalePriceWidgetContainer] > div > div')][1]
        # price_orig = [div.text() for div in d.css('div[class*=StoreSalePriceWidgetContainer] > div > div')][0]
        # reduction_percent = d.css_first('div[class*=StoreSalePriceWidgetContainer] > div').text()
        #
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

        # Print extracted game details
        print(attrs)
