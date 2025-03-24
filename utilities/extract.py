from playwright.sync_api import sync_playwright


def extract_full_body_html(from_url, wait_for_element=None):
    """
    """
    with sync_playwright() as p:
        # Launch a headless Chromium browser session
        # Ensure Playwright is installed with Chromium (i.e. playwright install chromium)
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(from_url)

        # Wait for the page to load completely
        page.wait_for_load_state("networkidle")

        # Scroll to the bottom of the page to load more content
        page.evaluate("() => window.scroll(0, document.body.scrollHeight)")
        page.wait_for_load_state("domcontentloaded")

        # Wait for specific element if specified:
        if wait_for_element:
            page.wait_for_selector(wait_for_element)

        # Capture the page's HTML content
        html_body = page.inner_html("body")

        return html_body
