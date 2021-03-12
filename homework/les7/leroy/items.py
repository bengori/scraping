# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Compose, TakeFirst



def parse_params(params):
    params = [i.strip() for i in params]
    params = list(filter(None, params))
    result = dict(zip(params[::2], params[1::2]))
    return result


def parse_price(values):
    values = [int(i.replace(' ', '')) for i in values]
    return values


class LeroyItem(scrapy.Item):
    _id: str = scrapy.Field()
    name: str = scrapy.Field(output_processor=TakeFirst())
    photos: list = scrapy.Field()
    description: dict = scrapy.Field(output_processor=Compose(parse_params))
    link: str = scrapy.Field(output_processor=TakeFirst())
    price: int = scrapy.Field(input_processor=Compose(parse_price), output_processor=TakeFirst())
