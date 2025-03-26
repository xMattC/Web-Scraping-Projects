import scrapy
from scrapy.loader import ItemLoader
from ..items import CountryGdpItem


class GdpSpider(scrapy.Spider):
    name = "gdp"
    allowed_domains = ["wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"]

    def parse(self, response):
        for country in response.css('table.wikitable.sortable tbody tr:not([class])'):
            item = ItemLoader(item=CountryGdpItem(), selector=country)

            # item.add_value("country_name", 'United Kingdom')  # for testing
            item.add_css("country_name", 'td:nth-child(1) a::text')
            item.add_css("year", 'td:nth-child(3)::text')
            item.add_css("gdp", 'td:nth-child(4)::text')
            yield item.load_item()

        # # Same code but using XPATH:
        # for country in response.xpath("//table[contains(@class, 'wikitable sortable')]//tbody//tr"):
        #     yield {
        #         "country": country.xpath('.//td[1]//a/text()').get(),
        #         "region": country.xpath('.//td[2]//a/text()').get(),
        #         "gdp": country.xpath('.//td[3]/text()').get(),
        #         "year": country.xpath('.//td[4]/text()').get()
        #     }
