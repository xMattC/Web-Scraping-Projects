import re
import scrapy
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags


# Function to remove commas from numerical values (e.g., "1,000" -> "1000")
def remove_commas(value):
    return value.replace(",", "")


# Function to attempt conversion of a string to an integer
def try_int(value):
    try:
        return int(value)  # Convert to integer if possible
    except ValueError:
        return value  # Return original value if conversion fails


# Function to attempt conversion of a string to a float
def try_float(value):
    try:
        return float(value)  # Convert to float if possible
    except ValueError:
        return value  # Return original value if conversion fails


# Function to extract the first four-digit year from a string
def extract_year(value):
    year = re.findall(r"\d{4}", value)  # Find all four-digit numbers
    if not year:
        return value  # Return original value if no year is found
    return year  # Return extracted year(s) as a list


# Define the Scrapy item for storing GDP data
class CountryGdpItem(scrapy.Item):
    # Country name field with text cleaning and extraction
    country_name = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),  # Remove HTML tags and extra spaces
        output_processor=TakeFirst()  # Take the first extracted value
    )

    # Year field with text cleaning, year extraction, and conversion to integer
    year = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip, extract_year, try_int),
        output_processor=TakeFirst()
    )

    # GDP field with text cleaning, comma removal, and conversion to float
    gdp = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip, remove_commas, try_float),
        output_processor=TakeFirst()
    )
