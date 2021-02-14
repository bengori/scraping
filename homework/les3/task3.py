import scrapper
from pymongo import MongoClient


def new_vacancy_to_db(vacancy):
    try:
        total_pages_hh = scrapper.amount_page_hh(vacancy)
    except AttributeError:
        total_pages_hh = 0
    except IndexError:
        total_pages_hh = 0

    vacancies_hh = []
    for page in range(total_pages_hh + 1):
        hh = scrapper.parser_hh(vacancy, page)
        vacancies_hh.extend(hh)

    try:
        total_pages_superjob = scrapper.amount_page_superjob(vacancy)
    except AttributeError:
        total_pages_superjob = 1

    vacancies_sj = []
    for page in range(1, total_pages_superjob + 1):
        sj = scrapper.parser_superjob(vacancy, page)
        vacancies_sj.extend(sj)

    total_vacancy_base = []
    total_vacancy_base.extend(vacancies_hh)
    total_vacancy_base.extend(vacancies_sj)

    client = MongoClient('localhost', 27017)
    db = client['my_database']
    for i in total_vacancy_base:
        id = i['vacancy_id']
        db.vacancies.replace_one({'vacancy_id' : { '$eq' : id } }, i, upsert=True)


if __name__ == "__main__":
    vacancy_name = input('Профессия, должность или компания:\n >>>')
    database = new_vacancy_to_db(vacancy_name)
