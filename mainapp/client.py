"""
Консольный мессенджер
Клиентская часть программы. v 0.1.0
Программа выполнена в рамках учебного курса
'Клиент-серверные приложения. Python', Geekbrains.
Преподаватель: Илья Барбылев.
Автор: Максим Сапунов, Jenny6199@yandex.ru
Москва, 2022
"""

import art
import sys
from socket import *
import json
import time
import logging
import argparse
import threading
from common.utils import get_response, send_response
from common.variables import ACTION, DESTINATION, PRESENCE, TIME, USER, \
    ACCOUNT_NAME, RESPONSE, ERROR, MESSAGE, MESSAGE_TEXT, \
    SENDER, DEFAULT_IP, PORT_LISTEN, LEAVE_MESSAGE, WHOS_HERE
from common.errors import MessageHasNoResponse, ServerError, ReqFieldMissingError
from decorators.log_deco import debug_log
from metaclasses.client_metaclass import ClientChecker


# Инициализация журнала логирования сервера.
# Имя регистратора должно соответствовать имени в client_log_config.py
CLIENT_LOG = logging.getLogger('client')


def print_help():
    """Функция выводящяя справку по использованию"""
    print('Поддерживаемые команды:')
    print('message - отправить сообщение. Кому и текст будет запрошены отдельно.')
    print('show users online - показать список активных пользователей.')
    print('help - вывести подсказки по командам')
    print('exit - выход из программы')


class ClientSendMessage(threading.Thread, metaclass=ClientChecker):
    def __init__(self, account_name, sock):
        self.account_name = account_name
        self.sock = sock
        super().__init__()

    # @debug_log
    def create_exit_message(self):
        """
        Функция генерирует сообщение при отключении клиента.
        :return - dict - словарь для передачи серверу сигнала о выходе клиента.
        """
        return {
            ACTION: LEAVE_MESSAGE,
            TIME: time.time(),
            ACCOUNT_NAME: self.account_name
        }

    # @debug_log
    def create_new_message(self):
        """
        Функция запрашивает у пользователя данные (получатель сообщения и
        текст сообщения), формирует словарь-сообщение и отправляет сообщение
        на сервер.
        Добавлена возможность выхода из программы по запросу пользователя.
        :return None
        """
        # Блок ввода данных
        recipient = input('Укажите получателя сообщения: ')
        print('Введите текст сообщения или quit! для выхода из программы')
        message = input('Текст сообщения: ')

        # Возможность выхода из программы по запросу пользователя
        if message == 'quit!':
            self.sock.close()
            CLIENT_LOG.info(f'Работа завершена по команде пользователя.')
            sys.exit(0)

        # Формирование словаря для отправки
        message_dict = {
            ACTION: MESSAGE,
            SENDER: self.account_name,
            DESTINATION: recipient,
            TIME: time.time(),
            MESSAGE_TEXT: message
        }
        CLIENT_LOG.debug(f'Сформирован словарь сообщения: {message_dict}')

        # Блок отправки сообщения на сервер.
        try:
            send_response(self.sock, message_dict, sender='client')
            CLIENT_LOG.info(f'Успешно отправлено сообщение пользователю {recipient}.')
        except Exception as exc:
            print(exc)
            CLIENT_LOG.critical('Соединение с сервером разорвано')
            sys.exit(1)

    # @debug_log
    def create_whos_online_message(self):
        out = {
            ACTION: WHOS_HERE,
            TIME: time.ctime(),
            USER: {
                ACCOUNT_NAME: self.account_name
            }
        }
        return out

    # def user_interactive(self):
    def run(self):
        """
        Функция для взаимодействия с пользователем.
        Реализует запрос команд в цикле, обеспечивает
        минимально необходимый функционал.
        :param - sock - socket
        :param - client_name - str
        :return - None
        """
        print_help()
        while True:
            command = input('Введите команду: ')

            if command == 'message':
                self.create_new_message()
                CLIENT_LOG.debug('Запрос на ввод нового сообщения')

            elif command == 'help':
                print_help()
                CLIENT_LOG.debug('Запрос помощи')

            elif command == 'show users online':
                send_response(self.sock, self.create_whos_online_message(), sender='client')
                CLIENT_LOG.debug('Запрос списка пользователей')

            elif command == 'exit':
                send_response(self.sock, self.create_exit_message(), sender='client')
                print('Завершение работы клиента')
                CLIENT_LOG.debug('Завершение работы клиента по команде пользователя')
                time.sleep(0.5)
                break

            else:
                print(f'Введена неизвестная команда "{command}". Попробуйте еще раз. '
                      '(help - посмотреть список доступных комманд).')
        sys.exit(0)


class ClientReadMessage(threading.Thread, metaclass=ClientChecker):
    def __init__(self, account_name, sock):
        self.account_name = account_name
        self.sock = sock
        super().__init__()

    # @debug_log
    # def message_from_server(self, *args, **kwargs):
    def run(self):
        """
        Функция обработчик сообщений полученных от других пользователей.
        При получении корректных данных выводит сообщение на дисплей
        или генерирует исключение и прерывает работу клиента.
        :return None
        """
        while True:
            try:
                message = get_response(self.sock, sender='client')
                print(message)
                if ACTION in message \
                        and message[ACTION] == MESSAGE \
                        and SENDER in message \
                        and DESTINATION in message \
                        and MESSAGE_TEXT in message \
                        and message[DESTINATION] == self.account_name:
                    print(f'\n[!] Получено новое сообщение '
                          f'от {message[SENDER]}: \n - {message[MESSAGE_TEXT]} \n'
                          f'Введите команду: ')
                    CLIENT_LOG.info(f'Получено сообщение от пользователя '
                                    f'{message[SENDER]}: {message[MESSAGE_TEXT]}')
                    continue
                elif ACTION in message \
                        and message[ACTION] == WHOS_HERE:
                    print(f'\n[*] Ответ сервера: в чате доступны клиенты: '
                          f'{message[MESSAGE_TEXT]} \n'
                          f'Введите команду: ')
                    CLIENT_LOG.info(f'Сервер вернул список клиентов {message[MESSAGE_TEXT]}')
                    continue
                else:
                    CLIENT_LOG.error(f'Получено некорректное сообщение от сервера:'
                                     f'{message}')
            except MessageHasNoResponse:
                CLIENT_LOG.error('Получено некорректное сообщение.')
            except (OSError, ConnectionError, ConnectionAbortedError,
                    ConnectionResetError, json.JSONDecodeError):
                CLIENT_LOG.critical('Соединение с сервером потеряно.')
                break
            except Exception as err:
                print('Что-то пошло не так :( попробуйте перезапустить клиент')
                CLIENT_LOG.error(f'Неожиданная ошибка: {err}')
                break


@debug_log
def create_presence_message(account_name='Guest'):
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
    CLIENT_LOG.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}.')
    return out


@debug_log
def exam_server_message(message):
    """
    Осуществляет парсинг сообщения от сервера
    :param message - json словарь с данными.
    :return:  - возвращает корректное сообщение от сервера или 
                генерирует исключение.
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
def process_response_ans(message):
    """
    Обработчик ответа сервера на сообщение о присутствии.
    Возвращает 200 или генерирует сообщение об ошибке.
    :param - message - dict
    :return '200:OK' or raise
    """
    CLIENT_LOG.debug(f'Разбор приветственного сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200:OK'
        elif message[RESPONSE] == 400:
            raise ServerError(f'400: {message[ERROR]}')
    raise ReqFieldMissingError(RESPONSE)


@debug_log
def arg_parser():
    """Парсер аргументов коммандной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', default=DEFAULT_IP, nargs='?')
    parser.add_argument('-p', default=PORT_LISTEN, type=int, nargs='?')
    parser.add_argument('-n', default=None, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.a
    server_port = namespace.p
    client_name = namespace.n

    # Проверка доступности порта
    if not 1023 < server_port < 65536:
        CLIENT_LOG.critical(f'Попытка запуска клиента с неподходящим номером порта: {server_port}.'
                            f'Допустимы адреса с 1024 до 65535. Клиент завершает работу.')
        sys.exit(1)

    return server_address, server_port, client_name


def banner(client_name):
    """
    Выводит на экран приветственное сообщение при запуске клиента.
    :param client_name :str - имя клиента
    :return - None
    """
    art.tprint('...Hello world...', font='doom')
    print(f'ПРОГРАММА ОБМЕНА СООБЩЕНИЯМИ В КОНСОЛИ. \n'
          f'КЛИЕНТ. v 0.1.0 (06.2022) \n'
          f'Пользователь - {client_name}. \n'
          f'Связь с разработчиком - Jenny6199@yandex.ru \n'
          )


def main():
    """Агрегация работы функций и запуск программы-клиента"""

    # Загрузка параметров коммандной строки
    server_address, server_port, client_name = arg_parser()

    # Проверка наличия имени пользователя
    if not client_name:
        client_name = input('Введите имя пользователя: ')

    # Заставка
    banner(client_name)

    CLIENT_LOG.info(f'Запущен клиент с параметрами: '
                    f'адрес сервера - {server_address}, '
                    f'порт - {server_port}, '
                    f'имя пользователя - {client_name}.')

    # Инициализация работы сокета
    try:
        transport = socket(AF_INET, SOCK_STREAM)
        transport.connect((server_address, server_port))
        send_response(transport, create_presence_message(client_name), sender='client')
        answer = exam_server_message(get_response(transport, sender='client'))
        CLIENT_LOG.info(f'Установлено соединение с сервером. Получен ответ: {answer}')
    except ServerError as err:
        CLIENT_LOG.error(f'При установке соединения сервер вернул ошибку: {err.text}')
        sys.exit(1)
    except json.JSONDecodeError:
        CLIENT_LOG.error('Не удалось декодировать JSON.')
        sys.exit(1)
    except ReqFieldMissingError as missing_error:
        CLIENT_LOG.error(f'В ответе сервера отсутствуют необходимые поля: {missing_error.missing_field}')
        sys.exit(1)
    except ConnectionResetError:
        CLIENT_LOG.critical(f'Не удалось подключиться к серверу: {server_address}:{server_port}'
                            f'Конечный компьютер отверг запрос на подключение.')
        sys.exit(1)

    # После успешного подключения формируем потоки
    else:

        # Поток запуска процесса приема сообщений
        # receiver = threading.Thread(
        #     name='receiver_thread',
        #     target=ClientReadMessage.message_from_server,
        #     args=(transport, client_name)
        # )
        receiver = ClientReadMessage(client_name, transport)
        receiver.daemon = True
        receiver.start()
        CLIENT_LOG.debug(f'Поток для получения сообщений  для клиента {client_name} успешно запущен.')

        # Поток запуска процесса отправки сообщений
        # transmitter = threading.Thread(
        #     name='transmitter_thread',
        #     target=ClientSendMessage.user_interactive,
        #     args=(transport, client_name)
        #     )
        transmitter = ClientSendMessage(client_name, transport)
        transmitter.daemon = True
        transmitter.start()
        CLIENT_LOG.debug(f'Поток для отправки сообщений для клиента {client_name} успешно запущен.')

    # Основной цикл клиентской программы
    while True:
        time.sleep(1)
        if receiver.is_alive and transmitter.is_alive:
            continue
        break


if __name__ == '__main__':
    main()
