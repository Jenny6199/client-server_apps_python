"""Серверная часть программы."""

import json
import select
import time
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from common.utils import get_response, send_response, \
    get_port_and_address_for_use
from common.variables import CONNECTION_LIMIT, \
    ACTION, ACCOUNT_NAME, USER, TIME, PRESENCE, \
    RESPONSE, ERROR, ALLOWED_USERS, MESSAGE, MESSAGE_TEXT, SENDER
import logging
import log.server_log_config
from decorators.log_deco import debug_log

# Инициализация журнала логирования сервера.
# Имя регистратора должно соответствовать имени в server_log_config.py
SERVER_LOG = logging.getLogger('server')


@debug_log
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
        SERVER_LOG.debug('Сообщение от клиента корректное')
        return {
            RESPONSE: 200,
            'time': time.ctime(),
            'text': 'Hello client!'
        }
    SERVER_LOG.debug(f'Получено ошибочное сообщение от клиента {message}')
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def process_client_message(message, messages_list, client):
    """Обработчик сообщений"""
    SERVER_LOG.debug(f'Разбор сообщения от клиента: {message}')
    if ACTION in message \
        and message[ACTION] == PRESENCE \
        and TIME in message \
        and USER in message \
        and message[USER][ACCOUNT_NAME] == 'Guest':
        send_response(client, {RESPONSE: 200})
        return
    elif ACTION in message \
        and message[ACTION] == MESSAGE \
        and TIME in message \
        and MESSAGE_TEXT in message:
        messages_list.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))
        return
    else:
        send_response(client, {RESPONSE: 400, ERROR: 'Bad Request'})
        return


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
    transport.settimeout(0.5)
    SERVER_LOG.info(f'Сервер запущен и слушает порт: {option[1]}.')

    # Создаем списки клиентов и очередь сообщений
    clients = []
    messages = []

    # Режим ожидания входящих сообщений
    SERVER_LOG.info('Сервер ожидает входящие сообщения.')
    transport.listen(CONNECTION_LIMIT)
    while True:
        # Устанавливаем обход блокирующего accept через таймаут и исключение
        try:
            client, client_address = transport.accept()
            SERVER_LOG.info(f'Новое подключение: {client_address}')
        except OSError as err:
            # Печатает None если время вышло
            print(err.errno)
            pass
        else:
            SERVER_LOG.info(f'Установлено новое соединение с клиентом {client_address}')
            clients.append(client)
        
        # Создаем списки для Select
        res_data_list, send_data_list, err_data_list = [], [], []

        # Проверяем наличие клиентов ожидающих ответ сервера
        try:
            if clients:
                res_data_list, send_data_list, err_data_list = select.select(clients, clients, [], 0)
        except OSError:
            pass

        # Проверяем наличие входящих сообщений
        if res_data_list:
            for client_with_message in res_data_list:
                try:
                    process_client_message(
                        get_response(client_with_message, sender='server'),
                        messages,
                        client_with_message
                    )
                except:
                    SERVER_LOG.info(
                        f'Клиент {client_with_message.getpeername()} отключился от сервера'
                    )
                    clients.remove(client_with_message)

        if messages and send_data_list:
            message = {
                ACTION: MESSAGE,
                SENDER: messages[0][0],
                TIME: time.time(),
                MESSAGE_TEXT: messages[0][1]
            }
            del messages[0]
            for waiting_client in send_data_list:
                try:
                    send_response(waiting_client, message, sender='server')
                except:
                    SERVER_LOG.info(f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                    waiting_client.close()
                    clients.remove(waiting_client)


if __name__ == '__main__':
    main()
