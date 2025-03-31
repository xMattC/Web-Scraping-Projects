import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags


def remove_newlines(value):
    """ Function to remove newlines and extra spaces from a string.
    It strips leading/trailing spaces and replaces newline characters with an empty string.
    """
    return value.replace("\n", "").strip()  # Remove newlines and extra spaces


def modify_job_link(link):
    """ Function to modify the job link by adding the base URL.
    Appends the link to the base URL to form a complete link.
    """
    new_link = f"https://www.workingnomads.com{link}"  # Concatenate base URL with the job-specific URL
    return new_link


class JobContainerItem(scrapy.Item):
    """ Class defining the structure of the job data to be scraped.
    Each field represents a piece of data extracted from the job listing.
    """

    # Field to store the job title
    job_name = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip, remove_newlines),  # Remove HTML tags, strip spaces, and remove newlines
        output_processor=TakeFirst()  # Take the first extracted value (ensures single value)
    )

    # Field to store the job link (URL)
    job_link = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip, modify_job_link),  # Remove HTML tags, strip spaces, and modify the link
        output_processor=TakeFirst()  # Take the first extracted value
    )

    # Field to store the company name
    company_name = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),  # Remove HTML tags and strip spaces
        output_processor=TakeFirst()  # Take the first extracted value
    )

    # Field to store the job location
    job_location = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),  # Remove HTML tags and strip spaces
        output_processor=TakeFirst()  # Take the first extracted value
    )

    # Field to store the work type (e.g., Full-time, Part-time)
    work_type = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),  # Remove HTML tags and strip spaces
        output_processor=TakeFirst()  # Take the first extracted value
    )

    # Field to store the tags associated with the job (e.g., skills, category)
    tags = scrapy.Field(
        # This field is not processed in the current version, but you could apply processors like MapCompose and TakeFirst
        # For now, it is left empty
    )
