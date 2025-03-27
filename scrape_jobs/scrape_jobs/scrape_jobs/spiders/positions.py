import scrapy


class PositionsSpider(scrapy.Spider):
    name = "positions"
    allowed_domains = [".com"]
    start_urls = ["https://xxxxxxxxxx.com"]

    def parse(self, response):
        pass
