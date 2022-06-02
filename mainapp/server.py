"""Серверная часть программы."""

import json
import time
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from common.utils import get_response, send_response, \
    get_port_and_address_for_use
from common.variables import CONNECTION_LIMIT, \
    ACTION, ACCOUNT_NAME, USER, TIME, PRESENCE, \
    RESPONSE, ERROR, ALLOWED_USERS
import logging
import log.server_log_config

# Инициализация журнала логирования сервера.
# Имя регистратора должно соответствовать имени в server_log_config.py
SERVER_LOG = logging.getLogger('server')


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
        SERVER_LOG.debug('Получено корректное сообщение от клиента')
        return {
            RESPONSE: 200,
            'time': time.ctime(),
            'text': 'Hello client!'
        }
    SERVER_LOG.debug('Получено ошибочное сообщение от клиента')
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
    SERVER_LOG.debug(f'Запущен сервер ip-адрес: {option[0]}, порт: {option[1]}')
    # Режим ожидания входящих сообщений
    SERVER_LOG.info('Сервер ожидает входящие сообщения.')
    transport.listen(CONNECTION_LIMIT)
    while True:
        client, client_address = transport.accept()
        try:
            message_from_client = get_response(client)
            SERVER_LOG.info(message_from_client)
            response = prepare_response(message_from_client)
            send_response(client, response)
            SERVER_LOG.info('Отправлено сообщение клиенту')
            client.close()
        except (ValueError, json.JSONDecodeError):
            SERVER_LOG.warning('Получено некорректное сообщение от клиента')
            client.close()


if __name__ == '__main__':
    main()
