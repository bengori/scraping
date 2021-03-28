import scrapy
from scrapy.http import HtmlResponse
from scraping.homework.les8.instagram.items import InstagramSubscriberItem, InstagramSubscriptionItem
import re
import json
from urllib.parse import urlencode
from copy import deepcopy


class InstagramcomSpider(scrapy.Spider):
    # атрибуты класса
    name = 'instagramcom'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    insta_login = 'cloudlesssky4u'
    insta_pwd = '#PWD_INSTAGRAM_BROWSER:10:1616097966:AWVQANvPMxiEMZragSCsG7fktOUfNz+5Q8QgTJo8zGCJVhkA6n9CXIsEzoV9t/yyMiWx67c7iH62jxknA8ELSfyEq2nFFtHBQyvjG+3c/dimvPdLjkmjv2V/T5nVWptxPMPkC4QHzyikFw93'
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    parse_user = ['montessori.ekb', 'uralsurfsysert']  # Пользователи, у которых собираем подписчиков и подписки. Список

    graphql_url = 'https://www.instagram.com/graphql/query/?'

    subscribers_hash = '5aefa9893005572d237da5068082d8d5'  # hash для получения данных о подписчиках
    subscriptions_hash = '3dec7e2c57367ef3da3d987d89f9dbc8'  # hash для получения данных о подпиcках

    def parse(self, response: HtmlResponse):  # Первый запрос на стартовую страницу
        csrf_token = self.fetch_csrf_token(response.text)  # csrf token забираем из html
        yield scrapy.FormRequest(  # заполняем форму для авторизации
            self.inst_login_link,
            method='POST',
            callback=self.user_parse,
            formdata={'username': self.insta_login, 'enc_password': self.insta_pwd},
            headers={'X-CSRFToken': csrf_token}
        )

    def user_parse(self, response: HtmlResponse):
        j_body = json.loads(response.text)
        if j_body['authenticated']:  # Проверяем ответ после авторизации
            for username in self.parse_user:
                yield response.follow(
                    # Переходим на желаемую страницу пользователя. Сделать цикл для кол-ва пользователей больше 2-ух
                    f'/{username}/',
                    callback=self.user_data_parse,
                    cb_kwargs={'username': username}
                )

    def user_data_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)  # Получаем id пользователя
        variables = {'id': user_id,  # Формируем словарь для передачи данных в запрос
                     'include_reel': 'true',
                     'fetch_mutual': 'false',
                     'first': 12}

        url_subscribers = f'{self.graphql_url}query_hash={self.subscribers_hash}&{urlencode(variables)}'  # Формируем ссылку для получения данных о постах
        yield response.follow(
            url_subscribers,
            callback=self.user_subscribers_parse,
            cb_kwargs={'username': username,
                       'user_id': user_id,
                       'variables': deepcopy(variables)}  # variables ч/з deepcopy во избежание гонок
        )
        url_subscriptions = f'{self.graphql_url}query_hash={self.subscriptions_hash}&{urlencode(variables)}'
        yield response.follow(
            url_subscriptions,
            callback=self.user_subscriptions_parse,
            cb_kwargs={'username': username,
                       'user_id': user_id,
                       'variables': deepcopy(variables)}  # variables ч/з deepcopy во избежание гонок
        )

    def user_subscribers_parse(self, response: HtmlResponse, username, user_id,
                               variables):  # Принимаем ответ. Не забываем про параметры от cb_kwargs
        j_data = json.loads(response.text)
        page_info = j_data.get('data').get('user').get('edge_followed_by').get('page_info')
        if page_info.get('has_next_page'):  # Если есть следующая страница
            variables['after'] = page_info['end_cursor']  # Новый параметр для перехода на след. страницу
            url_subscribers = f'{self.graphql_url}query_hash={self.subscribers_hash}&{urlencode(variables)}'
            yield response.follow(
                url_subscribers,
                callback=self.user_subscribers_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)}
            )
        subscribers = j_data.get('data').get('user').get('edge_followed_by').get('edges')  # Сами подписчики
        for subscriber in subscribers:  # Перебираем подписчиков, собираем данные
            item_subscriber = InstagramSubscriberItem(
                user_id=user_id,
                category='follow_by',
                subscriber_id=subscriber['node']['id'],
                subscriber_username=subscriber['node']['username'],
                subscriber_fullname=subscriber['node']['full_name'],
                subscriber_foto=subscriber['node']['profile_pic_url']
            )
        yield item_subscriber  # В пайплайн

    def user_subscriptions_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = json.loads(response.text)
        page_info = j_data.get('data').get('user').get('edge_follow').get('page_info')
        if page_info.get('has_next_page'):  # Если есть следующая страница
            variables['after'] = page_info['end_cursor']  # Новый параметр для перехода на след. страницу
            url_subscriptions = f'{self.graphql_url}query_hash={self.subscriptions_hash}&{urlencode(variables)}'
            yield response.follow(
                url_subscriptions,
                callback=self.user_subscribers_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)}
            )
        subscriptions = j_data.get('data').get('user').get('edge_follow').get('edges')  # Сами подписчики
        for subscription in subscriptions:  # Перебираем инфу о подписках, собираем данные
            item_subscription = InstagramSubscriptionItem(
                user_id=user_id,
                category='follow',
                subscription_id=subscription['node']['id'],
                subscription_username=subscription['node']['username'],
                subscription_fullname=subscription['node']['full_name'],
                subscription_foto=subscription['node']['profile_pic_url']
            )
        yield item_subscription  # В пайплайн

    # Получаем токен для авторизации
    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    # Получаем id желаемого пользователя
    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')
