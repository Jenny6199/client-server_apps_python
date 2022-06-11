"""Клиентская часть программы."""

import sys
from socket import *
import json
import time
import logging
import argparse
import threading
from common.utils import get_response, send_response, get_port_and_address_for_use
from common.variables import ACTION, DESTINATION, PRESENCE, TIME, USER, \
    ACCOUNT_NAME, RESPONSE, ERROR, MESSAGE, MESSAGE_TEXT, \
    SENDER, DEFAULT_IP, PORT_LISTEN, LEAVE_MESSAGE
from common.errors import MessageHasNoResponse, ServerError, ReqFieldMissingError
from decorators.log_deco import debug_log

# Инициализация журнала логирования сервера.
# Имя регистратора должно соответствовать имени в client_log_config.py
CLIENT_LOG = logging.getLogger('client')


@debug_log
def create_exit_message(account_name):
    """
    Функция генерирует сообщение при отключении клиента.
    """
    return {
        ACTION: LEAVE_MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: account_name
    }


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
def message_from_server(sock, username):
    """
    Функция обработчик сообщений полученных от других пользователей.
    При получении корректных данных выводит сообщение на дисплей
    или генерирует исключение и прерывает работу клиента.
    :param sock: dict - сокет
    :param username: str - имя пользователя
    :return None
    """
    while True:
        try:
            message = get_response(sock, sender='client')
            if ACTION in message \
                    and message[ACTION] == MESSAGE \
                    and SENDER in message \
                    and DESTINATION in message \
                    and MESSAGE_TEXT in message \
                    and message[DESTINATION] == username:
                    print(f'\033[104m Получено новое сообщение: \n'
                        f'    от {message[SENDER]}: {message[MESSAGE_TEXT]} \033[0m')
                    CLIENT_LOG.info(f'Получено сообщение от пользователя:'
                                    f'{message[SENDER]}: {message[MESSAGE_TEXT]}')
            else:
                CLIENT_LOG.error(f'\033[091m Получено некорректное сообщение от сервера:'
                                 f'{message} \033[0m')
        except MessageHasNoResponse:
            CLIENT_LOG.error('Получено некорректное сообщение.')
        except (OSError, ConnectionError, ConnectionAbortedError, 
                ConnectionResetError, json.JSONDecodeError):
            CLIENT_LOG.critical('\033[031m Соединение с сервером потеряно. \033[0m')
            break


@debug_log
def create_new_message(sock, account_name='Guest'):
    """
    Функция запрашивает у пользователя данные (получатель сообщения и
    текст сообщения), формирует словарь-сообщение и отправляет сообщение
    на сервер.
    Добавлена возможность выхода из программы по запросу пользователя.
    :param sock: dict - сокет
    :param account_name: str - имя пользователя
    :return None
    """
    # Блок ввода данных
    recipient = input('Укажите получателя сообщения: ')
    print('Введите текст сообщения или quit! для выхода из программы')
    message = input('Текст сообщения: ')
    
    # Возможность выхода из программы по запросу пользователя
    if message == 'quit!':
        sock.close()
        CLIENT_LOG.info(f'Работа завершена по команде пользователя.')
        sys.exit(0)

    # Формирование словаря для отправки
    message_dict = {
        ACTION: MESSAGE,
        SENDER: account_name,
        DESTINATION: recipient,
        TIME: time.time(),
        MESSAGE_TEXT: message
    }
    CLIENT_LOG.debug(f'Сформирован словарь сообщения: {message_dict}')

    # Блок отправки сообщения на сервер.
    try:
        send_response(sock, message_dict, sender='client')
        CLIENT_LOG.info(f'Успешно отправлено сообщение пользователю {recipient}.')
    except Exception as exc:
        print(exc)
        CLIENT_LOG.critical('\033[031m Соединение с сервером разорвано \033[0m')
        sys.exit(1)


@debug_log
def process_response_ans(message):
    """
    Обработчик ответа сервера на сообщение о присутствии.
    Возвращает 200 или генерирует сообщение об ошибке.
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
    parser.add_argument('addr', default=DEFAULT_IP, nargs='?')
    parser.add_argument('port', default=PORT_LISTEN, type=int, nargs='?')
    parser.add_argument('-n', '--name', default=None, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_name = namespace.name

    # Проверка доступности порта
    if not 1023 < server_port < 65536:
        CLIENT_LOG.critical(f'Попытка запуска клиента с неподходящим номером порта: {server_port}.'
                            f'Допустимы адреса с 1024 до 65535. Клиент завершает работу.')
        sys.exit(1)

    return server_address, server_port, client_name


def mainloop():
    """Агрегация работы функций и запуск программы-клиента"""
    
    # Загрузка параметров коммандной строки
    server_address, server_port, client_name = arg_parser()

    # Проверка наличия имени пользователя
    if not client_name:
        client_name = input('Введите имя пользователя: ')

    CLIENT_LOG.info(f'Запущен клиент с параметрами: \n'
                    f'- адрес сервера: {server_address}, \n'
                    f'- порт: {server_port}, \n'
                    f'- имя пользователя: {client_name}.')

    # Титульное сообщение
    print(f'ПРОГРАММА ОБМЕНА СООБЩЕНИЯМИ В КОНСОЛИ. v 0.1.0 \n'
          f'КЛИЕНТ. \n'
          f'ПОЛЬЗОВАТЕЛЬ: {client_name}'
          )
        
    # Инициализация работы сокета
    try:
        transport = socket(AF_INET, SOCK_STREAM)
        transport.connect((server_address, server_port))
        send_response(transport, create_presence_message(client_name), sender='client')
        answer = process_response_ans(get_response(transport, sender='client'))
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
        receiver = threading.Thread(
            target=message_from_server,
            args=(transport, client_name)
            )
        receiver.daemon = True
        receiver.start()

    # Поток запуска процесса отправки сообщений
        transmitter = threading.Thread(
            target=create_new_message,
            args=(transport, client_name)
        )
        transmitter.daemon = True
        transmitter.start()

    CLIENT_LOG.debug('Потоки для отправки/получения сообщений успешно запущены.')

    # Основной цикл клиентской программы
    while True:
        time.sleep(1)
        if receiver.is_alive and transmitter.is_alive:
            continue
        break


if __name__ == '__main__':
    mainloop()
