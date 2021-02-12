# 2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы.

from pymongo import MongoClient
from pprint import pprint


def select_salary(salary, currency):
    client = MongoClient('localhost', 27017)
    db = client['my_database']

    select_vacancy = []
    for i in db.vacancies.find({'salary_currency': currency, '$or':
        [{'max_salary': {'$gt': salary}}, {'min_salary': {'$gte': salary}}]}):
        select_vacancy.append(i)
    return select_vacancy

if __name__ == "__main__":
    while True:
        user_answer = input('Введите желаемую зарплату и валюту (руб., USD, EUR и т.п.) через пробел\n >>>')
        try:
            salary, currency = user_answer.split(' ')
            if currency in ('руб', 'RUR'):
                currency = 'руб.'
            select_vacancy = select_salary(int(salary), currency)
        except ValueError as e:
            print(f'Введены некорректные данные {e}')
        else:
            pprint(select_vacancy)
            break
