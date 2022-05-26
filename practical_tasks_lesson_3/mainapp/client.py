from socket import *
from common.utils import get_response, send_response
from common.variables import ACTION, PRESENCE, TIME, USER, \
    ACCOUNT_NAME, RESPONSE, ERROR, ADDR_LISTEN, PORT_LISTEN

import sys
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
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return out


def parse_server_message(message):
    """
    Осуществляет парсинг сообщения от сервера
    :param message - json словарь с данными.
    :return:
    """
    if RESPONSE not in message:
        raise ValueError
    if message[RESPONSE] == 200:
        return '200: OK'
    return f'400: {message[ERROR]}'


def main():
    """
    Агрегация работы функций и запуск программы-клиента.
    :return:
    """
    pass
