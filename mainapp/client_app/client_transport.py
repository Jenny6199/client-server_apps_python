import socket
import threading
import time
import json
import hashlib
import hmac
import binascii
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

    def __init__(self, port, ip_address, database, username, passwd, keys):
        """constructor of class ClientTransport"""
        # super init
        threading.Thread.__init__(self)
        QObject.__init__(self)

        # База данных клиента
        self.database = database
        # Имя пользователя
        self.username = username
        # Пароль
        self.password = passwd
        # Ключи доступа
        self.keys = keys
        # Сокет
        self.transport = None
        # Соединение
        self.connection_init(port, ip_address)
        # Обновление списков известных пользователей и список контактов
        try:
            self.user_list_update()
            self.contact_list_update()
        except OSError as err:
            if err.errno:
                logger.critical(f'Соединение с сервером потеряно.')
                logger.error('Не удалось обновить список известных пользователей и список контактов')
                raise ServerError(f'Соединение с сервером потеряно.')
            logger.error('Не удалось обновить список известных пользователей и список контактов')
        except json.JSONDecodeError:
            logger.critical('Потеряно соединение с сервером.')
            logger.error('Не удалось обновить список известных пользователей и список контактов')
            raise ServerError('Потеряно соединение с сервером.')
        # Если все прошло успешно поднимаем флаг запуска транспорта
        self.running = True

    def connection_init(self, port, ip_address):
        """Функция инициализации соединения с сервером"""
        # Инициализация сокета
        self.transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.transport.settimeout(5)
        flag_connected = False
        # Попытки соединения с сервером, в случае успеха поднимает flag_connected,
        # в противном случае вызываем исключение.
        for i in range(5):
            logger.info(f'Попытка соединения № {i + 1}')
            try:
                self.transport.connect((ip_address, port))
            except(OSError, ConnectionRefusedError):
                pass
            else:
                flag_connected = True
                break
            time.sleep(1)
        if not flag_connected:
            logger.critical('Не удалось подключиться к серверу! flag_connected=False')
            raise ServerError('Не удалось подключиться к серверу!')
        logger.debug('Установлено соединение с сервером.')
        # Процедура авторизации
        passwd_bytes = self.password.encode('utf-8')
        salt = self.username.lower().encode('utf-8')
        passwd_hash = hashlib.pbkdf2_hmac('sha512', passwd_bytes, salt, 5000)
        passwd_hash_string = binascii.hexlify(passwd_hash)
        logger.debug(f'Успешно создан хэш пароля {passwd_hash_string}.')

        # Получение публичного ключа.
        public_key = self.keys.publickey().export_key().decode('ascii')

        # Отправка приветственного сообщения на сервер
        try:
            with socket_lock:
                send_response(self.transport, self.create_presence_message(public_key), sender='client')
                server_answer = get_response(self.transport, sender='client')
                logger.debug(f'Ответ сервера на приветственное сообщение - {server_answer}.')
                # Обработка ответа сервера:
                if RESPONSE in server_answer:
                    if server_answer[RESPONSE] == 400:
                        raise ServerError(server_answer[ERROR])
                    elif server_answer[RESPONSE] == 511:
                        # Данный ответ получает при штатном запуске авторизации клиента на сервере
                        data = server_answer[DATA]
                        hash = hmac.new(passwd_hash_string, data.encode('utf-8'), 'MD5')
                        digest = hash.digest()
                        report = RESPONSE_511
                        report[DATA] = binascii.b2a_base64(digest).decode('ascii')
                        send_response(self.transport, report, sender='client')
                        self.process_server_answer(get_response(self.transport, sender='client'))
        except (OSError, json.JSONDecodeError):
            logger.critical('Потеряно соединение с сервером! '
                            'Не обработано приветственное сообщение')
            raise ServerError('Разрыв соединения в процессе авторизации!')

    def user_list_update(self):
        """
        Запрашивает с сервера обновление списка известных пользователей
        """
        request = {
            ACTION: USERS_REQUEST,
            TIME: time.time(),
            ACCOUNT_NAME: self.username,
        }
        logger.debug(f'Сформирован запрос к серверу на обновление списка известных пользователей')
        try:
            with socket_lock:
                send_response(self.transport, request, sender='client')
                answer = get_response(self.transport, sender='client')
        except ERROR as e:
            logger.error(f'не удалось обновить список известных пользователей - {e}')
        if RESPONSE in answer and answer[RESPONSE] == 202:
            self.database.add_user(answer[LIST_INFO])
        else:
            logger.error('Не удалось обновить список известных пользователей')

    def contact_list_update(self):
        """
        Запрашивает список контактов с сервера и добавляет в базу данных клиента.
        """
        request = {
            ACTION: CONTACT_LIST,
            TIME: time.time(),
            USER: self.username
        }
        logger.debug(f'Сформирован запрос к серверу на получение списка контактов {self.username}: - {request}')
        try:
            with socket_lock:
                send_response(self.transport, request, sender='client')
                answer = get_response(self.transport, sender='client')
            logger.debug(f'Получен ответ {answer}')
        except ERROR as e:
            print('Ошибка при обновлении списка контактов')
            logger.warning(f'Не удалось обновить список контактов. {e}')
        if RESPONSE in answer and answer[RESPONSE] == 202:
            try:
                for contact in answer[LIST_INFO]:
                    self.database.add_contact(contact)
            except ERROR as e:
                print('Не удалось добавить контакты в базу данных')
                print(e)
        else:
            logger.error('Не удалось обновить список контактов')

    def key_request(self, user):
        """
        Запрашивает с сервера публичный ключ пользователя.
        :param user: user - имя пользователя для запроса
        :return: None
        """
        logger.debug(f'Вызов функции key_request. Запрос публичного ключа пользователя {user}.')
        request = {
            ACTION: PUBLIC_KEY_REQUEST,
            TIME: time.time(),
            ACCOUNT_NAME: user,
        }
        try:
            with socket_lock:
                send_response(self.transport, request)
                answer = get_response(self.transport, sender='client')
                logger.info(f' Получен ответ от сервера {answer}')
        except ERROR as e:
            logger.error(f'Не удалось получить публичный ключ - {e}.')
        if RESPONSE in answer and answer[RESPONSE] == 511:
            return answer[DATA]
        else:
            logger.error('Ключ собеседника не получен.')

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
            self.process_server_answer(get_response(self.transport, sender='client'))
            logger.info(f'Отправлено сообщение для пользователя  {destination}')

    def create_presence_message(self, public_key):
        """
        Формирует приветственное сообщение от клиента
        :return: out: dict - message for server
        """
        out = {
            ACTION: PRESENCE,
            TIME: time.time(),
            USER: {
                ACCOUNT_NAME: self.username,
                PUBLIC_KEY: public_key
            }
        }
        logger.debug(f'Сформировано {PRESENCE} сообщение '
                     f'для пользователя {self.username}. '
                     f'Pubkey = {public_key}')
        return out

    def process_server_answer(self, message):
        """
        Обеспечивает обработку сообщения от сервера,
        генерирует исключение при ошибке.
        """
        logger.debug(f'разбор сообщения от сервера: {message}')

        # Если в сообщении подтверждение какого-либо запроса.
        if RESPONSE in message:
            if message[RESPONSE] == 200:
                return
            elif message[RESPONSE] == 400:
                raise ServerError(f'{[ERROR]}')
            elif message[RESPONSE] == 205:
                self.user_list_update()
                self.contact_list_update()
                self.message_205.emit()
            else:
                logger.debug(f'Незвестный код подтвержения в ответе сервера: '
                             f'{message[RESPONSE]}')

        # Если получили сообщение от пользователя, добавляем в базу данных
        # и формируем сигнал о новом сообщении
        elif ACTION in message and \
                message[ACTION] == MESSAGE and \
                SENDER in message and \
                DESTINATION in message and \
                MESSAGE_TEXT in message and \
                message[DESTINATION] == self.username:
            logger.debug(f'Получено сообщение от пользователя '
                         f'{message[SENDER]}: {message[MESSAGE_TEXT]}')
            self.database.save_message(message[SENDER], 'in', message[MESSAGE_TEXT])
            self.new_message.emit(message)

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
