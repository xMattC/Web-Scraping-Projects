import scrapy


class ElementsSpider(scrapy.Spider):
    name = "elements"
    allowed_domains = ["nih.gov"]
    start_urls = ["https://pubchem.ncbi.nlm.nih.gov/ptable/"]

    def parse(self, response):
        pass
