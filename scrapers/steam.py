from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser

# Ensure Playwright is installed and Chromium is set up before running the script.
URL = "https://store.steampowered.com/specials"

if __name__ == "__main__":
    with sync_playwright() as p:
        # Launch a headless Chromium browser session
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL)

        # Wait for the page to load completely
        page.wait_for_load_state("networkidle")

        # Scroll to the bottom of the page to load more content
        page.evaluate("() => window.scroll(0, document.body.scrollHeight)")
        page.wait_for_load_state("domcontentloaded")

        # Wait for the sale items to appear in the DOM
        page.wait_for_selector('div[class*="_2hhNOdcC6yLwL_rugP3YLf _37iggltdgh0RtNIECJCfOj Focusable"]')

        # Capture the page's HTML content
        html = page.inner_html("body")
        tree = HTMLParser(html)

        # Select all sale item divs using CSS selectors
        divs = tree.css('div[class*="_2hhNOdcC6yLwL_rugP3YLf _37iggltdgh0RtNIECJCfOj Focusable"]')

        for d in divs:
            # Extract game title
            title = d.css_first('div[class*="StoreSaleWidgetTitle"]').text()

            # Extract game thumbnail image URL
            thumbnail = d.css_first('img[class*="_2eQ4mkpf4IzUp1e9NnM2Wr"]').attributes.get("src")

            # Extract up to 5 tags associated with the game
            tags = [a.text() for a in d.css('div[class*="_2bkP-3b7dvr0a_qPdZEfHY"] > a')[:5]]

            # Extract release date
            release_data = d.css_first('div[class*="_1qvTFgmehUzbdYM9cw0eS7"]').text()

            # Extract review score and count
            review_score = [div.text() for div in d.css('a[class*="ReviewScore"] > div > div')][0]
            review_count = [div.text() for div in d.css('a[class*="ReviewScore"] > div > div')][1]

            # Extract original and sale prices
            price_sale = [div.text() for div in d.css('div[class*=StoreSalePriceWidgetContainer] > div > div')][1]
            price_orig = [div.text() for div in d.css('div[class*=StoreSalePriceWidgetContainer] > div > div')][0]

            # Extract price reduction percentage
            price_reduction = d.css_first('div[class*=StoreSalePriceWidgetContainer] > div').text()

            # Store extracted data in a dictionary
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

            # Print extracted game details
            print(attrs)
