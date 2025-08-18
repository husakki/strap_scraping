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
        yield scrapy.Request(response.url, self.parse_strap)

    def parse_strap(self, response):
        match = re.search(r"\S*[0-9]+\S*.php", response.url)
        if not match:
            self.logger.info(f"Skipping {response.url} as it does not contain 'strap'")
            return
        match = re.search(r"([a-zA-Z-]*[0-9]+mm).php", response.url)
        size = None
        if match:
            if match.group(1):
                base = re.search(r"([0-9]+mm)", match.group(1))
                if base:
                    size = base.group(1)
                else:
                    size = 0
        
                    
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
