from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser

# remember playwright install chromium!

URL = "https://store.steampowered.com/specials"

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL)

        page.wait_for_load_state("networkidle")
        page.evaluate("() => window.scroll(0, document.body.scrollHeight)")
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_selector('div[class*="_2hhNOdcC6yLwL_rugP3YLf _37iggltdgh0RtNIECJCfOj Focusable"]')

        # page.screenshot(path="steam.png", full_page=True)
        html = page.inner_html("body")
        tree = HTMLParser(html)

        divs = tree.css('div[class*="_2hhNOdcC6yLwL_rugP3YLf _37iggltdgh0RtNIECJCfOj Focusable"]')

        for d in divs:
            title = d.css_first('div[class*="StoreSaleWidgetTitle"]').text()
            thumbnail = d.css_first('img[class*="_2eQ4mkpf4IzUp1e9NnM2Wr"]').attributes.get("src")
            tags = [a.text() for a in d.css('div[class*="_2bkP-3b7dvr0a_qPdZEfHY"] > a')[:5]]
            release_data = d.css_first('div[class*="_1qvTFgmehUzbdYM9cw0eS7"]').text()
            review_score = [div.text() for div in d.css('a[class*="ReviewScore"] > div > div')][0]
            review_count = [div.text() for div in d.css('a[class*="ReviewScore"] > div > div')][1]
            price_sale = [div.text() for div in d.css('div[class*=StoreSalePriceWidgetContainer] > div > div')][1]
            price_orig = [div.text() for div in d.css('div[class*=StoreSalePriceWidgetContainer] > div > div')][0]
            price_reduction = d.css_first('div[class*=StoreSalePriceWidgetContainer] > div').text()

            attrs = {
                "title": title,
                "release_data": release_data,
                "review_score": review_score,
                "review_count": review_count,
                "price_orig": price_orig,
                "price_sale": price_sale,
                "price_reduction": price_reduction,
                "tags": tags,
                "thumbnail": thumbnail
            }
            print(attrs)
