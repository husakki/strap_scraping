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

    def parse_strap(self, response):
        loader = ItemLoader(item=Watchstrap(), response=response)
        loader.add_css("name", ".product-name h1::text")
        loader.add_css("price", ".price::text")
        loader.add_css("description", "div#product_tabs_description_contents div.std::text")
        
        # yield {
        #     "name": response.css(".product-name").css("h1::text").get(),
        #     "price": response.css(".price::text").get(),
        #     "description": response.css("div#product_tabs_description_contents").css("div.std::text").get(),
        # }
        
        return loader.load_item()
