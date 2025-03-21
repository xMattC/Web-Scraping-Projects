from tools import extract_full_body_html
from selectolax.parser import HTMLParser
import logging
import os
from httpx import get

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def scrape_up_splash(terms: list[str]):
    if not terms or len(terms) == 0:
        raise Exception("No search term provided")

    for term in terms:
        img_nodes = get_img_tags_for(term)
        all_img_urls = [get_high_res_img_url(i) for i in img_nodes]
        img_urls = [u for u in all_img_urls if u]

        save_images(img_urls, term, term)


def get_img_tags_for(term=None):
    url = f"https://unsplash.com/s/photos/{term}"
    html = extract_full_body_html(url)

    tree = HTMLParser(html)
    imgs = tree.css('figure[data-testid*="photo-grid-masonry-figure"] a img')

    return imgs


def img_filter_out(url: str, keywords: list) -> bool:
    return not any(x in url for x in keywords)


def get_high_res_img_url(img_node):
    srcset = img_node.attrs["srcset"]
    srcset_list = srcset.split(", ")

    url_res = [src.split(" ") for src in srcset_list if img_filter_out(src, ['plus', 'profile', 'premium'])]

    if not url_res:
        return None

    return url_res[0][0].split("?")[0]


def save_images(img_urls, term, tag=""):
    for url in img_urls:
        resp = get(url)
        logging.info(f"Downloading {url}...")

        dest_dir = f'../outputs/up-splash/{term}'
        file_name = url.split("/")[-1]

        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        with open(f"{dest_dir}/{tag}-{file_name}.jpeg", "wb") as f:
            f.write(resp.content)
            logging.info(f"Saved {file_name}, with size {round(len(resp.content) / 1024 / 1024, 2)} MB.")


if __name__ == '__main__':
    scrape_up_splash(
        ['lions', 'tigers', 'wolves', 'foxes', 'bears', 'rabbits', 'horses', 'elephants', 'giraffes', 'zebras']
    )
