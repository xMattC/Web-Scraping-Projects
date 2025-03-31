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
        jobs_per_page = 50  # How many jobs doe the site load? this may chang
        load_pages = math.ceil(self.required_jobs / jobs_per_page) - 1
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

        # Loop through each job in the response
        for job in response.css('div.jobs-list div.ng-scope div.job-wrapper'):
            job_title = job.css('h4.hidden-xs a.open-button.ng-binding::text').get()
            if job_title and job_title.strip():  # Check if title exists and is not empty
                item = ItemLoader(item=JobContainerItem(), selector=job)
                item.add_css("job_name", 'h4.hidden-xs a.open-button.ng-binding::text')
                # Extract job link (check for ng-href attribute)
                item.add_css("job_link", 'a.open-button.ng-binding::attr(ng-href)')

                # Extract company name (check the correct CSS selector for company)
                item.add_css("company_name", 'div.company.hidden-xs a::text')

                # Extract job location (ensure the selector is correct)
                item.add_css("job_location", 'div.box i.fa-map-marker + span::text')

                # Extract work type (ensure the correct selector for work type)
                item.add_css("work_type", 'div.box i.fa-clock-o + span::text')

                # Extract tags (ensure the correct selector for tags)
                tags = job.css('div.box.hidden-xs.ng-scope a::text').getall()
                item.add_value("tags", tags)

                tags = job.xpath(
                    './/div[contains(@class, "box") and contains(@class, "hidden-xs") and contains(@class, "ng-scope")]/a/text()').getall()
                item.add_value("tags", tags)

                # Extract the data as a dictionary and check what is being yielded
                job_data = item.load_item()

                yield job_data

            # yield {
            #     "job_name": job.css("a.open-button.ng-binding::text").get(),
            # }
