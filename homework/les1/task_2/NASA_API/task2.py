"""
Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа). Выполнить запросы к нему,
пройдя авторизацию. Ответ сервера записать в файл.
"""
# NASA Open API https://api.nasa.gov/
# https://api.nasa.gov/planetary/apod?date=2019-03-11&api_key=...
# https://api.nasa.gov/EPIC/api/natural/date/2019-05-30?api_key=DEMO_KEY


import requests
import json

dates = ['2019-03-11', '2006-12-29', '2012-12-28', '2020-02-22', '2007-07-21' ,'2020-12-29', '2020-04-27', '2020-07-21']
api_key = '...'
url = 'https://api.nasa.gov/planetary/apod?'

for date in dates:
    response = requests.get(f'{url}date={date}&api_key={api_key}')
    if response.status_code == 200:
        print('OK')
    else:
        print(response.status_code)
        print(response.content)

    r = response.json()

    print(r)

    filename = f'{date}_nasa.json'
    with open(filename, 'w') as f:
        # преобразуем в json и сохраняем в файл
        json.dump(r, f)

    print(f"Ссылка на фото {r.get('hdurl')}")
