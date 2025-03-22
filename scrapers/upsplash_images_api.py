from tools import extract_full_body_html
from selectolax.parser import HTMLParser
import logging
import os
from httpx import get
from playwright.sync_api import sync_playwright

# Configure logging settings
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def scrape_up_splash_using_api(terms: list[str], result=20):
    """ Scrapes Unsplash for images related to the given search terms and saves them.
    """
    if not terms or len(terms) == 0:
        raise Exception("No search terms provided")

    for i, term in enumerate(terms):

        if type(term) == str:
            urls = (get_all_image_urls(term, result))
            download_images(urls, term)

        else:
            logging.warning(f"Input list element {i} - ({term}) is not of type string. Ignoring element")


def get_all_image_urls(key_word, results):
    page_number = 0
    img_urls = []

    while len(img_urls) < results:
        data = get_response_for(key_word, page_number)

        page_img_urls = [x["urls"]["raw"] for x in data["results"] if x["premium"] is False]
        page_img_urls = [x.split("?")[0] for x in page_img_urls]

        img_urls.extend(page_img_urls)  # Efficiently appends multiple items
        img_urls = list(dict.fromkeys(img_urls))
        page_number += 1  # Increment page number

    if len(img_urls) > results:
        img_urls = img_urls[:results - len(img_urls)]

    return img_urls


def get_response_for(keyword: str, page_number=0):
    with sync_playwright() as p:
        url = f"https://unsplash.com/napi/search/photos?page={page_number}&per_page={30}&query={keyword}"
        context = p.request.new_context()
        resp = context.get(url)
        return resp.json()


def download_images(img_urls: list[str], term: str, tag: str = ""):
    for url in img_urls:

        resp = get(url)
        logging.info(f"Downloading {url}...")

        dest_dir = f'../outputs/up-splash/{term}'  # Define output directory path

        file_name = url.split("/")[-1]  # Extract filename from URL

        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)  # Create directory if it does not exist

        # Save image to the specified directory
        with open(f"{dest_dir}/{tag}-{file_name}.jpeg", "wb") as f:
            f.write(resp.content)
            logging.info(f"Saved {file_name}, with size {round(len(resp.content) / 1024 / 1024, 2)} MB.")

    return


if __name__ == "__main__":
    scrape_up_splash_using_api(['cats', 'dogs'], 15)
#
