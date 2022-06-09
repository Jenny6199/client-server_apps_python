"""Клиентская часть программы."""
import sys
from socket import *
from common.utils import get_response, send_response, get_port_and_address_for_use
from common.variables import ACTION, PRESENCE, TIME, USER, \
    ACCOUNT_NAME, RESPONSE, ERROR, MESSAGE, MESSAGE_TEXT, SENDER
import json
import time
import logging
import log.client_log_config
from common.errors import MessageHasNoResponse
from decorators.log_deco import debug_log

# Инициализация журнала логирования сервера.
# Имя регистратора должно соответствовать имени в client_log_config.py
CLIENT_LOG = logging.getLogger('client')


@debug_log
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


@debug_log
def exam_server_message(message):
    """
    Осуществляет парсинг сообщения от сервера
    :param message - json словарь с данными.
    :return:
    """
    if RESPONSE not in message:
        CLIENT_LOG.warning(f'Получены ошибочные данные: {message}')
        raise MessageHasNoResponse
    if message[RESPONSE] == 200:
        return message
    elif message[RESPONSE] == 403:
        raise ConnectionError
    else:
        return f'400: {message[ERROR]}'


@debug_log
def get_descriptive_output(message):
    """Обеспечивает аккуратный вывод данных на дисплей"""
    for key, value in message.items():
        print(f'{key}: {value}')


@debug_log
def message_from_server(message):
    """Обработчик"""
    if ACTION in message \
            and message[ACTION] == MESSAGE \
            and SENDER in message \
            and MESSAGE_TEXT in message:
        print(f'Получено сообщение от пользователя: '
              f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
        CLIENT_LOG.info(f'Получено сообщение от пользователя:'
                        f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
    else:
        CLIENT_LOG.error(f'Получено некорректное сообщение от сервера:'
                         f'{message}')


@debug_log
def create_message(sock, account_name='Guest'):
    """Запрашивает текст сообщения"""
    print('Введите сообщение или quit для выхода из программы:')
    message = input('Текст сообщения: ')
    if message == 'quit':
        sock.close()
        CLIENT_LOG(f'Работа завершена по команде пользователя.')
        sys.exit(0)
    message_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: account_name,
        MESSAGE_TEXT: message
    }
    LOGGER.debug(f'Сформирован словарь сообщения: {message_dict}')
    return message_dict


@debug_log
def process_response_ans(message):
    """Обработчик"""
    pass


def main():
    """
    Агрегация работы функций и запуск программы-клиента.
    """
    # Анализ параметров коммандной строки
    option = get_port_and_address_for_use(sender='client')

    # Запуск сокета
    transport = socket(AF_INET, SOCK_STREAM)
    try:
        transport.connect(option)
    except ConnectionRefusedError:
        CLIENT_LOG.warning('Невозможно установить соединение - удаленный сервер не отвечает.')
        sys.exit(1)
    CLIENT_LOG.info(f'Установлено соединение (ip: {option[0]}, port: {option[1]})')
    message_for_server = make_presence_message()
    send_response(transport, message_for_server, 'client')
    try:
        response = exam_server_message(get_response(transport, 'client'))
        get_descriptive_output(response)
    except (ValueError, json.JSONDecodeError):
        CLIENT_LOG.warning('Не удалось обработать сообщение от сервера.')
    except ConnectionResetError:
        CLIENT_LOG.warning('Удаленный сервер разорвал соединение.')
        sys.exit(1)


if __name__ == '__main__':
    main()
