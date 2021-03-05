import scrapy
from scrapy.http import HtmlResponse
from scraping.homework.les6.jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://ekaterinburg.hh.ru/search/vacancy?L_save_area=true&clusters=true&enable_snippets=true&'
                  'text=data+engineer&showClusters=true']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").extract_first()
        vacancies_links = response.css("a.bloko-link.HH-LinkModifier::attr(href)").extract()
        for link in vacancies_links:
            yield response.follow(link, callback=self.vacancy_parse)

        if next_page:
            yield response.follow(next_page, callback=self.parse)
        else:
            return

    def vacancy_parse(self, response: HtmlResponse):
        item_name = response.xpath("//h1/text()").extract_first()
        item_salary = response.xpath("//p[@class='vacancy-salary']/span/text()").extract()
        item_link = response.url
        item_source = self.allowed_domains
        yield JobparserItem(name=item_name, salary=item_salary, link=item_link, source=item_source)
