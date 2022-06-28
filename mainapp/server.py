"""
Консольный мессенджер
Серверная часть программы. v 0.1.0
Программа выполнена в рамках учебного курса
'Клиент-серверные приложения. Python', Geekbrains.
Преподаватель: Илья Барбылев.
Автор: Максим Сапунов, Jenny6199@yandex.ru
Москва, 2022
"""

import select
import time
import art
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from common.utils import get_response, send_response, \
    get_port_and_address_for_use
from common.variables import CONNECTION_LIMIT, \
    ACTION, ACCOUNT_NAME, USER, TIME, PRESENCE, \
    RESPONSE, ERROR, ALLOWED_USERS, MESSAGE, MESSAGE_TEXT, \
    SENDER, LEAVE_MESSAGE, DESTINATION, RSP_200, RSP_400, WHOS_HERE
import logging
from decorators.log_deco import debug_log

# Инициализация журнала логирования сервера.
SERVER_LOG = logging.getLogger('server')


def show_active_users(clients_list=[]):
    """
    Формирует ответное сообщение со списком активных пользователей
    """
    SERVER_LOG.debug(f'Готовим список активных пользователей " {clients_list}".')
    out = {
        ACTION: WHOS_HERE,
        MESSAGE_TEXT: clients_list
    }
    return out


@debug_log
def process_client_message(message, messages_list, client, clients, names):
    """
    Функция обработчик сообщений полученных от клиента
    На вход принимает словарь - проверяет соответствие форме,
    отправляет ответ клиенту при получении приветственного сообщения или ошибке
    добавляет сообщение в список сообщений
    возвращает None
    :param message: data from client
    :param messages_list: list of data
    :param client: object of client
    :param clients: list of clients
    :param names: clients account_name's list.
    """
    SERVER_LOG.debug(f'Разбор сообщения от клиента: {message}')

    # Получено приветственное сообщение.
    if ACTION in message \
            and message[ACTION] == PRESENCE \
            and TIME in message \
            and USER in message:
        SERVER_LOG.debug('Получено приветственное сообщение.')
        # Проверка регистрации клиента
        if message[USER][ACCOUNT_NAME] not in names.keys():
            names[message[USER][ACCOUNT_NAME]] = client
            response = RSP_200
            SERVER_LOG.debug('Ответ клиенту - 200:OK')
        else:
            response = RSP_400
            response[ERROR] = 'Пользователь с таким именем уже существует'
            SERVER_LOG.debug('Ответ клиенту - 400: пользователь уже существует')
        send_response(client, response, sender='server')
        return

    # Получен запрос об активных участниках
    elif ACTION in message \
            and message[ACTION] == WHOS_HERE \
            and TIME in message \
            and USER in message:
        SERVER_LOG.debug(
            f'Получен запрос от {message[USER]} о пользователях on-line'
            )
        user_list = ', '.join(names.keys())
        response = show_active_users(user_list)
        try:
            send_response(client, response, sender='server')
            SERVER_LOG.debug(f'Ответное сообщение со списком активных '
                    f'пользователей успешно отправлено клиенту '
                    f'{message[USER]}')
        except Exception as exc:
            SERVER_LOG.error(
                'Не удалось отправить ответное сообщение клиенту'
                )
        return

    # Получено текстовое сообщение.
    elif ACTION in message \
            and message[ACTION] == MESSAGE \
            and TIME in message \
            and DESTINATION in message:
        SERVER_LOG.debug('Получено текстовое сообщение.')
        messages_list.append(message)
        SERVER_LOG.debug('Сообщение добавлено в список сообщений')
        return

    # Получено сообщение о выходе клиента.
    elif ACTION in message \
            and message[ACTION] == LEAVE_MESSAGE \
            and ACCOUNT_NAME in message:
        SERVER_LOG.debug('Получено сообщение о выходе клиента.')
        clients.remove(names[message[ACCOUNT_NAME]])
        names[message[ACCOUNT_NAME]].close()
        del names[message[ACCOUNT_NAME]]
        SERVER_LOG.debug(f'Клиент {message[ACCOUNT_NAME]} завершил работу.')
        return

    # Получено некорректное сообщение
    else:
        send_response(client, {RESPONSE: 400, ERROR: 'Bad Request'}, sender='server')
        SERVER_LOG.debug('Ответ клиенту - 400:Bad Request')
        return


@debug_log
def process_message(message, names, listen_socks):
    """
    Функция для отправки сообщения конкретному клиенту
    Принимает словарь с сообщением, список пользователей, список сокетов.
    Возвращает None.
    :param message: dict - message
    :param names: list - clients' list
    :param listen_socks: list - sockets' list
    :return: None
    """
    if message[DESTINATION] in names \
            and names[message[DESTINATION]] in listen_socks:
        send_response(names[message[DESTINATION]], message, sender='server')
        SERVER_LOG.info(f'Отправлено сообщение от {message[DESTINATION]} '
                        f'пользователю {message[SENDER]}')
    elif message[DESTINATION] in names \
            and names[message[DESTINATION]] not in listen_socks:
        raise ConnectionError
    else:
        SERVER_LOG.error(
            f'!!! {message[DESTINATION]} - данный клиент не зарегистрирован. '
            f'Сообщение не было отправлено.'
        )


def banner():
    """
    Выводит на экран приветственное сообщение при запуске сервера
    """
    art.tprint('...Hello world...', font='doom')
    print('ПРОГРАММА ОБМЕНА СООБЩЕНИЯМИ В КОНСОЛИ. \n'
          'СЕРВЕР. v 0.1.0 (06.2022) \n'
          'Связь с разработчиком - Jenny6199@yandex.ru \n' 
    )


def main():
    """
    Агрегация работы функций и запуск программы-сервера.
    """
    # Заставка
    banner()

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

    #  Словарь для хранения имен пользователей и соответствующих сокетов
    names = {}

    # Режим ожидания входящих сообщений
    SERVER_LOG.info('Сервер ожидает входящие сообщения.')
    transport.listen(CONNECTION_LIMIT)

    # Основной цикл серверной части программы.
    while True:
        # Устанавливаем обход блокирующего accept через таймаут и исключение
        try:
            client, client_address = transport.accept()
            SERVER_LOG.info(f'Новое подключение: {client_address}')
        except OSError as err:
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
            print('error')

        # Проверяем наличие входящих сообщений
        if res_data_list:
            for client_with_message in res_data_list:
                try:
                    process_client_message(
                        get_response(client_with_message, sender='server'),
                        messages,
                        client_with_message,
                        clients,
                        names
                    )
                except Exception as err:
                    print(err)
                    SERVER_LOG.info(
                        f'Клиент {client_with_message.getpeername()} отключился от сервера')
                    clients.remove(client_with_message)

        for mail in messages:
            try:
                process_message(mail, names, send_data_list)
            except Exception:
                SERVER_LOG.info(f'Не удалось отправить сообщение клиенту {mail[DESTINATION]}.')
                clients.remove(names[mail[DESTINATION]])
                del names[mail[DESTINATION]]
        messages.clear()


if __name__ == '__main__':
    main()
