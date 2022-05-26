"""Серверная часть программы."""

from socket import *
from common.utils import get_response, send_response

import json
import sys
import argparse
import time

from common.variables import ADDR_LISTEN, PORT_LISTEN, CONNECTION_LIMIT, \
    ACTION, ACCOUNT_NAME, USER, TIME, PRESENCE, RESPONSE, ERROR


def prepare_response(message):
    """
    Подготавливает ответное сообщение
    :param message: сообщение от клиента.
    :return: response: dict
    """
    if ACTION in message \
            and message[ACTION] == PRESENCE \
            and TIME in message \
            and USER in message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def get_port_and_address_for_use():
    """
    Осуществляет парсинг коммандной строки, возвращает номер порта
    или ошибку.
    :return addr_listen - str: ip-address
    :return: port_listen - str: port number
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
        port_listen = args.p
        addr_listen = args.a
        message_port = f'Используется заданный порт: {port_listen}'
        message_addr = f'Используется заданный адрес: {addr_listen}'
        if port_listen is None:
            port_listen = PORT_LISTEN
            message_port = f'Используется порт по умолчанию: {port_listen}'
        if int(port_listen) < 1024 or int(port_listen) > 65535:
            raise ValueError
        if addr_listen is None:
            addr_listen = ADDR_LISTEN
            message_addr = f'Используется адрес по умолчанию'
        print(message_addr, message_port, sep='\n')
    except ValueError:
        print('Номер порта должен быть указан в диапазоне от 1024 до 65535.')
        sys.exit(1)
    return addr_listen, int(port_listen)


def main():
    """
    Агрегация работы функций и запуск программы-сервера.
    :return:
    """
    # Получаем значения адреса и порта
    server_options = get_port_and_address_for_use()
    # Готовим сокет
    transport = socket(AF_INET, SOCK_STREAM)
    transport.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    transport.bind(server_options)
    # Слушаем порт
    print(f'Ожидание сообщения от {server_options[0]}:{server_options[1]}')
    transport.listen(CONNECTION_LIMIT)

    while True:
        client, client_address = transport.accept()  # socket, address
        try:
            message_from_client = get_response(client)
            print(message_from_client)
            response = prepare_response(message_from_client)
            send_response(client, response)
            client.close()
        except (ValueError, json.JSONDecodeError):
            print('Получено некорректное сообщение от клиента')
            client.close()


if __name__ == '__main__':
    main()
