from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint


# https://hh.ru/search/vacancy?L_is_autosearch=false&clusters=true&enable_snippets=true&text=data+engineer&page=39
# https://hh.ru/search/vacancy?L_is_autosearch=false&clusters=true&enable_snippets=true&text=data+engineer&page=0
# https://ekaterinburg.hh.ru/search/vacancy?clusters=true&enable_snippets=true&salary=&st=searchVacancy&text=data+engineer

def salary(salary_str: str):
    salary_str = salary_str.replace('-', ' ')  # для hh.ru
    salary_list = salary_str.split(' ')
    salary_currency = salary_list[-1]
    if salary_list[0] == 'от':
        min_salary = f'{salary_list[1]}{salary_currency}'
        max_salary = 'не указана'
    elif salary_list[0] == 'до':
        max_salary = f'{salary_list[1]}{salary_currency}'
        min_salary = 'не указана'
    else:
        min_salary = f'{salary_list[0]}{salary_currency}'
        max_salary = f'{salary_list[1]}{salary_currency}'

    return min_salary, max_salary


def amount_page_hh(vacancy):
    url = 'https://ekaterinburg.hh.ru'
    my_params = {'clusters': 'true',
                 'enable_snippets': 'true',
                 'salary': '',
                 'st': 'searchVacancy',
                 'text': vacancy,
                 'page': 0
                 }

    my_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
        'Accept': '*/*'}

    response = requests.get(f'{url}/search/vacancy/', params=my_params, headers=my_headers)

    soup = bs(response.text, "html.parser")

    block_info = soup.find_all('a', {'class': 'bloko-button HH-Pager-Control'})
    last_page = block_info[-1].attrs['data-page']
    return int(last_page)


def parser_hh(name_vacancy, page):
    url = 'https://ekaterinburg.hh.ru'
    my_params = {'clusters': 'true',
                 'enable_snippets': 'true',
                 'salary': '',
                 'st': 'searchVacancy',
                 'text': name_vacancy,
                 'page': page
                 }

    my_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
        'Accept': '*/*'}

    response = requests.get(f'{url}/search/vacancy/', params=my_params, headers=my_headers)

    if response.status_code == 200:
        pass
    else:
        raise ValueError(f'Error: status_code {response.status_code},text {response.content}')

    soup = bs(response.text, "html.parser")

    vacancies_block = soup.find('div', {'class': 'vacancy-serp'})
    vacancies_list = vacancies_block.find_all('div', {'class': 'vacancy-serp-item'})

    vacancies = []
    for vacancy in vacancies_list:
        vacancy_data = {}
        vacancy_name = vacancy.find('a').text  # можно и так ...find('a',{'class':'bloko-link HH-LinkModifier'}
        vacancy_link = vacancy.find('a').attrs['href']
        vacancy_company_info = vacancy.find('div', {'class': 'vacancy-serp-item__meta-info-company'})
        vacancy_company_name = vacancy_company_info.text
        vacancy_company_link = url + vacancy_company_info.next.attrs['href']
        vacancy_salary_block = vacancy.find('div', {'class': 'vacancy-serp-item__sidebar'})
        vacancy_salary_info = vacancy_salary_block.find('span',
                                                        {'class': 'bloko-section-header-3 bloko-section-header-3_lite'})
        try:
            vacancy_salary_info = vacancy_salary_info.text
            vacancy_salary_info = vacancy_salary_info.replace(u'\xa0', '')
            min_salary, max_salary = salary(vacancy_salary_info)
        except:
            min_salary, max_salary = ('не указана', 'не указана')

        vacancy_data['name'] = vacancy_name
        vacancy_data['link_vacancy'] = vacancy_link
        vacancy_data['name_company'] = vacancy_company_name
        vacancy_data['link_company'] = vacancy_company_link
        vacancy_data['min_salary'] = min_salary
        vacancy_data['maх_salary'] = max_salary
        vacancies.append(vacancy_data)

    pprint(vacancies)


def parser_superjob(name_vacancy, page):
    url = 'https://russia.superjob.ru'

    my_params = {
        'keywords': name_vacancy,
        'page': page
    }

    my_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
        'Accept': '*/*'
    }

    response = requests.get(f'{url}/vacancy/search/', params=my_params, headers=my_headers)
    if response.status_code == 200:
        pass
    else:
        raise ValueError(f'Error: status_code {response.status_code},text {response.content}')

    soup = bs(response.text, "html.parser")

    vacancies_block = soup.find('div', {'class': '_1Ttd8 _2CsQi'})
    vacancies_list = vacancies_block.find_all('div', {'class': 'iJCa5 f-test-vacancy-item _1fma_ undefined _2nteL'})
    # print(len(vacancies_list))
    vacancies = []
    for vacancy in vacancies_list:
        vacancy_data = {}
        vacancy_info = vacancy.find('div', {'class': '_3mfro PlM3e _2JVkc _3LJqf'})
        vacancy_name = vacancy_info.text
        vacancy_link = url + vacancy_info.next.attrs['href']
        vacancy_salary_block_1 = vacancy.find('span', {'class': '_3mfro _2Wp8I PlM3e _2JVkc _2VHxz'}).text
        try:
            vacancy_salary_block_2 = vacancy.find('span', {'class': '_3mfro PlM3e _2JVkc _2VHxz'}).text
        except:
            vacancy_salary_block_2 = ''

        vacancy_company_info = vacancy.find('span', {'class': '_3mfro _3Fsn4 f-test-text-vacancy-item-company-name _9fXTd _2JVkc _2VHxz _15msI'})
        vacancy_company_name = vacancy_company_info.text
        vacancy_company_link = url + vacancy_company_info.next.attrs['href']

        # были ошибки на сайте для этого вставляла блок ниже
        # try:
        #    vacancy_company_name = vacancy_company_info.text
        # except AttributeError as e:
        #    vacancy_company_name = 'нет данных'
        # else:
        #    continue
        # try:
        #    vacancy_company_link = vacancy_company_info.next.attrs['href']
        # except AttributeError as e:
        #    vacancy_company_link = 'нет данных'
        # else:
        #    continue

        vacancy_salary_block_1 = vacancy_salary_block_1.replace(u'\xa0', '').replace('—', ' ')
        salary_list = vacancy_salary_block_1.split(' ')
        # print(salary_list)
        salary_currency = salary_list[-1][-4:]
        if len(salary_list) == 2:
            if salary_list[0] == 'По':
                min_salary = 'по договоренности'
                max_salary = 'по договоренности'
            else:
                min_salary = f'{salary_list[0]}{salary_currency} в {vacancy_salary_block_2}'
                max_salary = f'{salary_list[1][:-4]}{salary_currency} в {vacancy_salary_block_2}'
        else:
            if salary_list[0][:1] == 'от':
                min_salary = f'{salary_list[0][2:-4]}{salary_currency} в {vacancy_salary_block_2}'
                max_salary = 'не указана'
            elif salary_list[0][:1] == 'до':
                max_salary = f'{salary_list[0][2:-4]}{salary_currency} в {vacancy_salary_block_2}'
                min_salary = 'не указана'
            else:
                max_salary = f'{salary_list[0][:-4]}{salary_currency} в {vacancy_salary_block_2}'
                min_salary = 'не указана'

        vacancy_data['name'] = vacancy_name
        vacancy_data['link_vacancy'] = vacancy_link
        vacancy_data['name_company'] = vacancy_company_name
        vacancy_data['link_company'] = vacancy_company_link
        vacancy_data['min_salary'] = min_salary
        vacancy_data['maх_salary'] = max_salary
        vacancies.append(vacancy_data)

    pprint(vacancies)


if __name__ == "__main__":
    text = input('Профессия, должность или компания:\n >>>')

    total_pages_hh = amount_page_hh(text)  # нумерация страниц с 0
    while True:
        try:
            user_answer = input(f'Ответ на запрос: {total_pages_hh + 1} страниц. Укажите номера страниц через'
                                f' пробел либо all, если нужны все страницы\n>>>')
            if user_answer.lower() == 'all':
                pages = [number for number in range(0, total_pages_hh+1)]
                break
            else:
                list_pages = user_answer.split()
                pages = []
                for page in list_pages:
                    page = int(page) - 1
                    pages.append(page)
                break
        except ValueError as e:
            print(f'{e} некорректные данные')

    for page in pages:
        parser_hh(text, page)

    parser_superjob(text, 1)
