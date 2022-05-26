"""Клиентская часть программы."""

from socket import *
from common.utils import get_response, send_response, get_port_and_address_for_use
from common.variables import ACTION, PRESENCE, TIME, USER, \
    ACCOUNT_NAME, RESPONSE, ERROR
import json
import time


def make_presence_message(account_name='Guest'):
    """
    Формирует приветственное сообщение от клиента
    :param account_name: string - name of client
    :return: out: dict - message for server
    """
    out = {
        ACTION: PRESENCE,
        TIME: time.ctime(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return out


def exam_server_message(message):
    """
    Осуществляет парсинг сообщения от сервера
    :param message - json словарь с данными.
    :return:
    """
    if RESPONSE not in message:
        raise ValueError
    if message[RESPONSE] == 200:
        return message
    return f'400: {message[ERROR]}'


def get_descriptive_output(message):
    """Обеспечивает аккуратный вывод данных на дисплей"""
    for key, value in message.items():
        print(f'{key}: {value}')


def main():
    """
    Агрегация работы функций и запуск программы-клиента.
    """
    # Анализ параметров коммандной строки
    option = get_port_and_address_for_use(sender='client')

    # Запуск сокета
    transport = socket(AF_INET, SOCK_STREAM)
    transport.connect(option)
    message_for_server = make_presence_message()
    send_response(transport, message_for_server)
    try:
        response = exam_server_message(get_response(transport))
        get_descriptive_output(response)
    except (ValueError, json.JSONDecodeError):
        print('Не удалось обработать сообщение от сервера')


if __name__ == '__main__':
    main()
