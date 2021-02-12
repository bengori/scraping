# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, записывающую собранные вакансии
# в созданную БД.

import scrapper
from pymongo import MongoClient
from pprint import pprint


def vacancy_to_db(vacancy):
    # для контроля результатов 'скраппера' вывожу сколько страниц просмотрено, сколько ваканский найдено на сайтах
    # и сколько вакансий будет добавленов базу данных
    try:
        total_pages_hh = scrapper.amount_page_hh(vacancy)
    except AttributeError:
        total_pages_hh = 0
    except IndexError:
        total_pages_hh = 0
    print(f'Количество страниц с вакансиями на сайте hh.ru {total_pages_hh + 1}')

    vacancies_hh = []
    for page in range(total_pages_hh + 1):
        hh = scrapper.parser_hh(vacancy, page)
        vacancies_hh.extend(hh)
    print(f'Количество добавленных вакансий с сайта hh.ru в базу данных - {len(vacancies_hh)}')

    try:
        amount_vacancies_hh = scrapper.amount_vacancies_hh(vacancy)
    except ValueError as e:
        amount_vacancies = None
        print(f'вакансии {vacancy} не найдены')
    else:
        print(f'Количество найденных вакансий {vacancy} на hh.ru - {amount_vacancies_hh}')

    try:
        total_pages_superjob = scrapper.amount_page_superjob(vacancy)
    except AttributeError:
        total_pages_superjob = 1
    print(f'Количество страниц с вакансиями на сайте superjob.ru {total_pages_superjob}')

    vacancies_sj = []
    for page in range(1, total_pages_superjob + 1):
        sj = scrapper.parser_superjob(vacancy, page)
        vacancies_sj.extend(sj)
    print(f'Количество добавленных вакансий с сайта superjob в базу данных - {len(vacancies_sj)}')

    try:
        amount_vacancies_superjob = scrapper.amount_vacancies_sj(vacancy)
    except ValueError as e:
        amount_vacancies = None
        print(f'вакансии {vacancy} не найдены')
    else:
        print(f'Количество найденных вакансий {vacancy} на superjob - {amount_vacancies_superjob}')

    total_vacancy_base = []
    total_vacancy_base.extend(vacancies_hh)
    total_vacancy_base.extend(vacancies_sj)
    # загружаем всю собранную информацию в БД
    client = MongoClient('localhost', 27017)
    db = client['my_database']
    vacancies = db.vacancies
    vacancies.insert_many(total_vacancy_base)


if __name__ == "__main__":
    vacancy_name = input('Профессия, должность или компания:\n >>>')
    database = vacancy_to_db(vacancy_name)
