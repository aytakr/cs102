import pandas as pd
import requests
import textwrap

from pandas.io.json import json_normalize
from string import Template
from tqdm import tqdm

import config
import emoji
from stop_words import get_stop_words
import pymorphy2

def get_wall(
    owner_id: str='',
    domain: str='',
    offset: int=0,
    count: int=10,
    filter: str='owner',
    extended: int=0,
    fields: str='',
    v: str='5.103'
) -> pd.DataFrame:
    """
    Возвращает список записей со стены пользователя или сообщества.

    @see: https://vk.com/dev/wall.get

    :param owner_id: Идентификатор пользователя или сообщества, со стены которого необходимо получить записи.
    :param domain: Короткий адрес пользователя или сообщества.
    :param offset: Смещение, необходимое для выборки определенного подмножества записей.
    :param count: Количество записей, которое необходимо получить (0 - все записи).
    :param filter: Определяет, какие типы записей на стене необходимо получить.
    :param extended: 1 — в ответе будут возвращены дополнительные поля profiles и groups, содержащие информацию о пользователях и сообществах.
    :param fields: Список дополнительных полей для профилей и сообществ, которые необходимо вернуть.
    :param v: Версия API.
    """

    code = ("return API.wall.get({" +
        f"'owner_id': '{owner_id}'," +
        f"'domain': '{domain}'," +
        "'offset': 0," +
        "'count': 1,"+
        "'filter': 'owner'," +
        "'extended': '0'," +
        "'fields': ''," +
        "'v': '5.103'" +
    "});""")

    # print(code)
#
#     code = """return API.wall.get({
#     "owner_id": "",
#     f" 'domain': '{domain}'",
#     "offset": 0,
#     "count": 10,
#     "filter": "owner",
#     "extended": 0,
#     "fields": "",
#     "v": "5.103"
# });"""

    response = requests.post(
        url="https://api.vk.com/method/execute",
        data={
            "code": code,
            "access_token": config.VK_CONFIG['access_token'],
            "v": config.VK_CONFIG['version']
        }
    )
    return response.json()['response']['items']

def unite_texts(text):
    text1 = []
    for i in range(len(text)):
        text1.append(text[i]['text'])

    return text1

def remove_signs(text):
    signs = ['.', ',', '!', '?', '@', '#', '-', '_', '+', '<', '>', '/', '*', ':', ';', '«', '»', '"', '[', ']', '|', '\n' ]
    for i in range(len(signs)):
        text = text.replace(signs[i], '')

    return text

def remove_digits(text):
    digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    for i in range(len(digits)):
        text = text.replace(digits[i], '')

    return text

def remove_emoji(text):
    l = emoji.UNICODE_EMOJI
    emojis = list(emoji.UNICODE_EMOJI.keys())
    for i in range(len(emojis)):
        text = text.replace(emojis[i], '')

    return text

def remove_links(text):
    text = text.split(' ')
    for i in range(len(text)):
        if 'https' in text[i]:
            text[i] = ''
    text = ' '.join(text)

    return text

def remove_stopwords(text):
    stop_words = get_stop_words('ru')
    text = text.split(' ')
    for i in range(len(text)):
        if text[i] in stop_words:
            text[i] = ''
    text = ' '.join(text)

    return text

def normalize(text):
    morph = pymorphy2.MorphAnalyzer()
    text = text.split(' ')
    for i in range(len(text)):
        text[i] = morph.parse(text[i])[0].normal_form
    text = ' '.join(text)

    return text

def prepare_text(domain):
    text = get_wall(domain=domain)
    texts = unite_texts(text)

    for i, text in enumerate(texts):
        text = remove_signs(text)
        text = remove_digits(text)
        text = remove_emoji(text)
        text = remove_links(text)
        text = remove_stopwords(text)
        text = normalize(text)ди

        texts[i] = text

    texts = [text.split() for text in texts]

    return texts
