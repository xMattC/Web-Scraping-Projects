from playwright.sync_api import sync_playwright
import playwright

# remember playwright install chromium!

URL = "https://store.steampowered.com/specials"
if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(URL)

        page.wait_for_load_state("networkidle")
        page.evaluate("() => window.scroll(0, document.body.scrollHeight)")

        page.screenshot(path="steam.png", full_page=True)

