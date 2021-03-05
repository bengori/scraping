# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter

from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy_db_0403


    def process_item(self, item, spider):
        if spider.name == 'sjru':
            item['salary'] = self.salary_sj(item['salary'])
        elif spider.name == 'hhru':
            item['salary'] = self.salary_hh(item['salary'])

        vacancy_data = {}
        vacancy_data['name'] = item['name']
        vacancy_data['link_vacancy'] = item['link']
        vacancy_data['min_salary'] = item['salary'][0]
        vacancy_data['maх_salary'] = item['salary'][1]
        vacancy_data['salary_currency'] = item['salary'][2]
        collection = self.mongo_base[spider.name]
        collection.insert_one(vacancy_data)

        return vacancy_data

    def salary_hh(self, salary_list: list):
        if salary_list[0] == 'з/п не указана':
            min_salary = None
            max_salary = None
            salary_currency = None
        else:
            for i in range(len(salary_list)):
                salary_list[i] = salary_list[i].replace(u'\xa0', '').replace('-', ' ')
            salary_currency = salary_list[-2]
            if salary_list[0] == 'от ' and salary_list[2] == ' ':
                min_salary = int(salary_list[1])
                max_salary = None
            elif salary_list[0] == 'до ':
                max_salary = int(salary_list[1])
                min_salary = None
            else:
                min_salary = int(salary_list[1])
                max_salary = int(salary_list[3])

        result = [min_salary, max_salary, salary_currency]
        return result

    def salary_sj(self, salary_list: list):
        if salary_list[0] == 'По договорённости':
            min_salary = None
            max_salary = None
            salary_currency = None
        else:
            for i in range(len(salary_list)):
                salary_list[i] = salary_list[i].replace(u'\xa0', '')
            if salary_list[0] == 'от':
                min_salary = int(salary_list[2][:-4])
                max_salary = None
                salary_currency = f'{salary_list[2][-4:]}'
            elif salary_list[0] == 'до':
                max_salary = int(salary_list[2][:-4])
                min_salary = None
                salary_currency = f'{salary_list[2][-4:]}'
            else:
                min_salary = int(salary_list[0])
                max_salary = int(salary_list[4])
                salary_currency = f'{salary_list[-2]}'

        result = [min_salary, max_salary, salary_currency]
        return result