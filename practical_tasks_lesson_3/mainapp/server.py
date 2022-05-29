"""Серверная часть программы."""

import json
import time
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from common.utils import get_response, send_response, \
    get_port_and_address_for_use
from common.variables import CONNECTION_LIMIT, \
    ACTION, ACCOUNT_NAME, USER, TIME, PRESENCE, \
    RESPONSE, ERROR, ALLOWED_USERS

<<<<<<< HEAD
from common.variables import ADDR_LISTEN, PORT_LISTEN
=======
>>>>>>> c5d01734998cdbfe32fc7b0d33f0b0c0bc579a56

def prepare_response(message):
    """
    Подготавливает ответное сообщение
<<<<<<< HEAD
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
    Осуществляет парсинг коммандной строки, поиск номер порта,
    и IP-адреса в параметрах, при их отсутствии возвращает
    значения по умолчанию;
    При наличии ошибок, возбуждает исключение и выводит на
    дисплей текстовое сообщение.
    :return: addr_listen - str: IP-addres
    :return: port_listen - str: port number
    """
    try:
        parser = argparse.ArgumentParser(
            description='Choose and indicate port number in range 1024-65535, '
            'after -p parametr, f.e. -p 8080.'
            'Then indicate IP address after -a parametr f.e. -a 127.0.0.1. '
            'That will be use for socket create. '
            'Default parameters will be choose when this options missing. '
            'Exception and error message returns in case of mistake.'
        )
        parser.add_argument('-p')
        parser.add_argument('-a')
        args = parser.parse_args()
        port_listen = args.p
        addr_listen = args.a
        message_port = f'Используется заданный порт: {port_listen}'
        message_addr = f'Используется заданный IP: {addr_listen}'
        if port_listen is None:
            port_listen = PORT_LISTEN
            message_port = f'Используется порт по умолчанию: {port_listen}'
        if int(port_listen) < 1024 or int(port_listen) > 65535:
            raise ValueError
        if addr_listen is None:
            addr_listen = ADDR_LISTEN
            message_addr = f'Используется IP-адрес по умолчанию: {addr_listen}'
        print(message_addr, message_port, sep='\n')
        
    except ValueError:
        print('Доступны для использования порты в диапазоне от 1024 до 65535.\n'
              'Укажите иное значение порта, или используйте порт по умолчанию')
        sys.exit(1)
    return addr_listen, port_listen
=======
    :param message: dict - сообщение c данными от клиента.
    :return: response: dict - ответное сообщение
    """
    if ACTION in message \
            and message[ACTION] == PRESENCE \
            and TIME in message \
            and USER in message \
            and message[USER][ACCOUNT_NAME] in ALLOWED_USERS:
        return {
            RESPONSE: 200,
            'time': time.ctime(),
            'text': 'Hello client!'
        }
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }
>>>>>>> c5d01734998cdbfe32fc7b0d33f0b0c0bc579a56


def main():
    """
    Агрегация работы функций и запуск программы-сервера.
    """
<<<<<<< HEAD
    c = get_port_and_address_for_use()
    print(c)

    return
=======
    # Анализ параметров коммандной строки
    option = get_port_and_address_for_use(sender='server')
    # Инициализация сокета
    transport = socket(AF_INET, SOCK_STREAM)
    transport.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    transport.bind(option)
    # Режим ожидания входящих сообщений
    transport.listen(CONNECTION_LIMIT)
    while True:
        client, client_address = transport.accept()
        try:
            message_from_client = get_response(client)
            print(message_from_client)
            response = prepare_response(message_from_client)
            send_response(client, response)
            client.close()
        except (ValueError, json.JSONDecodeError):
            print('Получено некорректное сообщение от клиента')
            client.close()
>>>>>>> c5d01734998cdbfe32fc7b0d33f0b0c0bc579a56


if __name__ == '__main__':
    main()
