import json
import sys
import socket
import threading
import time
import logging
from PyQt5.QtCore import pyqtSignal, QObject

from mainapp.common.utils import *
from mainapp.common.variables import *
from mainapp.common.errors import *

logger = logging.getLogger('client')
socket_lock = threading.Lock()


class ClientTransport(threading.Thread, QObject):
    """
     Класс обеспечивающий взаимодействие клиентской и серверной
     частей программы.
    """
    # Signals
    new_message = pyqtSignal(str)
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

    def user_list_update(self):
        pass

    def contact_list_update(self):
        pass

    def create_presence_message(self):
        """
        Формирует приветственное сообщение от клиента
        :return: out: dict - message for server
        """
        out = {
            ACTION: PRESENCE,
            TIME: time.ctime(),
            USER: {
                ACCOUNT_NAME: self.username
            }
        }
        logger.debug(f'Сформировано {PRESENCE} сообщение для пользователя {self.username}.')
        return out


