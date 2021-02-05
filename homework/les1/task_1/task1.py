"""
Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
сохранить JSON-вывод в файле *.json.
"""
# https://github.com/ubisoft  ключи в json ответе 'html_url', 'full_url' или просто 'name'


import requests
import json

user = 'ubisoft'
url = 'https://api.github.com'

# универсальная переменная, изменяем переменную user
# формат full_url, ссылка на документацию https://docs.github.com/en/rest/reference/repos#list-repositories-for-a-user
response = requests.get(f'{url}/users/{user}/repos')
if response.status_code == 200:
    print('OK')
    print(response.headers)  # интересно было посмотреть
else:
    print(response.status_code)
    print(response.content)
    print(response.headers)
    print(response.text)

# поиск ссылок на репозитории пользователя
repos = response.json()
for repo in repos:
    if not repo['private']:
        print(repo['html_url'])

filename = f'{user}_repos.json'
with open(filename, 'w') as f:
    # преобразуем в json и сохраняем в файл
    json.dump(repos, f)
