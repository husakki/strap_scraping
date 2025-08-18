import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule

from ..items import Watchstrap


class StrapSpider(CrawlSpider):
    name = "strap"
    allowed_domains = ["www.watch-tools.de"]
    start_urls = ["https://www.watch-tools.de"]
    
    rules = (
        # find the strap types
        Rule(LinkExtractor(allow=(r"(straps\.php)",))),
        # find the straps sizes
        Rule(LinkExtractor(allow=(r"[a-zA-Z]+-straps/([0-9]+mm[-up]*|[a-zA-Z0-9-]+).php",))),
        # its a product list page
        Rule(LinkExtractor(allow=(r"[a-zA-Z]+-straps/([0-9]+mm[-up]*|[a-zA-Z0-9-]+)/([a-zA-Z0-9-]+.php)",)), callback ="parse_strap")
        
    )
    
    def parse(self, response):
        self.logger.info(f"!!!Visiting!!! {response.url}")
        yield scrapy.Request(response.url, self.parse_strap)

    def parse_strap(self, response):
        self.logger.info(f"Parsing strap from {response.url}")
        # TODO if "strap" is not in the URL, skip the item
        if "strap" not in response.url:
            self.logger.info(f"Skipping {response.url} as it does not contain 'strap'")
            return
        # TODO get the response URL and extract the size from it
        match = re.search(r"([0-9]+mm).php|([0-9]+mm[a-zA-Z-]*).php|([a-zA-Z-]*[0-9]+mm).php", response.url)
        size = None
        if match:
            if match.group(1):
                self.logger.info(f"Found size g1: {match.group(1)}")
                size = match.group(1)
            elif match.group(2):
                self.logger.info(f"Found size g2: {match.group(2)}")
                # Remove everything after the digits+mm and prepend ">"
                base = re.match(r"([0-9]+mm)", match.group(2))
                if base:
                    size = ">" + base.group(1)
            elif match.group(3):
                self.logger.info(f"Found size g3: {match.group(3)}")
                # Remove everything before the digits+mm and prepend "<"
                base = re.search(r"([0-9]+mm)", match.group(3))
                if base:
                    size = "<" + base.group(1)
                    
        loader = ItemLoader(item=Watchstrap(), response=response)
        loader.add_css("name", ".product-name h1::text")
        loader.add_css("price", ".price::text")
        loader.add_css("description", "div#product_tabs_description_contents div.std::text")
        loader.add_value("size", size)
        
        # yield {
        #     "name": response.css(".product-name").css("h1::text").get(),
        #     "price": response.css(".price::text").get(),
        #     "description": response.css("div#product_tabs_description_contents").css("div.std::text").get(),
        # }
        
        return loader.load_item()
