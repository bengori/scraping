from bs4 import BeautifulSoup as bs
import requests
import re


def salary_hh(salary_str: str):
    salary_str = salary_str.replace('-', ' ')
    salary_list = salary_str.split(' ')
    salary_currency = salary_list[-1]
    if salary_list[0] == 'от':
        min_salary = int(salary_list[1])
        max_salary = None
    elif salary_list[0] == 'до':
        max_salary = int(salary_list[1])
        min_salary = None
    else:
        min_salary = int(salary_list[0])
        max_salary = int(salary_list[1])

    return min_salary, max_salary, salary_currency


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


def amount_page_superjob(vacancy):
    url = 'https://russia.superjob.ru'

    my_params = {
        'keywords': vacancy,
        'page': 0
    }

    my_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
        'Accept': '*/*'}

    response = requests.get(f'{url}/vacancy/search/', params=my_params, headers=my_headers)

    soup = bs(response.text, "html.parser")

    block_info = soup.find('div', {
        'class': re.compile('^_3zucV L1p51')})
    page_button = block_info.find_all('span', {'class': '_1BOkc'})
    last_page = page_button[-2].text
    return int(last_page)


def amount_vacancies_sj(vacancy):
    url = 'https://russia.superjob.ru'

    my_params = {
        'keywords': vacancy,
        'page': 0
    }

    my_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
        'Accept': '*/*'}

    response = requests.get(f'{url}/vacancy/search/', params=my_params, headers=my_headers)

    soup = bs(response.text, "html.parser")

    info = soup.find('div', {'class': 'GPKTZ _1o0Xp _1tH7S'}).next.text
    info = info.split(' ')
    if info[-1] == 'не\xa0найдено':
        amount = 0
    else:
        amount = info[1]

    return int(amount)


def amount_vacancies_hh(vacancy):
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

    block_info = soup.find('h1', {'class': 'bloko-header-1'}).text
    block_info = block_info.replace(u'\xa0', ' ')
    block_info = block_info.split(' ')
    amount_info = []
    for i in block_info:
        if (i.isdigit()):
            amount_info.append(i)
    if len(amount_info) == 2:
        amount_vacancies = ('').join(amount_info)
    else:
        amount_vacancies = amount_info[0]

    return int(amount_vacancies)


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
        vacancy_name = vacancy.find('a').text
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
        except:
            min_salary, max_salary, salary_currency = (None, None, None)
        else:
            min_salary, max_salary, salary_currency = salary_hh(vacancy_salary_info)

        vacancy_data['name'] = vacancy_name
        vacancy_data['link_vacancy'] = vacancy_link
        vacancy_data['name_company'] = vacancy_company_name
        vacancy_data['link_company'] = vacancy_company_link
        vacancy_data['min_salary'] = min_salary
        vacancy_data['maх_salary'] = max_salary
        vacancy_data['salary_currency'] = salary_currency
        vacancies.append(vacancy_data)

    return vacancies


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
    vacancies_list = vacancies_block.find_all('div', {'class': re.compile('^iJCa5 f')})

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

        vacancy_company_info = vacancy.find('span', {'class': re.compile('^_3mfro _3Fsn4')})

        try:
            vacancy_company_name = vacancy_company_info.text
            vacancy_company_link = url + vacancy_company_info.next.attrs['href']
        except AttributeError as e:
            vacancy_company_name = 'нет данных'
            vacancy_company_link = 'нет данных'

        vacancy_salary_block_1 = vacancy_salary_block_1.replace(u'\xa0', '').replace('—', ' ')
        salary_list = vacancy_salary_block_1.split(' ')

        if len(salary_list) == 2:
            if salary_list[0] == 'По':
                min_salary = None
                max_salary = None
                salary_currency = None
            else:
                min_salary = int(salary_list[0])
                max_salary = int(salary_list[1][:-4])
                salary_currency = f'{salary_list[-1][-4:]}, периодичность {vacancy_salary_block_2}'
        else:
            if salary_list[0][:2] == 'от':
                min_salary = int(salary_list[0][2:-4])
                max_salary = None
                salary_currency = f'{salary_list[-1][-4:]}, периодичность {vacancy_salary_block_2}'
            elif salary_list[0][:2] == 'до':
                max_salary = int(salary_list[0][2:-4])
                min_salary = None
                salary_currency = f'{salary_list[-1][-4:]}, периодичность {vacancy_salary_block_2}'
            else:
                max_salary = int(salary_list[0][0:-4])
                min_salary = None
                salary_currency = f'{salary_list[-1][-4:]}, периодичность {vacancy_salary_block_2}'

        vacancy_data['name'] = vacancy_name
        vacancy_data['link_vacancy'] = vacancy_link
        vacancy_data['name_company'] = vacancy_company_name
        vacancy_data['link_company'] = vacancy_company_link
        vacancy_data['min_salary'] = min_salary
        vacancy_data['maх_salary'] = max_salary
        vacancy_data['salary_currency'] = salary_currency
        vacancies.append(vacancy_data)

    return vacancies