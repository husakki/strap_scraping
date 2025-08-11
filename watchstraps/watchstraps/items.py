# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst
from scrapy.item import Field, Item
from w3lib.html import remove_tags

# TODO price remove the currency symbol 
# TODO description clean up the whitespace and newlines

class Watchstrap(Item):
    name = Field(
        input_processor= MapCompose(remove_tags),
        output_processor= TakeFirst())
    price = Field(
        input_processor= MapCompose(remove_tags),
        output_processor= TakeFirst())
    description = Field(
        input_processor= MapCompose(remove_tags),
        output_processor= TakeFirst())
