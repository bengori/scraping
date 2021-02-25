"""
1) Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить данные
 о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
Логин тестового ящика: study.ai_172@mail.ru
Пароль тестового ящика: ***
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
import time

chrome_options = Options()
chrome_options.add_argument("--headless")  # Режим без интерфейса
driver = webdriver.Chrome(options=chrome_options)


def info_letter():
    letters = {}
    letters['letter_author'] = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'letter__author')]/span"))).text
    letters['letter_date'] = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'letter__date')]"))).text
    letters['letter_name'] = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'h2'))).text
    letters['letter_text'] = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'html-expander')]"))).text

    return letters


client = MongoClient('localhost', 27017)
db = client['my_database']
mail = db.mail

try:
    driver.get('https://account.mail.ru/login')
    elem = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.NAME, "username")))
    elem.send_keys('study.ai_172')
    elem.send_keys(Keys.ENTER)
    elem = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//input[contains(@name,'password') and contains(@class, 'input')]"))
    )
    elem.send_keys('***')
    elem.send_keys(Keys.ENTER)
except exceptions.TimeoutException as e:
    print(f'Error: {e}')

first_letter = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'llc')]")))
driver.get(first_letter.get_attribute('href'))

while True:
    try:
        mail.insert_one(info_letter())
        next_letter_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'button2_arrow-down'))).click()
        time.sleep(1)
    except exceptions.ElementClickInterceptedException:
        print('Все письма скопированы в БД. Больше писем нет.')
        break

driver.quit()
