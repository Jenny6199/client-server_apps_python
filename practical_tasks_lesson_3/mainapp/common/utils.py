""" Общие функции для сервера и клиента"""

import json
from .variables import PACKAGE_SIZE, ENCODING_METHOD


def send_response(sock, message):
    """
    Принимает сообщение в виде словаря, осуществляет проверку соответствия.
    Генерирует ошибку в случае несовпадения содержимого.
    Кодирует сообщение в байтовый формат.
    Отправляет сообщение.
    :param - sock: socket
    :param - message: dict
    """
    if not isinstance(message, dict):
        raise TypeError
    json_message = json.dumps(message)
    encoded_message = json_message.encode(ENCODING_METHOD)
    sock.send(encoded_message)


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
