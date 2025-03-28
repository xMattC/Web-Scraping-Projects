import scrapy
from scrapy_playwright.page import PageMethod


class GetJobsSpider(scrapy.Spider):
    name = "get_jobs"
    allowed_domains = ["www.workingnomads.com"]
    start_urls = ["https://www.workingnomads.com/jobs"]

    def start_requests(self):
        yield scrapy.Request(
            self.start_urls[0],
            meta=dict(
                playwright=True,
                playwright_page_methods=[
                    PageMethod("wait_for_selector", 'div.jobs-list div.job-wrapper')
                ]
            )
        )


async def parse(self, response):
    for job in response.css('div.jobs-list div.job-wrapper'):
        yield {
            "job_name": job.css("a.open-button.ng-binding::text").get(),
            "job_link": job.css("a.open-button.ng-binding::attr(href)").get(),
            "ng_href": job.css("a.open-button.ng-binding::attr(ng-href)").get(),
            "company_name": job.css("div.company a::text").get(),
            "job_location": job.css("div.box i.fa-map-marker + span::text").get(),
            "work_type": job.css("div.box i.fa-clock-o + span::text").get(),
            "tags": job.css("div.box i.fa-tags + a::text").getall(),
            "salary": job.css("div.box i.fa-money + span::text").get() or job.css(
                "div.box.ng-hide i.fa-money + span::text").get(),
        }
