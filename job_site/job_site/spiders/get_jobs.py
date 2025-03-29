import scrapy
from scrapy_playwright.page import PageMethod
import math
from scrapy.loader import ItemLoader
from ..items import JobContainerItem
from pathlib import Path


class GetJobsSpider(scrapy.Spider):
    name = "get_jobs"
    allowed_domains = ["www.workingnomads.com"]
    start_urls = ["https://www.workingnomads.com/jobs"]

    def __init__(self, n_listings=200, **kwargs):
        super().__init__(**kwargs)
        self.required_jobs = int(n_listings)
        self.js_code = self.load_js_code(3000)

    def load_js_code(self, click_timeout):

        load_pages = math.ceil(self.required_jobs / 100) - 1
        file_path = Path.joinpath(Path.cwd(), "job_site/spiders/page_method.js")

        with open(file_path, "r") as js_file:
            js_code = js_file.read()

        js_code = js_code.replace("LOAD_PAGES", str(load_pages))
        js_code = js_code.replace("CLICK_TIMEOUT", str(click_timeout))

        return js_code

    def start_requests(self):
        yield scrapy.Request(
            self.start_urls[0],
            meta=dict(
                playwright=True,
                playwright_page_methods=[
                    PageMethod("wait_for_selector", 'div.jobs-list div.job-wrapper'),
                    PageMethod("wait_for_selector", "#accept-btn"),
                    PageMethod("click", "#accept-btn"),
                    PageMethod("evaluate", self.js_code),
                ]
            )
        )

    async def parse(self, response):
        for job in response.css('div.jobs-list div.job-wrapper'):
            item = ItemLoader(item=JobContainerItem(), selector=job)
            item.add_css("job_name", 'a.open-button.ng-binding::text')
            item.add_css("job_link", 'a.open-button.ng-binding::attr(href)')
            item.add_css("ng_href", 'a.open-button.ng-binding::attr(ng-href)')
            item.add_css("company_name", 'div.company a::text')
            item.add_css("job_location", 'div.box i.fa-map-marker + span::text')
            item.add_css("work_type", 'div.box i.fa-clock-o + span::text')
            item.add_css("tags", 'div.box i.fa-tags + a::text')
            yield item.load_item()

            # yield {
            #     "job_name": job.css("a.open-button.ng-binding::text").get(),
            # }
