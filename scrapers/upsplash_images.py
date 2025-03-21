import os
from tools import extract_full_body_html
from httpx import get
from selectolax.parser import HTMLParser
import logging
import requests


# logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")


#

#
#
# def save_images(img_urls, dest_dir="images", tag=""):
#     for url in img_urls:
#         resp = get(url)
#         # logging.info(f"Downloading {url}...")
#
#         file_name = url.split("/")[-1]
#
#         if not os.path.exists(dest_dir):
#             os.makedirs(dest_dir)
#
#         with open(f"{dest_dir}/{tag}{file_name}.jpeg", "wb") as f:
#             f.write(resp.content)
#             # logging.info(f"Saved {file_name}, with size {round(len(resp.content) / 1024 / 1024, 2)} MB.")

def get_img_tags_for(term=None):
    if not term:
        raise Exception("No search term provided")

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


if __name__ == '__main__':

    img_nodes = get_img_tags_for('stars')
    all_img_urls = [get_high_res_img_url(i) for i in img_nodes]
    img_urls = [u for u in all_img_urls if u]

    print(all_img_urls)
    print(img_urls)
    # save_images(img_urls[:3], dest_dir, search_tag)
