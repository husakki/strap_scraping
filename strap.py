import scrapy


class StrapSpider(scrapy.Spider):
    name = "strap"
    allowed_domains = ["www.watch-tools.de"]
    start_urls = ["https://www.watch-tools.de"]

    def parse(self, response):
        pass
