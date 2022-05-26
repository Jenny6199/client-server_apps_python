""" Общие функции для сервера и клиента"""

import sys
import json
import argparse
from .variables import PACKAGE_SIZE, ENCODING_METHOD, PORT_LISTEN, ADDR_LISTEN, DEFAULT_IP


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
    или содержат ошибку.
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


def get_port_and_address_for_use(sender):
    """
    Осуществляет парсинг коммандной строки, возвращает кортеж с
    содержащий IP-адрес и номер порта. Генерирует ошибку при
    получении ошибочных параметров.
    :return tuple: (str(ip-address), int(port number))
    """
    try:
        parser = argparse.ArgumentParser(
            description='Choose and indicate IP-address and port for server '
                        'listen. In case of options -p or -a is missing '
                        'default settings will be use. Available port in range '
                        '1024-65535. Exception will be generate in case of '
                        'mistake find.'
        )
        parser.add_argument('-p')
        parser.add_argument('-a')
        args = parser.parse_args()
        addr_listen, port_listen = args.a, args.p
        message_port = f'Используется заданный порт: {port_listen}'
        message_addr = f'Используется заданный адрес: {addr_listen}'

        # Порт не указан в параметрах
        if port_listen is None:
            port_listen = PORT_LISTEN
            message_port = f'default_port: {port_listen}'
        if int(port_listen) < 1024 or int(port_listen) > 65535:
            raise ValueError

        # Адрес не указан в параметрах
        if addr_listen is None:
            if sender == 'server':
                addr_listen = ADDR_LISTEN
                message_addr = 'Listen IP-addresses: default'
            else:
                addr_listen = DEFAULT_IP
                message_addr = f'IP-address: {addr_listen}'

    except ValueError:
        print('Номер порта должен быть указан в диапазоне от 1024 до 65535.')
        sys.exit(1)
    print(message_addr, message_port, sep='\n')
    return addr_listen, int(port_listen)
