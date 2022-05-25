"""Серверная часть программы."""

import socket
import json
import sys
import argparse
import time

from common.variables import ADDR, PORT_LISTEN


def get_client_message():
    """
    Принимает сообщение от клиента
    :return:
    """
    pass


def prepare_response():
    """
    Подготавливает ответное сообщение
    :return:
    """
    pass


def send_response():
    """
    Отправляет ответ клиенту
    :return:
    """
    pass


def get_port_for_use():
    """
    Осуществляет парсинг коммандной строки, возвращает номер порта
    или ошибку.
    :return: port_listen - str: port number
    """
    try:
        parser = argparse.ArgumentParser(description='get port number')
        parser.add_argument('-p')
        args = parser.parse_args()
        port_listen = args.p
        message = str(f'Используется заданный порт: {port_listen}')
        if port_listen is None:
            port_listen = PORT_LISTEN
            message = str(f'Используется порт по умолчанию:{port_listen}')
        if int(port_listen) < 1024 or int(port_listen) > 65535:
            raise ValueError
        print(message)
    except ValueError:
        print('Номер порта может быть указано только в диапазоне от 1024 до 65535.')
        sys.exit(1)
    return port_listen


def main():
    """
    Агрегация работы функций и запуск программы-сервера.
    :return:
    """
    get_port_for_use()

    return


if __name__ == '__main__':
    main()
