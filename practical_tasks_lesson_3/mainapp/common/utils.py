""" Общие функции для сервера и клиента"""

import json
from variables import PACKAGE_SIZE, ENCODING_METHOD


def send_response(client, response):
    """
    Отправляет сообщение
    :return:
    """
    return client, response


def get_response(client):
    """
    Функция принимает сообщение в байтовом формате,
    Генерирует ValueError если данные получены другом формате
    или не содержат ошибку.
    Возращает сообщение в JSON-формате (словарь).

    :return response: dict - json-data.
    """
    encoded_response = client.recv(PACKAGE_SIZE)
    if not isinstance(encoded_response, bytes):
        raise ValueError
    json_response = encoded_response.decode(ENCODING_METHOD)
    if not isinstance(json_response, str):
        raise ValueError
    response = json.loads(json_response)
    if not isinstance(response, dict):
        raise ValueError
    return response
