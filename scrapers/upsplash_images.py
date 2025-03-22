from tools import extract_full_body_html
from selectolax.parser import HTMLParser
import logging
import os
from httpx import get

# Configure logging settings
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def scrape_up_splash(terms: list[str]):
    """ Scrapes Unsplash for images related to the given search terms and saves them.
    """
    if not terms or len(terms) == 0:
        raise Exception("No search terms provided")

    for i, term in enumerate(terms):

        if type(term) == str:

            img_nodes = get_img_tags_for(term)  # Extract image nodes from Unsplash search results
            all_img_urls = [get_high_res_img_url(i) for i in img_nodes]  # Extract high-resolution image URLs
            img_urls = [u for u in all_img_urls if u]  # Filter out None values

            save_images(img_urls, term, term)  # Download and save images

        else:
            logging.warning(f"Input list element {i} - ({term}) is not of type string. Ignoring element")


def get_img_tags_for(term: str) -> list:
    """ Fetches image elements from Unsplash search results.
    """
    url = f"https://unsplash.com/s/photos/{term}"
    html = extract_full_body_html(url)

    tree = HTMLParser(html)
    imgs = tree.css('figure[data-testid*="photo-grid-masonry-figure"] a img')

    return imgs


def img_filter_out(url: str, keywords: list[str]) -> bool:
    """ Checks if an image URL contains any unwanted keywords and filters it out.
    """
    return not any(x in url for x in keywords)


def get_high_res_img_url(img_node) -> str | None:
    """ Extracts the highest-resolution image URL from the srcset attribute.
    """
    src_set = img_node.attrs["srcset"]  # Get "srcset" attribute containing multiple image URLs
    src_set_list = src_set.split(", ")  # Split into individual image entries

    # Extract URL with the highest resolution, filtering out unwanted keywords
    url_res = [src.split(" ") for src in src_set_list if img_filter_out(src, ['plus', 'profile', 'premium'])]

    if not url_res:
        return None  # Return None if no valid image URLs remain

    return url_res[0][0].split("?")[0]  # Return the highest-resolution image URL


def save_images(img_urls: list[str], term: str, tag: str = ""):
    """ Downloads images from given URLs and saves them to a directory.
    """
    for url in img_urls:
        resp = get(url)  # Send GET request to download image
        logging.info(f"Downloading {url}...")

        dest_dir = f'../outputs/up-splash/{term}'  # Define output directory path
        file_name = url.split("/")[-1]  # Extract filename from URL

        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)  # Create directory if it does not exist

        # Save image to the specified directory
        with open(f"{dest_dir}/{tag}-{file_name}.jpeg", "wb") as f:
            f.write(resp.content)
            logging.info(f"Saved {file_name}, with size {round(len(resp.content) / 1024 / 1024, 2)} MB.")


def try_with_api_intercept(query: str, per_page='10'):
    """
    """
    url = f"https://unsplash.com/napi/search/photos?page=1&per_page={per_page}&query={query}"
    html = extract_full_body_html(url)
    resp = get(html)

    if resp.status_code == 200:
        return resp.json()


if __name__ == '__main__':
    # Run the scraper with a predefined list of search terms
    # scrape_up_splash(
    #     ['tigers', 'wolves', 'foxes', 'bears', 'rabbits']
    # )

    print(try_with_api_intercept())
