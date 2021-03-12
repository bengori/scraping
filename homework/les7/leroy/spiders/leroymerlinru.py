import scrapy
from scraping.homework.les7.leroy.items import LeroyItem
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader


class LeroymerlinruSpider(scrapy.Spider):
    name = 'leroymerlinru'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search):
        super(LeroymerlinruSpider, self).__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']

    def parse(self, response: HtmlResponse):
        next_page = response.css("a.paginator-button.next-paginator-button::attr(href)").extract_first()
        yield response.follow(next_page, callback=self.parse)

        product_links = response.css("a.plp-item__info__title::attr(href)")
        for link in product_links:
            yield response.follow(link, callback=self.parse_product)

    def parse_product(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroyItem(), response=response)
        loader.add_xpath("name", "//h1/text()")
        loader.add_xpath("description", "//div[@class='def-list__group']//text()")
        loader.add_xpath("price", "//span[@slot='price']/text()")
        loader.add_xpath("photos", "//picture[@slot='pictures']/source[contains(@media,'1024px')]/@data-origin")
        loader.add_value('link', response.url)
        yield loader.load_item()
