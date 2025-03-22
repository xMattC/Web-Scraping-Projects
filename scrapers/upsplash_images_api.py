import logging
import os
from httpx import get, HTTPStatusError
from playwright.sync_api import sync_playwright

# Configure logging settings to provide timestamped info and error messages
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def scrape_unsplash_using_api(terms: list[str], result=20):
    """
    Scrapes Unsplash for images related to the given search terms and saves them.

    Args:
        terms (list[str]): A list of search terms to query Unsplash.
        result (int, optional): The number of images to fetch per search term. Defaults to 20.

    Raises:
        Exception: If no search terms are provided.
    """
    if not terms or len(terms) == 0:
        raise Exception("No search terms provided")

    for i, term in enumerate(terms):

        if isinstance(term, str):  # Ensure the term is a string before processing
            urls = get_all_image_urls(term, result)
            download_images(urls, term)

        else:
            logging.warning(f"Input list element {i} - ({term}) is not of type string. Ignoring element")


def get_all_image_urls(key_word: str, results: int) -> list[str]:
    """
    Fetches image URLs from Unsplash based on the given search term.

    Iterates through multiple pages of search results until it collects the required
    number of unique image URLs, ensuring duplicates are removed and the list is
    limited to the requested number of images.

    Args:
        key_word (str): The search term for retrieving images.
        results (int): The desired number of image URLs to fetch.

    Returns:
        list[str]: A list of image URLs.
    """
    page_number = 0
    img_urls = []

    while len(img_urls) < results:

        data = get_response_for(key_word, page_number)

        # Extract raw image URLs from the response, filtering out premium images (since they have watermarks)
        page_img_urls = [x["urls"]["raw"] for x in data.get("results", []) if not x.get("premium", True)]
        page_img_urls = [x.split("?")[0] for x in page_img_urls]  # Remove query parameters from URLs

        # Append new unique URLs while maintaining order
        img_urls.extend(page_img_urls)
        img_urls = list(dict.fromkeys(img_urls))  # Removes duplicates while keeping order
        page_number += 1  # Increment page number for the next batch of results

    return img_urls[:results]  # Limit results to the requested amount


def get_response_for(keyword: str, page_number=0):
    """
    Fetches search results from Unsplash API and handles potential errors.

    Uses Playwright to simulate a request to Unsplash’s API and retrieve image search results.
    Playwright is used instead of a direct HTTP request to bypass bot detection mechanisms imposed by
    Unsplash's frontend.

    Args:
        keyword (str): The search term for Unsplash.
        page_number (int, optional): The page number to retrieve results from. Defaults to 0.

    Returns:
        dict or None: A dictionary containing search results or None if an error occurs.
    """
    try:
        with sync_playwright() as p:
            url = f"https://unsplash.com/napi/search/photos?page={page_number}&per_page={30}&query={keyword}"
            context = p.request.new_context()  # Create a new request context
            resp = context.get(url)  # Perform the HTTP request

            return resp.json()

    except HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")

    except Exception as e:
        logging.error(f"An error occurred while fetching data: {e}")
    return None


def download_images(img_urls: list[str], term: str, tag: str = ""):
    """
    Downloads images from the given list of URLs and saves them locally.

    Each image is fetched using an HTTP request, and saved into a directory named after the search term.
    If a tag is provided, it is prefixed to the filename. The function also logs download status and handles
    errors gracefully.

    Args:
        img_urls (list[str]): A list of image URLs to download.
        term (str): The search term used, which determines the subfolder name.
        tag (str, optional): An optional tag to be prefixed to file names. Defaults to an empty string.
    """
    for url in img_urls:
        try:
            resp = get(url)
            resp.raise_for_status()  # Raise error if HTTP request fails
            logging.info(f"Downloading {url}...")

            dest_dir = f'../outputs/up-splash/{term}'  # Define output directory path based on search term
            file_name = url.split("/")[-1]  # Extract filename from URL

            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)  # Create directory if it does not exist

            # Construct file path, avoiding unnecessary '-' if the tag is empty
            file_path = f"{dest_dir}/{f'{tag}-' if tag else ''}{file_name}.jpeg"

            # Save image to the specified directory
            with open(file_path, "wb") as f:
                f.write(resp.content)  # Write binary content to file
                logging.info(f"Saved {file_name}, with size {round(len(resp.content) / 1024 / 1024, 2)} MB.")

        except HTTPStatusError as e:
            logging.error(f"Failed to download {url}: {e.response.status_code} - {e.response.text}")

        except Exception as e:
            logging.error(f"An error occurred while downloading {url}: {e}")


if __name__ == "__main__":
    # Example usage: fetching images for 'cats' and 'dogs'. 15 images for each.
    scrape_unsplash_using_api(['cats', 'dogs'], 15)
