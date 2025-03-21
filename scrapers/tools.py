from playwright.sync_api import sync_playwright
import requests


def extract_full_body_html(from_url, wait_for_key_selector=None):
    """ Launches a headless browser, navigates to the given URL, scrolls to load content,
        and extracts the full HTML of the page body.

    Args:
        from_url (str): The webpage URL to scrape.
        wait_for_key_selector (str, optional): CSS selector to wait for before extracting HTML.

    Returns:
        str: The full HTML content of the page body.
    """
    with sync_playwright() as p:
        # Launch a headless Chromium browser session (set headless=True for background execution)
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(from_url)

        # Wait for the page to fully load (DOM content, network requests, and other resources)
        page.wait_for_load_state("networkidle", timeout=1000000)  # Ensures no ongoing network requests
        page.wait_for_load_state("domcontentloaded")  # Ensures initial DOM is ready
        page.wait_for_load_state("load")  # Ensures all assets are fully loaded

        # Scroll to the bottom of the page to load dynamically loaded content
        page.evaluate("() => window.scroll(0, document.body.scrollHeight)")

        # Wait for a specific element (game item container) to ensure content is present
        if wait_for_key_selector:
            page.wait_for_selector(wait_for_key_selector)

        # Extract and return the full HTML content of the page body
        html = page.inner_html("body")

        return html


def test_user_agents(url: str):
    """ Quick check to determine if URL is blocking simple agents.
        print should show "Status Code: 200" if no block is in place.
    """
    user_agents = [
        # List of some common User-Agent strings to simulate different browsers and devices.
        # Source: https://techblog.willshouse.com/2012/01/03/most-common-user-agents/
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0',
    ]

    for i, agent in enumerate(user_agents):
        data_request = requests.get(url, headers={'User-Agent': agent})
        print(f'Agent {i}:')
        print(f"Status Code: {data_request.status_code}")  # Display HTTP response status
        print(f"Headers: {data_request.request.headers}")  # Show request headers used


# TODO
def rotate_proxi():
    return


if __name__ == "__main__":
    test_user_agents("https://store.steampowered.com/specials")
