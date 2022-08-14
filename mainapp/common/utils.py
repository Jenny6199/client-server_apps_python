""" Общие функции для сервера и клиента"""

import sys
import json
import argparse
from .variables import PACKAGE_SIZE, ENCODING_METHOD, \
    PORT_LISTEN, ADDR_LISTEN, DEFAULT_IP
# Загружаем ошибки
from .errors import DictionaryNotReceived, SenderIndicationError, \
    NonBytesMessage, JsonEncodeError, NonStrData, PortNumberError
# Обеспечиваем доступность пути к корню проекта
import os

sys.path.append(os.path.join(os.getcwd(), '..'))
# Загружаем обработчики логов клиента и сервера
import logging
import log.server_log_config
import log.client_log_config
# Загружаем декораторы
from decorators.log_deco import debug_log


def choose_log(sender):
    """
    Вспомогательная функция.
    Принимает источник вызова функции
    и устанавливает адресацию записи логов
    :param - sender: str
    """
    if sender == 'server':
        return logging.getLogger('server')
    elif sender == 'client':
        return logging.getLogger('client')
    else:
        raise SenderIndicationError


@debug_log
def send_response(sock, message, sender):
    """
    Принимает сообщение в виде словаря, осуществляет проверку соответствия.
    Генерирует ошибку в случае несовпадения содержимого.
    Кодирует сообщение в байтовый формат.
    Отправляет сообщение.
    :param - sock: socket
    :param - message: dict
    :param - sender: str
    :return None
    """
    log_aim = choose_log(sender)
    if not isinstance(message, dict):
        log_aim.error(f'Невозможно обработать сообщение {message}')
        raise DictionaryNotReceived
    try:
        json_message = json.dumps(message)
        encoded_message = json_message.encode(ENCODING_METHOD)
    except UnicodeEncodeError:
        log_aim.error(f'Невозможно обработать сообщение {message}')
        raise JsonEncodeError
    sock.send(encoded_message)
    log_aim.info('Сообщение отправлено')
    return


@debug_log
def get_response(client, sender):
    """
    Функция принимает сообщение в байтовом формате,
    Генерирует ValueError если данные получены другом формате
    или содержат ошибку.
    Возращает сообщение в JSON-формате (словарь).

    :return response: dict - json-data.
    """

    log_aim = choose_log(sender)
    log_aim.debug(f'Ожидается сообщение от {sender}')
    encoded_response = client.recv(PACKAGE_SIZE)
    if not isinstance(encoded_response, bytes):
        log_aim.error('Ошибка обработки данных в функции get_response')
        raise NonBytesMessage
    json_response = encoded_response.decode(ENCODING_METHOD)
    if not isinstance(json_response, str):
        log_aim.error('Ошибка обработки данных в функции get_response')
        raise NonStrData
    response = json.loads(json_response)
    if not isinstance(response, dict):
        raise DictionaryNotReceived
    log_aim.info(f'Получены новые данные от {sender}.')
    return response


@debug_log
def get_port_and_address_for_use(sender):
    """
    Осуществляет парсинг коммандной строки, возвращает кортеж с
    содержащий IP-адрес и номер порта. Генерирует ошибку при
    получении ошибочных параметров.
    :return tuple: (str(ip-address), int(port number))
    """
    log_aim = choose_log(sender)
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
        addr_listen, port_listen = args.a, args.p

        # Порт не указан в параметрах
        if port_listen is None:
            port_listen = PORT_LISTEN
        if int(port_listen) < 1024 or int(port_listen) > 65535:
            raise PortNumberError

        # Адрес не указан в параметрах
        if addr_listen is None:
            if sender == 'server':
                addr_listen = ADDR_LISTEN
            else:
                addr_listen = DEFAULT_IP

    except PortNumberError:
        log_aim.error(f'Номер порта должен быть указан в диапазоне от 1024 до 65535. Указано - {port_listen}')
        sys.exit(1)
    return addr_listen, int(port_listen)
