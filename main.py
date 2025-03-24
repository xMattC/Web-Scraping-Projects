from utilities.extract import extract_full_body_html
from selectolax.parser import HTMLParser
from config.tools import get_config
from utilities.parse import parse_raw_attributes
from utilities.post_process import format_and_transform
from utilities.post_process import save_to_file


def main():
    config = get_config()

    html = extract_full_body_html(
        from_url=config.get('url'),
        wait_for_element=config.get('container').get('selector')
    )

    tree = HTMLParser(html)
    divs = tree.css(config.get('container').get('selector'))

    game_data = []
    for d in divs:
        attrs = parse_raw_attributes(d, config.get('item'))
        attrs = format_and_transform(attrs)
        game_data.append(attrs)

    save_to_file("steam_specials.csv", game_data)


if __name__ == "__main__":
    main()
