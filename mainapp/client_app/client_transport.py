import socket
import threading
import time
import json
from logging import getLogger
from PyQt5.QtCore import pyqtSignal, QObject

from mainapp.common.utils import *
from mainapp.common.variables import *
from mainapp.common.errors import *

logger = getLogger('client')
socket_lock = threading.Lock()


class ClientTransport(threading.Thread, QObject):
    """
     Класс обеспечивающий взаимодействие клиентской и серверной
     частей программы.
    """
    # Signals
    new_message = pyqtSignal(str)
    message_205 = pyqtSignal()
    connection_lost = pyqtSignal()

    def __init__(self, port, ip_address, database, username):
        """constructor of class ClientTransport"""
        # super init
        threading.Thread.__init__(self)
        QObject.__init__(self)

        self.database = database
        self.username = username
        self.transport = None
        self.connection_init(port, ip_address)
        # Обновление списков пользователей и контактов
        try:
            pass
            self.user_list_update()
            self.contact_list_update()
        except OSError as err:
            if err.errno:
                logger.critical(f'Соединение с сервером потеряно.')
                raise ServerError(f'Соединение с сервером потеряно.')
            logger.error('Refresh user_list and contact_list: connection timeout!')
        except json.JSONDecodeError:
            logger.critical('Потеряно соединение с сервером.')
            raise ServerError('Потеряно соединение с сервером.')
        # Transport running flag
        self.running = True

    def connection_init(self, port, ip_address):
        """Функция инициализации соединения с сервером"""
        self.transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.transport.settimeout(5)
        flag_connected = False
        for i in range(5):
            logger.info(f'Попытка соединения № {i+1}')
            try:
                self.transport.connect((ip_address, port))
            except(OSError, ConnectionRefusedError):
                pass
            else:
                flag_connected = True
                break
            time.sleep(1)
        if not flag_connected:
            logger.critical('Не удалось подключиться к серверу!')
            raise ServerError('Не удалось подключиться к серверу!')
        logger.debug('Установлено соединение с сервером')
        try:
            with socket_lock:
                send_response(self.transport, self.create_presence_message(), sender='client')
                self.process_server_answer(get_response(self.transport, sender='client'))
        except (OSError, json.JSONDecodeError):
            logger.critical('Потеряно соединение с сервером!')
            raise ServerError('Потеряно соединение с сервером!')

    def user_list_update(self):
        """
        Обеспечивает обновление таблицы известных пользователей
        """
        logger.debug(f'Запрос списка известных пользователей {self.username}')
        request = {
            ACTION: USERS_REQUEST,
            TIME: time.time(),
            ACCOUNT_NAME: self.username,
        }
        with socket_lock:
            send_response(self.transport, request, sender='client')
            answer = get_response(self.transport, sender='client')
        if RESPONSE in answer and answer[RESPONSE] == 202:
            self.database.add_user(answer[LIST_INFO])
        else:
            logger.error('Не удалось обновить список известных пользователей')

    def contact_list_update(self):
        """
        Обеспечивает обработку запроса на обновление списка контактов
        """
        logger.debug(f'Запрос списка контактов для пользователя {self.username}')
        request = {
            ACTION: CONTACT_LIST,
            TIME: time.time(),
            USER: self.username
        }
        logger.debug(f'Сформирован запрос {request}')
        with socket_lock:
            send_response(self.transport, request, sender='client')
            print(self.transport)
            answer = get_response(self.transport, sender='client')
        logger.debug(f'Получен ответ {answer}')
        if RESPONSE in answer and answer[RESPONSE] == 202:
            try:
                for contact in answer[LIST_INFO]:
                    self.database.add_contact(contact)
            except ERROR as e:
                print('Не удалось добавить контакты в базу данных')
                print(e)
        else:
            logger.error('Не удалось обновить список контактов')

    def send_message(self, destination, message):
        """Обработчик отправки сообщения на сервер"""
        message_dict = {
            ACTION: MESSAGE,
            SENDER: self.username,
            DESTINATION: destination,
            TIME: time.time(),
            MESSAGE_TEXT: message,
        }
        logger.debug(f'Сформирован словарь сообщения: {message_dict}')
        with socket_lock:
            send_response(self.transport, message_dict, sender='client')
            self.process_server_answer(get_response(self.transport))
            logger.info(f'Отправлено сообщение для пользователя  {destination}')

    def create_presence_message(self):
        """
        Формирует приветственное сообщение от клиента
        :return: out: dict - message for server
        """
        out = {
            ACTION: PRESENCE,
            TIME: time.time(),
            USER: {
                ACCOUNT_NAME: self.username
            }
        }
        logger.debug(f'Сформировано {PRESENCE} сообщение для пользователя {self.username}.')
        return out

    def process_server_answer(self, message):
        """
        Обеспечивает обработку сообщения от сервера,
        генерирует исключение при ошибке.
        """
        logger.debug(f'разбор сообщения от сервера: {message}')
        if RESPONSE in message:
            if message[RESPONSE] == 200:
                return
            elif message[RESPONSE] == 400:
                raise ServerError(f'{[ERROR]}')
            else:
                logger.debug(f'Незвестный код подтвержения в ответе сервера: '
                             f'{message[RESPONSE]}'
                             )
                # Если получили сообщение от пользователя, добавляем в базу данных
                # и формируем сигнал о новом сообщении
        elif ACTION in message and \
                message[ACTION] == MESSAGE and \
                SENDER in message and \
                DESTINATION in message and \
                MESSAGE_TEXT in message and \
                message[DESTINATION] == self.username:
            logger.debug(f'Получено сообщение от пользователя '
                         f'{message[SENDER]}: {message[MESSAGE_TEXT]}'
                         )
            self.database.save_message(
                message[SENDER], 'in', message[MESSAGE_TEXT]
            )
            self.new_message.emit(message[SENDER])

    def add_contact(self, contact):
        """Обработчик добавления нового контакта"""
        logger.debug(f' Создание нового контакта {contact}')
        request = {
            ACTION: ADD_CONTACT,
            TIME: time.time(),
            USER: self.username,
            ACCOUNT_NAME: contact,
        }
        with socket_lock:
            send_response(self.transport, request, sender='client')
            self.process_server_answer(get_response(self.username, sender='client'))

    def remove_contact(self, contact):
        """Обработчик удаления контакта"""
        logger.debug(f'Удаление контакта {contact}')
        request = {
            ACTION: REMOVE_CONTACT,
            TIME: time.time(),
            USER: self.username,
            ACCOUNT_NAME: contact
        }
        with socket_lock:
            send_response(self.transport, request, sender='client')
            self.process_server_answer(get_response(self.transport))

    def transport_shutdown(self):
        """Обработчик закрытия сокета"""
        self.running = False
        message = {
            ACTION: EXIT,
            TIME: time.time(),
            ACCOUNT_NAME: self.username
        }
        with socket_lock:
            try:
                send_response(self.transport, message, sender='client')
            except OSError:
                pass
        logger.debug('Сокет закрыт')
        time.sleep(1)
