import scrapy
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags


class CountryGdpItem(scrapy.Item):

    country_name = scrapy.Field(
        input_processer=MapCompose(remove_tags, str.strip),
        output_processer=TakeFirst()
    )
    # gdp = scrapy.Field(
    #     input_processer=MapCompose(),
    #     output_processer=TakeFirst()
    # )
    year = scrapy.Field(
        input_processer=MapCompose(remove_tags, str.strip),
        output_processer=TakeFirst()

    )
