# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobparserItem(scrapy.Item):
    _id = scrapy.Field()
    source = scrapy.Field()
    name = scrapy.Field()
    link = scrapy.Field()
    salary = scrapy.Field()



