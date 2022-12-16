import threading
import logging
import select
import socket
import json
import hmac
import binascii
import os
# from mainapp.metaclasses.server_metaclass import ServerVerifier
# from mainapp.descriptors.port_descr import PortDescriptor
from mainapp.common.variables import *
from mainapp.common.utils import send_response, get_response
from mainapp.decorators.log_deco import debug_log

SERVER_LOG = logging.getLogger('server')


class MessageProcessor(threading.Thread):
    """
    Основной класс сервера. Обеспечивает прием и обработку поступающих
    сообщений. Запускается в отдельном потоке.
    """

    def __init__(self, listen_address, listen_port, database):
        self.addr = listen_address
        self.port = listen_port
        self.database = database
        self.sock = None
        self.clients = []
        self.listen_sockets = None
        self.error_sockets = None
        self.running = True
        self.names = dict()
        super().__init__()

    def autorize_user(self, message, sock):
        """
        Метод реализующий авторизцию пользователей.
        """
        # Если имя пользователя занять --> 400
        SERVER_LOG.debug(f'Start auth process for {message[USER]}')
        if message[USER][ACCOUNT_NAME] in self.names.keys():
            response = RSP_400
            response[ERROR] = 'Имя пользователя уже занято.'
            try:
                SERVER_LOG.debug(f'Username busy, sending {response}')
                send_response(sock, response, sender='server')
            except OSError:
                SERVER_LOG.debug('OS Error')
                pass
            self.clients.remove(sock)
            sock.close()
        # Проверяем что пользователь зарегистрирован на сервере.
        elif not self.database.check_user(message[USER][ACCOUNT_NAME]):
            response = RSP_400
            response[ERROR] = 'Пользователь не зарегистрирован.'
            try:
                SERVER_LOG.debug(f'Неизвестное имя пользователя - {response}')
                send_response(sock, response, sender='server')
            except OSError:
                pass
            self.clients.remove(sock)
            sock.close()
        else:
            SERVER_LOG.debug('Correct username, starting passwd check.')
            # Иначе отвечаем 511 и проводим процедуру авторизации
            # Словарь - заготовка
            message_auth = RESPONSE_511
            # Набор байтов в hex представлении
            random_str = binascii.hexlify(os.urandom(64))
            # В словарь байты нельзя, декодируем (json.dumps -> TypeError)
            message_auth[DATA] = random_str.decode('ascii')
            # Создаём хэш пароля и связки с рандомной строкой, сохраняем
            # серверную версию ключа
            passwd_hash = hmac.new(self.database.get_hash(message[USER][ACCOUNT_NAME]), random_str, 'MD5')
            digest = passwd_hash.digest()
            SERVER_LOG.debug(f'Auth message = {message_auth}')
            try:
                # Обмен с клиентом
                send_response(sock, message_auth, sender='server')
                ans = get_response(sock, sender='server')
            except OSError as err:
                SERVER_LOG.debug('Error in auth, data:', exc_info=err)
                sock.close()
                return
            client_digest = binascii.a2b_base64(ans[DATA])
            # Если ответ клиента корректный, то сохраняем его в список
            # пользователей.
            if RESPONSE in ans and ans[RESPONSE] == 511 and hmac.compare_digest(
                    digest, client_digest):
                self.names[message[USER][ACCOUNT_NAME]] = sock
                client_ip, client_port = sock.getpeername()
                try:
                    send_response(sock, RSP_200, sender='server')
                except OSError:
                    self.remove_client(message[USER][ACCOUNT_NAME])
                # добавляем пользователя в список активных и если у него изменился открытый ключ
                # сохраняем новый
                self.database.user_login(
                    message[USER][ACCOUNT_NAME],
                    client_ip,
                    client_port,
                    message[USER][PUBLIC_KEY])
            else:
                response = RSP_400
                response[ERROR] = 'Неверный пароль.'
                try:
                    send_response(sock, response, sender='server')
                except OSError:
                    pass
                self.clients.remove(sock)
                sock.close()

    def remove_client(self, client):
        """
        Метод обработчик клиента с которым прервана связь.
        Ищет клиента и удаляет его из списков и базы:
        """
        SERVER_LOG.info(f'Клиент {client.getpeername()} отключился от сервера.')
        for name in self.names:
            if self.names[name] == client:
                self.database.user_logout(name)
                del self.names[name]
                break
        self.clients.remove(client)
        client.close()

    def process_message(self, message):
        """
        Метод отправки сообщения клиенту.
        :param - message
        :return - None
        """
        if message[DESTINATION] in self.names \
                and self.names[message[DESTINATION]] in self.listen_sockets:
            try:
                send_response(self.names[message[DESTINATION]], message, sender='server')
                SERVER_LOG.info(f'Отправлено сообщение пользователю '
                                f'{message[DESTINATION]} от пользователя '
                                f'{message[SENDER]}.')
            except OSError:
                self.remove_client(message[DESTINATION])
        elif message[DESTINATION] in self.names and self.names[message[DESTINATION]] not in self.listen_sockets:
            SERVER_LOG.error(
                f'Связь с клиентом {message[DESTINATION]} была потеряна. Соединение закрыто, доставка невозможна.')
            self.remove_client(self.names[message[DESTINATION]])
        else:
            SERVER_LOG.error(
                f'Пользователь {message[DESTINATION]} не зарегистрирован на сервере, отправка сообщения невозможна.')

    @debug_log
    def process_client_message(self, message, client):
        """
        Функция обработчик сообщений полученных от клиента
        На вход принимает словарь - проверяет соответствие форме,
        отправляет ответ клиенту при получении приветственного сообщения или ошибке
        добавляет сообщение в список сообщений
        возвращает None
        :param message: data from client
        :param client: object of client
        """
        SERVER_LOG.debug(f'Разбор сообщения от клиента : {message}')

        # 1. Получено приветственное сообщение.
        if ACTION in message \
                and message[ACTION] == PRESENCE \
                and TIME in message \
                and USER in message:
            self.autorize_user(message, client)

        # 2. Получено текстовое сообщение.
        elif ACTION in message \
                and message[ACTION] == MESSAGE \
                and DESTINATION in message \
                and TIME in message \
                and SENDER in message \
                and MESSAGE_TEXT in message \
                and self.names[message[SENDER]] == client:
            if message[DESTINATION] in self.names:
                self.database.process_message(
                    message[SENDER], message[DESTINATION])
                self.process_message(message)
                try:
                    send_response(client, RSP_200, sender='server')
                except OSError:
                    self.remove_client(client)
            else:
                response = RSP_400
                response[ERROR] = 'Пользователь не зарегистрирован на сервере.'
                try:
                    send_response(client, response, sender='server')
                except OSError:
                    pass
            return

        # 3. Клиент завершает работу.
        elif ACTION in message \
                and message[ACTION] == EXIT \
                and ACCOUNT_NAME in message \
                and self.names[message[ACCOUNT_NAME]] == client:
            self.remove_client(client)

        # 4. Запрос обновления контакт-листа
        elif ACTION in message \
                and message[ACTION] == CONTACT_LIST \
                and USER in message and \
                self.names[message[USER]] == client:
            response = RSP_200
            response[LIST_INFO] = self.database.get_contacts(message[USER])
            try:
                send_response(client, response, sender='server')
            except OSError:
                self.remove_client(client)

        # 5. Добавление контакта
        elif ACTION in message \
                and message[ACTION] == ADD_CONTACT \
                and ACCOUNT_NAME in message \
                and USER in message \
                and self.names[message[USER]] == client:
            self.database.add_contact(message[USER], message[ACCOUNT_NAME])
            try:
                send_response(client, RSP_200, sender='server')
            except OSError:
                self.remove_client(client)

        # 6. Удаление контакта
        elif ACTION in message \
                and message[ACTION] == REMOVE_CONTACT \
                and ACCOUNT_NAME in message \
                and USER in message \
                and self.names[message[USER]] == client:
            self.database.remove_contact(message[USER], message[ACCOUNT_NAME])
            try:
                send_response(client, RSP_200, sender='server')
            except OSError:
                self.remove_client(client)

        # 7. Запрос известных пользователей
        elif ACTION in message \
                and message[ACTION] == USERS_REQUEST \
                and ACCOUNT_NAME in message \
                and self.names[message[ACCOUNT_NAME]] == client:
            response = RSP_202
            response[LIST_INFO] = [user[0] for user in self.database.users_list()]
            try:
                send_response(client, response, sender='server')
            except OSError:
                self.remove_client(client)

        # 8. Запрос публичного ключа пользователя
        elif ACTION in message \
                and message[ACTION] == PUBLIC_KEY_REQUEST \
                and ACCOUNT_NAME in message:
            response = RESPONSE_511
            response[DATA] = self.database.get_pubkey(message[ACCOUNT_NAME])
            # может быть, что ключа ещё нет (пользователь никогда не логинился,
            # тогда шлём 400)
            if response[DATA]:
                try:
                    send_response(client, response, sender='server')
                except OSError:
                    self.remove_client(client)
            else:
                response = RSP_400
                response[ERROR] = 'Нет публичного ключа для данного пользователя'
                try:
                    send_response(client, response, sender='server')
                except OSError:
                    self.remove_client(client)

        # 9. Неизвестный запрос
        else:
            response = RSP_400
            response[ERROR] = 'Запрос некорректен.'
            try:
                send_response(client, response, sender='server')
            except OSError:
                self.remove_client(client)

    def run(self):
        """
        Метод запускает основной цикл сервера.
        :return:
        """
        # Инициализация Сокета
        self.init_socket()

        # Основной цикл программы сервера
        while self.running:
            # Ждём подключения, если таймаут вышел, ловим исключение.
            try:
                client, client_address = self.sock.accept()
            except OSError:
                pass
            else:
                SERVER_LOG.info(f'Установлено новое соедение -  {client_address}')
                client.settimeout(5)
                self.clients.append(client)

            recv_data_lst = []
            send_data_lst = []
            err_lst = []
            # Проверяем на наличие ждущих клиентов
            try:
                if self.clients:
                    recv_data_lst, self.listen_sockets, self.error_sockets = select.select(
                        self.clients, self.clients, [], 0)
            except OSError as err:
                SERVER_LOG.error(f'Ошибка работы с сокетами: {err.errno}')

            # принимаем сообщения и если ошибка, исключаем клиента.
            if recv_data_lst:
                for client_with_message in recv_data_lst:
                    try:
                        self.process_client_message(
                            get_response(client_with_message, sender='server'), client_with_message)
                    except (OSError, json.JSONDecodeError, TypeError) as err:
                        SERVER_LOG.debug(f'Getting data from client exception.', exc_info=err)
                        self.remove_client(client_with_message)

    def init_socket(self):
        """
        Метод инициализатор сокета.
        """
        SERVER_LOG.info(
            f'Запущен сервер, порт для подключений: '
            f'{self.port} , адрес с которого принимаются подключения: '
            f'{self.addr}. Если адрес не указан, принимаются соединения с любых адресов.')
        # Готовим сокет
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.bind((self.addr, self.port))
        transport.settimeout(0.5)

        # Начинаем слушать сокет.
        self.sock = transport
        self.sock.listen(CONNECTION_LIMIT)

    def service_update_lists(self):
        """
        Метод реализующий отправки сервисного сообщения 205 клиентам.
        :return:
        """
        for client in self.names:
            try:
                send_response(self.names[client], RESPONSE_205, sender='server')
            except OSError:
                self.remove_client(self.names[client])
