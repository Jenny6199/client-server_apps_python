# Консольный мессенджер
# Серверная часть программы. v 0.2.0
# Продолжение работы над проектом на курсе
# "Базы данных и PyQt", Geekbrains
# Преподаватель: Илья Барбылев.
# Автор: Максим Сапунов, Jenny6199@yandex.ru
# Москва, 2022

import argparse
import sys
import select
import art
from os import path
import threading
from common.errors import IncorrectDataRecivedError
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from common.utils import get_response, send_response
from common.variables import CONNECTION_LIMIT, PORT_LISTEN, \
    ACTION, ACCOUNT_NAME, USER, TIME, PRESENCE, \
    RESPONSE, ERROR, MESSAGE, MESSAGE_TEXT, \
    SENDER, LEAVE_MESSAGE, DESTINATION, RSP_200, RSP_400, WHOS_HERE
import logging
from decorators.log_deco import debug_log
from metaclasses.server_metaclass import ServerChecker
from descriptors.port_descr import Port
from db_builder.server_data_base import ServerDB

# Инициализация журнала логирования сервера.
SERVER_LOG = logging.getLogger('server')


def arg_parser():
    """command line parser"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=PORT_LISTEN, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p
    return listen_address, listen_port


def banner():
    """
    Выводит на экран приветственное сообщение при запуске сервера
    """
    art.tprint('...Hello world...', font='doom')
    print('ПРОГРАММА ОБМЕНА СООБЩЕНИЯМИ В КОНСОЛИ. \n'
          'СЕРВЕР. v 0.2.1 (08.2022) \n'
          'Связь с разработчиком - Jenny6199@yandex.ru \n'
          )


def show_active_users(clients_list):
    """
    Формирует ответное сообщение со списком активных пользователей
    """
    SERVER_LOG.debug(f'Готовим список активных пользователей " {clients_list}".')
    out = {
        ACTION: WHOS_HERE,
        MESSAGE_TEXT: clients_list
    }
    return out


class Server(threading.Thread, metaclass=ServerChecker):
    port = Port()

    def __init__(self, listen_address, listen_port):
        """Конструктор класса Server"""
        self.addr = listen_address
        self.port = listen_port
        self.clients = []
        self.messages = []
        self.names = dict()
        self.sock = None
        # Thread
        super().__init__()

    def init_socket(self):
        """Функция для инициализации сокета"""
        try:
            transport = socket(AF_INET, SOCK_STREAM)
            transport.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            transport.bind((self.addr, self.port))
            transport.settimeout(0.5)

            self.sock = transport
            self.sock.listen(CONNECTION_LIMIT)

            SERVER_LOG.info(
                f'Запущен сервер, порт для подключений {self.port}. '
                f'Адрес для входящих подключений {self.addr}. '
                f'Если адрес не указан, принимаются соединения с любых адресов. '
                f'Сервер ожидает входящие сообщения.'
            )
        except Exception as e:
            SERVER_LOG.critical(f'Не удалось инициализировать сокет! {e}')

    def run(self):
        """Функция осуществляет запуск и  поддерживает основной цикл работы сервера"""
        banner()
        self.init_socket()
        while True:
            try:
                client, client_address = self.sock.accept()
            except OSError:
                pass
            else:
                SERVER_LOG.info(f'Новое подключение: {client_address}')
                self.clients.append(client)

            # Создаем списки для Select
            res_data_list, send_data_list, err_data_list = [], [], []

            # Проверка ожидающих клиентов
            try:
                if self.clients:
                    res_data_list, send_data_list, err_data_list = select.select(self.clients, self.clients, [], 0)
            except OSError:
                SERVER_LOG.debug('Исключение при проверке ожидающих клиентов')
                pass

            # Принимаем сообщения, обрабатываем исключения
            if res_data_list:
                for client_with_message in res_data_list:
                    try:
                        self.process_client_message(
                            get_response(client_with_message, sender='server'),
                            self.messages,
                            client_with_message,
                            self.clients,
                            self.names
                            )
                    except TimeoutError:
                        SERVER_LOG.info(
                            f'Клиент {client_with_message.getpeername()} отключился от сервера')
                        self.clients.remove(client_with_message)

            # Обрабатываем сообщения
            for mail in self.messages:
                try:
                    self.process_message(mail, self.names, send_data_list)
                except ConnectionError:
                    SERVER_LOG.info(f'Не удалось отправить сообщение клиенту {mail[DESTINATION]}.')
                    self.clients.remove(self.names[mail[DESTINATION]])
                    del self.names[mail[DESTINATION]]
            self.messages.clear()

    @debug_log
    def process_client_message(self, message, messages_list, client, clients, names):
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
                    f'Не удалось отправить ответное сообщение клиенту: {exc}'
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
    def process_message(self, message, names, listen_socks):
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


def print_help():
    print('Поддерживаемые комманды:')
    print('users - список известных пользователей')
    print('connected - список подключённых пользователей')
    print('loghist - история входов пользователя')
    print('exit - завершение работы сервера.')
    print('help - вывод справки по поддерживаемым командам')


def main():
    # Загрузка параметров коммандной строки
    listen_address, listen_port = arg_parser()

    # Создание базы данных
    database = ServerDB()

    # Создается экземпляр класса сервера и запускается в потоке
    server = Server(listen_address, listen_port)
    server.daemon = True
    server.start()

    while True:
        command = input('Введите команду: ')
        if command == 'help':
            print_help()
        elif command == 'exit':
            break
        elif command == 'users':
            for user in sorted(database.users_list()):
                print(f'Пользователь {user[0]}, последний вход: {user[1]}')
        elif command == 'connected':
            for user in sorted(database.active_users_list()):
                print(f'Пользователь {user[0]}, подключен: {user[1]}:{user[2]}, время установки соединения: {user[3]}')
        elif command == 'loghist':
            name = input('Введите имя пользователя для просмотра истории. '
                         'Для вывода всей истории, просто нажмите Enter: ')
            for user in sorted(database.login_history(name)):
                print(f'Пользователь: {user[0]} время входа: {user[1]}. Вход с: {user[2]}:{user[3]}')
        else:
            print('Команда не распознана.')


if __name__ == '__main__':
    main()
