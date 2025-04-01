import scrapy
from scrapy_playwright.page import PageMethod
import math
from scrapy.loader import ItemLoader
from ..items import JobContainerItem
from pathlib import Path


class GetJobsSpider(scrapy.Spider):
    name = "get_jobs"  # The name of the spider
    allowed_domains = ["www.workingnomads.com"]  # Allowed domains for the spider
    start_urls = ["https://www.workingnomads.com/jobs"]  # The URL the spider will start from

    def __init__(self, n_listings=200, **kwargs):
        """ Initialization method to set up the number of listings required and the JS code for page interaction.
        param n_listings: The total number of job listings the spider should scrape
        """
        super().__init__(**kwargs)  # Initialize the parent class (Spider)
        self.required_jobs = int(n_listings)  # Set the number of jobs to scrape
        self.js_code = self.load_js_code(3000)  # Load the JavaScript code for scrolling and job loading

    def load_js_code(self, click_timeout):
        """ This function loads the JavaScript code that will be executed to load additional job listings.
        param click_timeout: Time in milliseconds to wait for the page to load after clicking
        return: The modified JavaScript code with the appropriate number of pages to load
        """
        jobs_per_page = 50  # How many jobs does the site load per page? This may change
        load_pages = math.ceil(self.required_jobs / jobs_per_page) - 1  # Calculate how many pages to load
        file_path = Path.joinpath(Path.cwd(), "job_site/spiders/page_method.js")  # Path to the JS code
        with open(file_path, "r") as js_file:
            js_code = js_file.read()  # Read the JavaScript code from the file

        # Replace placeholders in the JS code with the correct values
        js_code = js_code.replace("LOAD_PAGES", str(load_pages))
        js_code = js_code.replace("CLICK_TIMEOUT", str(click_timeout))

        return js_code  # Return the modified JavaScript code

    def start_requests(self):
        """ This method starts the initial request to the target URL and sends Playwright page methods
        for interaction (waiting for elements and executing JS code).
        """
        yield scrapy.Request(
            self.start_urls[0],  # The URL to start scraping from
            meta=dict(
                playwright=True,  # Enable Playwright to handle JavaScript
                playwright_page_methods=[  # List of Playwright methods to run on the page
                    PageMethod("wait_for_selector", 'div.jobs-list div.job-wrapper'),  # Wait for job elements to load
                    PageMethod("wait_for_selector", "#accept-btn"),  # Wait for the accept button
                    PageMethod("click", "#accept-btn"),  # Click the accept button (e.g., for cookies)
                    PageMethod("evaluate", self.js_code),  # Execute the custom JavaScript to load more jobs
                ]
            )
        )

    async def parse(self, response):
        """ This callback function processes the response and extracts job data. """

        count = 0  # Initialize count

        # Loop through each job in the response
        for job in response.css('div.jobs-list div.ng-scope div.job-wrapper'):

            if count >= self.required_jobs:  # Stop when enough jobs are collected
                break

            job_title = job.css('h4.hidden-xs a.open-button.ng-binding::text').get()

            if job_title and job_title.strip():  # Ensure job title is valid
                count += 1
                item = ItemLoader(item=JobContainerItem(), selector=job)  # Initialize item loader

                # Add job details
                item.add_css("job_name", 'h4.hidden-xs a.open-button.ng-binding::text')
                item.add_css("job_link", 'a.open-button.ng-binding::attr(ng-href)')
                item.add_css("company_name", 'div.company.hidden-xs a::text')
                item.add_css("job_location", 'div.box i.fa-map-marker + span::text')
                item.add_css("work_type", 'div.box i.fa-clock-o + span::text')

                # Extract job tags
                tags = job.xpath(
                    './/div[contains(@class, "box") and contains(@class, "hidden-xs") and contains(@class, "ng-scope")]/a/text()'
                ).getall()
                item.add_value("tags", tags)

                # Yield the item
                yield item.load_item()

                # Alternative way to yield a job if needed (commented out):
                # yield {
                #     "job_name": job.css("a.open-button.ng-binding::text").get(),
                # }
