# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstagramSubscriberItem(scrapy.Item):
    _id = scrapy.Field()
    category = scrapy.Field()
    user_id = scrapy.Field()
    subscriber_id = scrapy.Field()
    subscriber_username = scrapy.Field()
    subscriber_fullname = scrapy.Field()
    subscriber_foto = scrapy.Field()


class InstagramSubscriptionItem(scrapy.Item):
    _id = scrapy.Field()
    category = scrapy.Field()
    user_id = scrapy.Field()
    subscription_id = scrapy.Field()
    subscription_username = scrapy.Field()
    subscription_fullname = scrapy.Field()
    subscription_foto = scrapy.Field()
