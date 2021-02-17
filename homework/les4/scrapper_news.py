from pprint import pprint
import requests
from lxml import html

my_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/88.0.4324.150 Safari/537.36'}


def requests_lenta_news():
    url = 'https://lenta.ru'
    response = requests.get(f'{url}', headers=my_headers)
    root = html.fromstring(response.text)
    news_block = root.xpath("//div[contains(@class,'b-yellow-box__wrap')]/div[contains(@class, 'item')]")
    base_news = []
    for item in news_block:
        news = {}
        name_source = 'lenta.ru'
        name_news = item.xpath(".//a/text()")
        link_news_info = item.xpath(".//a/@href")
        link_news = f'{url}{link_news_info[0]}'
        response_2 = requests.get(link_news, headers=my_headers)
        root = html.fromstring(response_2.text)
        date_news = root.xpath(".//div[@class = 'b-topic__info']/time/@datetime")

        news['name_source'] = name_source
        news['name_news'] = name_news[0].replace(u'\xa0', ' ')
        news['link_news'] = link_news
        news['date_news'] = date_news[0].replace('T', ' ')

        base_news.append(news)

    return base_news


if __name__ == "__main__":
    lenta_news = requests_lenta_news()
    pprint(lenta_news)
