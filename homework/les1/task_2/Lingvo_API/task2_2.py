import requests
import json

url_auth = 'https://developers.lingvolive.com/api/v1.1/authenticate'
url_translate = 'https://developers.lingvolive.com/api/v1/Translation'
url_translate_2 = 'https://developers.lingvolive.com/api/v1/Minicard'
api_key = 'Key API'
# выполняем строки кода 81 -83 без переменной token, потом подставляем в переменную token полученное
# значение ключа из файла token.json
# token = ""


# из документации
# POST api/v1.1/authenticate
# Отвечает на POST запрос, в котором содержится заголовок Authorization: Basic {ApiKey}.
# Ключ API для вашего приложения (ApiKey) можно взять на странице приложения
# При успешной аутентификации клиент получает Bearer-токен (формат text/json), который нужно прикладывать
# к последующим запросам в заголовке Authorization. Иначе - сообщение о том, что аутентификация
# не удалась с кодом 401.
# Срок действия токена - сутки. По прошествии суток, либо при получении ошибки 401
# от методов перевода нужно заново вызвать этот метод и получить новый токен.

def generate_auth_token(api_key: str, url_auth: str) -> str:
    """ Return token, str
    :type api_key: str, key
    :type url_auth: str,service url
    """
    headers_auth = {'Authorization': 'Basic ' + api_key}
    auth = requests.post(url=url_auth, headers=headers_auth)
    if auth.status_code == 200:
        current_token = auth.text
        return current_token
    else:
        raise ValueError(f' Error auth: status_code {auth.status_code},text {auth.text}')


# из документации
# GET api/v1/Translation?text={text}&srcLang={srcLang}&dstLang={dstLang}&isCaseSensitive={isCaseSensitive}
# словарный перевод слова или фразы, поиск осуществляется только в указанном направлении.
# Требует HTTP-заголовок с токеном авторизации: "Authorization: Bearer {token}"
# Параметры URI: text (слово или фраза для перевода), тип string, обязательное;
# srcLang (язык с которого переводить) и dstLang (язык на который переводить), unsigned integer, обязательные;
# isCaseSensitive (чувствительность поиска к регистру), дефолт boolean

# GET api/v1/Minicard?text={text}&srcLang={srcLang}&dstLang={dstLang}
# Миникарточка (краткий перевод слова/фразы). Требует HTTP-заголовок с токеном авторизации:
# "Authorization: Bearer {token}". Параметры аналогичны словарному переводу (см. выше)

def translation(current_token: str, url_translate: str, word: str) -> str:
    """
    Function returns translate words en-ru, str
    :param current_token: str, key
    :param url_tr: service url
    :param word: str, word/words who need translate
    :return: translate word/words, str
    """
    headers_translate = {
        'Authorization': 'Bearer ' + current_token
    }
    params = {
        'text': word,
        'srcLang': 1033,  # (En-Ru) 1033→1049 код английский
        'dstLang': 1049  # код русский
    }
    response = requests.get(url_translate, headers=headers_translate, params=params)
    response_2 = requests.get(url_translate_2, headers=headers_translate, params=params)
    # из документации
    # Статус: результат
    # 200: коллекция карточек из словарей лингво
    # 404: не найдены доступные словари для указанного направления
    # 404: не найдено словарных переводов для запрошенного слова
    if response.status_code == 200 and response_2.status_code == 200:
        return response, response_2
    else:
        raise ValueError(f'Error auth: status_code {response.status_code},text {response.content}')


if __name__ == "__main__":
    #  строки кода 81-83 выполняю 1 раз в сутки
    #  token = generate_auth_token(api_key=api_key, url_auth=url_auth)
    #  with open('token.json', 'w') as file:
    #    json.dump(token, file)
    user_answer = input('Введите cлово или фразу для перевода (слова указывайте через пробел):\n>>>').split()
    # фразу преобразуем в список
    en_words = user_answer
    print(en_words)
    for en_word in en_words:
        translate = translation(current_token=token, url_translate=url_translate, word=en_word)
        en_ru_full, en_ru_mini = translate
        en_ru_full = en_ru_full.json()
        en_ru_mini = en_ru_mini.json()
        with open(f'en_ru_full_{en_word}.json', 'w') as file:
            json.dump(en_ru_full, file)
        print(en_ru_mini)
        try:
            value = en_ru_mini['Translation']['Translation']
            print(value)
            with open(f'en_ru_mini_{en_word}.json', 'w') as file:
                json.dump(en_ru_mini, file)
        except TypeError as e:
            if en_ru_mini == 'Incoming request rate exceeded for 50000 chars per day pricing tier':
                raise ValueError('Incoming request rate exceeded for 50000 chars per day pricing tier')
            else:
                print(f'{e}. No translation available')
# интерпретация Translation, список полей
# Title	(Заголовок словарной статьи), string
# TitleMarkup (Разметка заголовка. Может использоваться, например, для расстановки ударений), Коллекция ArticleNode
# Dictionary (Словарь, к которому относится данная словарная статья), string
# ArticleId (Идентификатор статьи), string
# Body (Тело статьи), Коллекция ArticleNode

# Миникарточка Lingvo. Содержит краткий перевод заголовка и предложения посмотреть что-то другое.
# SourceLanguage (Исходный язык),unsigned integer
# TargetLanguage (целевой язык), unsigned integer
# Heading Заголовок, string
# Translation Перевод. WordListItem
# SeeAlso Список рекомендаций. Коллекция string
