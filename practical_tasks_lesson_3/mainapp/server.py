"""Серверная часть программы."""

import json
import time
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from common.utils import get_response, send_response, \
    get_port_and_address_for_use
from common.variables import CONNECTION_LIMIT, \
    ACTION, ACCOUNT_NAME, USER, TIME, PRESENCE, \
    RESPONSE, ERROR, ALLOWED_USERS


def prepare_response(message):
    """
    Подготавливает ответное сообщение
    :param message: dict - сообщение c данными от клиента.
    :return: response: dict - ответное сообщение
    """
    if ACTION in message \
            and message[ACTION] == PRESENCE \
            and TIME in message \
            and USER in message \
            and message[USER][ACCOUNT_NAME] in ALLOWED_USERS:
        return {
            RESPONSE: 200,
            'time': time.ctime(),
            'text': 'Hello client!'
        }
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def main():
    """
    Агрегация работы функций и запуск программы-сервера.
    """
    # Анализ параметров коммандной строки
    option = get_port_and_address_for_use(sender='server')
    # Инициализация сокета
    transport = socket(AF_INET, SOCK_STREAM)
    transport.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    transport.bind(option)
    # Режим ожидания входящих сообщений
    transport.listen(CONNECTION_LIMIT)
    while True:
        client, client_address = transport.accept()
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
