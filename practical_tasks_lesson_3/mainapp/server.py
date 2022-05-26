"""Серверная часть программы."""

import socket
import json
import sys
import argparse
import time

from common.variables import ADDR_LISTEN, PORT_LISTEN


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
        print('Номер порта может быть указано только в диапазоне от 1024 до 65535.')
        sys.exit(1)
    return addr_listen, port_listen


def main():
    """
    Агрегация работы функций и запуск программы-сервера.
    :return:
    """
    ip_addr, port = get_port_and_address_for_use()

    return


if __name__ == '__main__':
    main()
