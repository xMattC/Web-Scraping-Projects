import scrapy


class CountryGdpItem(scrapy.Item):
    # define the fields for your item here like:
    country_name = scrapy.Field()
    gdp = scrapy.Field()
    year = scrapy.Field()

