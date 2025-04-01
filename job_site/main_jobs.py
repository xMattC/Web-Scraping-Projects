from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from job_site.spiders.get_jobs import GetJobsSpider

if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())
    process.crawl(GetJobsSpider)
    process.start()
