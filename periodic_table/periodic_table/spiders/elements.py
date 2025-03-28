import scrapy
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags

class ElementsSpider(scrapy.Spider):
    name = "elements"

    def start_requests(self):
        yield scrapy.Request('https://pubchem.ncbi.nlm.nih.gov/ptable', meta=dict(
            playwright=True
        ))

    def parse(self, response):
        pass
