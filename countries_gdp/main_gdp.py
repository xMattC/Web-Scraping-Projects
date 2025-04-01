from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from countries_gdp.spiders.gdp import GetCountryGDP

if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())
    process.crawl(GetCountryGDP)
    process.start()
