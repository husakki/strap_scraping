import scrapy
from itemloaders.processors import MapCompose, TakeFirst
from scrapy.item import Field, Item
from w3lib.html import remove_tags


class Watchstrap(Item):
    name = Field(
        input_processor= MapCompose(remove_tags),
        output_processor= TakeFirst())
    price = Field(
        input_processor= MapCompose(remove_tags, lambda x: x.replace('€', '').strip()),
        output_processor= TakeFirst())
    description = Field(
        input_processor= MapCompose(remove_tags, lambda x: x.strip()),
        output_processor= TakeFirst())
    size = Field(
        input_processor= MapCompose(remove_tags),
        output_processor= TakeFirst())
    link = Field(
        input_processor= MapCompose(remove_tags),
        output_processor= TakeFirst())
