from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from scraping.homework.les8.instagram.spiders.instagramcom import InstagramcomSpider
from scraping.homework.les8.instagram import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(InstagramcomSpider)
    process.start()
