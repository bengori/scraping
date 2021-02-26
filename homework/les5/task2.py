"""
2) Написать программу, которая собирает «Хиты продаж» с сайта техники mvideo и складывает данные в БД.
Магазины можно выбрать свои. Главный критерий выбора: динамически загружаемые товары
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options
import json
from pymongo import MongoClient
from pprint import pprint
import time

chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(options=chrome_options)

client = MongoClient('localhost', 27017)
db = client['my_database']
mvideo = db.mvideo

driver.get('https://www.mvideo.ru')
time.sleep(2)

try:
    block_hits = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'gallery-layout_products')))
except exceptions.TimeoutException as e:
    print(f'Ошибка при загрузке страницы {e}')

block_hits_name = driver.find_element_by_xpath(
    "//div[contains(@class,'gallery-layout_products')][position()=1]//div[contains(@class,'h2')]").text

if block_hits_name == 'Хиты продаж':
    ul_param = driver.find_element_by_xpath("//ul[contains(@data-init-param, 'Хиты продаж')]").get_attribute('data-init-param')
    data_init_param_ul = json.loads(ul_param)
    total = data_init_param_ul['ajaxContentLoad']['total']

    while True:
        try:
            prev_button = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class,'gallery-layout_products')][position()=1]//a[contains(@class, 'prev-btn')]")
            )).click()
            products = driver.find_elements_by_xpath("//ul[contains(@data-init-param, 'Хиты продаж')]/li")
            if len(products) == total:
                break
        except exceptions.ElementClickInterceptedException as e:
            print(f'Error: {e}. Try again')
            driver.quit()

    products_base = []
    time.sleep(2)

    for product in products:
        item = {}
        name_product = product.find_element_by_class_name('sel-product-tile-title').get_attribute('title')
        item['name_product'] = name_product
        link_product = product.find_element_by_class_name('sel-product-tile-title').get_attribute('href')
        item['link_product'] = link_product
        price = product.find_element_by_class_name('sel-product-tile-title').get_attribute('data-product-info')
        price = json.loads(price)
        item['price'] = float(price['productPriceLocal'])
        products_base.append(item)

    pprint(products_base)
    mvideo.insert_many(products_base)
else:
    print('Блок хиты продаж на странице не найден')

driver.quit()
