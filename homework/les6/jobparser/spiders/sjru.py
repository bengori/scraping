import scrapy
from scrapy.http import HtmlResponse
from scraping.homework.les6.jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[contains(@class, '-button-dalshe')]/@href").extract_first()
        vacancies_links = response.xpath("//div[contains(@class, '-vacancy-item')]//div[contains(@class,'_3mfro')]/a/@href").extract()

        for link in vacancies_links:
            yield response.follow(link, callback=self.vacancy_parse)

        if next_page:
            yield response.follow(next_page, callback=self.parse)
        else:
            return

    def vacancy_parse(self, response: HtmlResponse):
        item_name = response.xpath("//h1/text()").extract_first()
        item_salary = response.xpath(
            "//div[contains(@class, 'vacancy-base-info')]//span[contains(@class,'PlM3e')]//text()").extract()
        item_link = response.url
        item_source = self.allowed_domains
        yield JobparserItem(name=item_name, salary=item_salary, link=item_link, source=item_source)
