import re
import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags


def remove_newlines(value):
    return value.replace("\n", "").strip()  # Remove newlines and extra spaces


def modify_job_link(link):
    new_link = f"https://www.workingnomads.com{link}"
    return new_link


class JobContainerItem(scrapy.Item):
    # Country name field with text cleaning and extraction
    job_name = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip, remove_newlines),  # Remove HTML tags and extra spaces
        output_processor=TakeFirst()  # Take the first extracted value
    )

    # Year field with text cleaning, year extraction, and conversion to integer
    job_link = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip, modify_job_link),
        output_processor=TakeFirst()
    )

    # GDP field with text cleaning, comma removal, and conversion to float
    ng_href = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst()
    )

    # Country name field with text cleaning and extraction
    company_name = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),  # Remove HTML tags and extra spaces
        output_processor=TakeFirst()  # Take the first extracted value
    )

    # Year field with text cleaning, year extraction, and conversion to integer
    job_location = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst()
    )

    # GDP field with text cleaning, comma removal, and conversion to float
    work_type = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst()
    )
    # Year field with text cleaning, year extraction, and conversion to integer
    tags = scrapy.Field(
        # input_processor=MapCompose(remove_tags, str.strip),
        # output_processor=TakeFirst()
    )

    # GDP field with text cleaning, comma removal, and conversion to float
    salary = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst()
    )
