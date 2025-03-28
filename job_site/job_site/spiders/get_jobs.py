import scrapy
from scrapy_playwright.page import PageMethod
import math


class GetJobsSpider(scrapy.Spider):
    name = "get_jobs"
    allowed_domains = ["www.workingnomads.com"]
    start_urls = ["https://www.workingnomads.com/jobs"]

    def __init__(self, required_jobs=150, *args, **kwargs):
        super(GetJobsSpider, self).__init__(*args, **kwargs)
        self.required_jobs = 200  # int(required_jobs)

    def start_requests(self):
        load_pages = math.ceil((self.required_jobs / 100)) - 1  # or any number you want to pass
        yield scrapy.Request(
            self.start_urls[0],
            meta=dict(
                playwright=True,
                playwright_page_methods=[
                    PageMethod("wait_for_selector", 'div.jobs-list div.job-wrapper'),
                    PageMethod("wait_for_selector", "#accept-btn"),
                    PageMethod("click", "#accept-btn"),
                    PageMethod("evaluate",
                               f"""
                                    let count = 0;
                                    const load_pages = {load_pages};  // Injected Python variable
                                    async function clickLoadMore() {{
                                        while (count < load_pages) {{
                                            const button = document.querySelector('div.show-more');
                                            if (button) {{
                                                button.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                                                button.click();
                                                count++;
                                                console.log("Clicked, count:", count);  // Debug log
                                                await new Promise(resolve => setTimeout(resolve, 5000));
                                            }} else {{
                                                break;
                                            }}
                                        }}
                                    }}
                                    clickLoadMore();
                                """),
                    # PageMethod("wait_for_timeout", 10000000),
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
