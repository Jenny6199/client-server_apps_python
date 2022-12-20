"""
This modul was created for
Easy Messenger app
december 2022,  Moscow
@author: Maksim Sapunov
"""

from sqlalchemy import create_engine, Table, Column, Integer, String,\
    Text, MetaData, ForeignKey, DateTime
from sqlalchemy.orm import mapper, sessionmaker
from mainapp.common.variables import SERVER_DB_PATH
from _datetime import datetime


class ServerDB:
    """Серверная база данных"""

    class AllUsers:
        """Таблица для хранения всех пользователей"""
        def __init__(self, username, passwd_hash):
            self.name = username
            self.id = None
            self.last_login = datetime.now()
            self.passwd_hash = passwd_hash
            self.pubkey = None

    class ActiveUsers:
        """Таблица для активных пользователей"""
        def __init__(self, user_id, ip_address, port, login_time):
            self.user = user_id
            self.ip_address = ip_address
            self.port = port
            self.login_time = login_time
            self.id = None

    class LoginHistory:
        """Таблица для хранения истории входов"""
        def __init__(self, name, date, ip_address, port):
            self.id = None
            self.name = name
            self.date_time = date
            self.ip = ip_address
            self.port = port

    class UsersContacts:
        """
        Отображение таблицы контактов пользователя
        """
        def __init__(self, user, contact):
            self.id = None
            self.user = user
            self.contact = contact

    class UserHistory:
        """
        Отображение таблицы истории
        """
        def __init__(self, user):
            self.id = None
            self.user = user
            self.sent = 0
            self.accepted = 0

    def __init__(self):
        """Создание движка базы данных"""
        self.database_engine = create_engine(
            SERVER_DB_PATH,  # Путь к БД,
            echo=False,  # Индикация SQL-запросов
            pool_recycle=7200,  # Переустановка соединения каждый час
            connect_args={'check_same_thread': False})
        self.metadata = MetaData()  # Объект метадата

        # Таблица пользователей
        users_table = Table('Users', self.metadata,
                            Column('id', Integer, primary_key=True),
                            Column('name', String, unique=True),
                            Column('last_login', DateTime),
                            Column('passwd_hash', String),
                            Column('pubkey', Text),
                            )
        # Таблица активных пользователей
        active_users_table = Table('Active_users', self.metadata,
                                   Column('id', Integer, primary_key=True),
                                   Column('user', ForeignKey('Users.id'), unique=True),
                                   Column('ip_address', String),
                                   Column('port', Integer),
                                   Column('login_time', DateTime),
                                   )
        # Таблица истории входа
        user_login_history = Table('Login_history', self.metadata,
                                   Column('id', Integer, primary_key=True),
                                   Column('name', ForeignKey('Users.id')),
                                   Column('date_time', DateTime),
                                   Column('ip', String),
                                   Column('port', String),
                                   )
        # Таблица контактов пользователя
        users_contact = Table('User_contact', self.metadata,
                              Column('id', Integer, primary_key=True),
                              Column('user', ForeignKey('Users.id')),
                              Column('contact', ForeignKey('Users.id')),
                              )

        # Таблица истории пользователя
        user_history = Table('User_history', self.metadata,
                             Column('id', Integer, primary_key=True),
                             Column('user', ForeignKey('Users.id')),
                             Column('send', Integer),
                             Column('accepted', Integer),
                             )

        # Создание таблиц
        self.metadata.create_all(self.database_engine)
        # Связывание таблиц БД с классами Python с помощью mapper
        mapper(self.AllUsers, users_table)
        mapper(self.ActiveUsers, active_users_table)
        mapper(self.LoginHistory, user_login_history)
        mapper(self.UsersContacts, users_contact)
        mapper(self.UserHistory, user_history)

        # Создание сессии
        session = sessionmaker(bind=self.database_engine)
        self.session = session()
        self.session.query(self.ActiveUsers).delete()

        # initial commit
        self.session.commit()

    def user_login(self, username, ip_address, port, key):
        """
        Функция вносит изменения в базу данных при входе пользователя
        Обновляет открытый ключ пользователя при его изменении.
        :param username - str имя пользователя
        :param ip_address - str ip-адресс пользователя
        :param port - int номер порта
        :param key - str публичный ключ пользователя
        """
        # Проверяем что пользователь имеется в таблице пользователей
        rez = self.session.query(self.AllUsers).filter_by(name=username)
        # Если пользователь в таблице имеется обновляем время входа и ключ
        if rez.count():
            user = rez.first()
            user.last_login = datetime.now()
            if user.pubkey != key:
                user.pubkey = key
        # Если пользователя нет в таблице вызывается исключение
        else:
            raise ValueError('Пользователь не зарегистрирован.')
        # Создание записи в таблице активных пользователей.
        new_active_user = self.ActiveUsers(user.id, ip_address, port, datetime.now())
        self.session.add(new_active_user)
        # Создание записи в таблице истории входа
        history = self.LoginHistory(user.id, datetime.now(), ip_address, port)
        self.session.add(history)
        # Коммит
        self.session.commit()

    def add_user(self, name, passwd_hash):
        """
        Метод получает имя пользователя и хэш пароля, добавляет запись в таблицу UserHistory БД
        :param name: str - имя пользователя
        :param passwd_hash: str - хэш пароля
        :return: None
        """
        user_row = self.AllUsers(name, passwd_hash)
        self.session.add(user_row)
        self.session.commit()

        history_row = self.UserHistory(user_row.id)
        self.session.add(history_row)
        self.session.commit()

    def remove_user(self, name):
        """
        Метод получает имя пользователя и удаляет запись из всех таблиц в БД
        :param name:
        :return:
        """
        user = self.session.query(self.AllUsers).filter_by(name=name).first()
        self.session.query(self.ActiveUsers).filter_by(user=user.id).delete()
        self.session.query(self.LoginHistory).filter_by(user=user.id).delete()
        self.session.query(self.UsersContacts).filter_by(user=user.id).delete()
        self.session.query(self.UserHistory).filter_by(user=user.id).delete()
        self.session.query(self.AllUsers).filter_by(name=name).delete()
        self.session.commit()

    def get_hash(self, name):
        """
        Метод для получения из базы данных хэша пароля пользователя
        :param - str - name, username
        :return - str - user password's hash
        """
        user = self.session.query(self.AllUsers).filter_by(name=name).first()
        return user.passwd_hash

    def get_pubkey(self, name):
        """
        Метод получает имя пользователя, запрашивает из БД публичный ключ пользователя и возвращает его.
        :param name: str - имя пользователя
        :return: str - публичный ключ пользователя
        """
        user = self.session.query(self.AllUsers).filter_by(name=name).first()
        return user.pubkey

    def check_user(self, name):
        """Метод проверяющий существование пользователя."""
        if self.session.query(self.AllUsers).filter_by(name=name).count():
            return True
        else:
            return False

    def user_logout(self, username):
        """
        Функция вносит изменения в базу данных при выходе пользователя.
        :param username - имя пользователя.
        """
        user = self.session.query(self.AllUsers).filter_by(name=username).first()
        self.session.query(self.ActiveUsers).filter_by(user=user.id).delete()
        self.session.commit()

    def process_message(self, sender, recipient):
        """
        Метод записывает в таблицу статистики факт передачи сообщения.
        :param: sender - str отправитель сообщения
        :param: recipient - str получатель сообщения
        """
        # ID отправителя
        sender_id = self.session.query(self.AllUsers).filter_by(name=sender)
        # ID получателя
        recipient_id = self.session.query(self.AllUsers).filter_by(name=recipient)
        # Увеличиваем счетчики
        sender_row = self.session.query(self.UserHistory).filter_by(user=sender_id).first()
        sender_row.sent += 1
        recipient_row = self.session.query(self.UserHistory).filter_by(user=recipient_id).first()
        recipient_row.accepted += 1

    def add_user_contact(self, user, contact):
        """
        Метод осуществляет добавление контактов для пользователя.
        :param - user str - имя пользователя
        :param - contact str - контакт для добавления
        :return - None
        """
        user = self.session.query(self.AllUsers).filter_by(name=user).first()
        contact = self.session.query(self.AllUsers).filter_by(name=contact).first()
        if not contact \
                or \
                self.session.query(self.UsersContacts).\
                filter_by(user=user.id, contact=contact.id).\
                count():
            return
        contact_row = self.UsersContacts(user.id, contact.id)
        self.session.add(contact_row)
        self.session.commit()

    def remove_user_contact(self, user, contact):
        """
        Метод осуществляет удаление контактов для пользователя.
        :param user:
        :param contact:
        :return:
        """
        user_row = self.session.query(self.AllUsers).filter_by(name=user).first()
        contact_row = self.session.query(self.AllUsers).filter_by(name=contact).first()
        if not contact_row:
            return
        self.session.query(self.UsersContacts).filter(
            self.UsersContacts.user == user_row.id,
            self.UsersContacts.contact == contact_row.id
        ).delete()
        self.session.commit()

    def users_list(self):
        """
        Функция возвращает список пользователей.
        :return: list of tuples - all users.
        """
        query = self.session.query(
            self.AllUsers.name,
            self.AllUsers.last_login,
        )
        return query.all()

    def active_users_list(self):
        """
        Функция возвращает список активных пользователей.
        :return: list of tuples - active users.
        """
        query = self.session.query(
            self.AllUsers.name,
            self.ActiveUsers.ip_address,
            self.ActiveUsers.port,
            self.ActiveUsers.login_time
        ).join(self.AllUsers)
        return query.all()

    def login_history(self, username=None):
        """
        Функция возвращает историю входа. Если указано имя пользователя
        производится фильтрация по конкретному пользователю.
        :param username: str
        :return: list of tuples - login history
        """
        query = self.session.query(
            self.AllUsers.name,
            self.LoginHistory.date_time,
            self.LoginHistory.ip,
            self.LoginHistory.port
            ).join(self.AllUsers)
        if username:
            query = query.filter(self.AllUsers.name == username)
        return query.all()

    def get_contacts(self, username):
        """
        Функция запрашивает список контактов для пользователя
        :param - username
        """
        user = self.session.query(self.AllUsers).filter_by(name=username).one()
        query = self.session.query(
            self.UsersContacts, self.AllUsers.name).\
            filter_by(user=user.id).\
            join(self.AllUsers, self.UsersContacts.contact == self.AllUsers.id)
        return [contact[1] for contact in query.all()]

    def message_history(self):
        """
        Функция возвращает статистику соообщений
        """
        query = self.session.query(
            self.AllUsers.name,
            self.AllUsers.last_login,
            self.UserHistory.sent,
            self.UserHistory.accepted
        ).join(self.AllUsers)
        return query.all()
