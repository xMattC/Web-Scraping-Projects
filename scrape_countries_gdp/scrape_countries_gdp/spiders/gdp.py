import scrapy
from countries_gdp.items import CountryGdpItem

class GdpSpider(scrapy.Spider):
    """
        # scrapy startproject countries_gdp
        # scrapy genspider gdp wikipedia.org
        # Scrapy css selectors cheat sheet https://www.restack.io/p/scrapy-answer-css-selectors
    """
    name = "gdp"
    allowed_domains = ["wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"]

    def parse(self, response):
        #     for country in response.css('table.wikitable.sortable tbody tr:not([class])'):
        #         item = {}#CountryGdpItem()
        #         item["country_name"] = country.css('td:nth-child(1) a::text').get(),
        #         item["year"] = country.css('td:nth-child(3)::text').get(),
        #         item["gdp"] = country.css('td:nth-child(4)::text').get()
        #
        #         print(item)
        #         yield item

        # Same code but using XPATH:
        for country in response.xpath("//table[contains(@class, 'wikitable sortable')]//tbody//tr"):
            yield {
                "country": country.xpath('.//td[1]//a/text()').get(),
                "region": country.xpath('.//td[2]//a/text()').get(),
                "gdp": country.xpath('.//td[3]/text()').get(),
                "year": country.xpath('.//td[4]/text()').get()
            }
