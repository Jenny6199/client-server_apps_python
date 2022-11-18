from sqlalchemy import create_engine, Table, Column, Integer, String,\
    MetaData, ForeignKey, DateTime
from sqlalchemy.orm import mapper, sessionmaker
from ..common.variables import SERVER_DB
from uuid import uuid4
from _datetime import datetime


class ServerDB:
    """Серверная база данных"""

    class AllUsers:
        """Таблица для хранения всех пользователей"""
        def __init__(self, login):
            self.login = login
            self.id = None
            self.last_login = datetime.now()

    class ActiveUsers:
        """Таблица для активных пользователей"""
        def __init__(self, user_id, ip_address, port, login_time):
            self.user = user_id
            self.ip_address = ip_address
            self.port = port
            self.login_time = login_time
            self.id = None

    class UserHistory:
        """Таблица для хранения истории входов"""
        def __init__(self, name, date, ip_address, port):
            self.id = None
            self.name = name
            self.date_time = date
            self.ip = ip_address
            self.port = port

    def __init__(self):
        """Создание движка базы данных"""
        self.database_engine = create_engine(
            SERVER_DB,  # Путь к БД, сохранен в отдельной переменной
            echo=False,  # Индикация SQL-запросов
            pool_recycle=3600  # Переустановка соединения каждый час
        )
        self.metadata = MetaData()  # Объект метадата

        # Таблица пользователей
        users_table = Table('Users', self.metadata,
                            Column('id', uuid4(), primary_key=True),
                            Column('name', String, unique=True),
                            Column('last_login', DateTime)
                            )
        # Таблица активных пользователей
        active_users_table = Table('Active_users', self.metadata,
                                   Column('id', uuid4(), primary_key=True),
                                   Column('user', ForeignKey('Users.id'), unique=True),
                                   Column('ip_address', String),
                                   Column('port', Integer),
                                   Column('login_time', DateTime)
                                   )
        # Таблица истории входа
        user_login_history = Table('Login_history', self.metadata,
                                   Column('id', Integer, primary_key=True),
                                   Column('name', ForeignKey('Users.id')),
                                   Column('date_time', DateTime),
                                   Column('ip', String)
                                   )

        # Создание таблиц
        self.metadata.create_all(self.database_engine)
        # Связывание таблиц БД с классами Python с помощью mapper
        mapper(self.AllUsers, users_table)
        mapper(self.ActiveUsers, active_users_table)
        mapper(self.UsersHistory, user_login_history)

        # Создание сессии
        session = sessionmaker(bind=self.database_engine)
        self.session = session()
        self.session.query(self.ActiveUsers).delete()

        # initial commit
        self.session.commit()

    def user_login(self, username, ip_address, port):
        """
        Функция вносит изменения в базу данных при входе пользователя
        :param username - str
        :param ip_address - str
        :param port - int
        """
        print(username, ip_address, port)
        rez = self.session.query(self.AllUsers).filter_by(name=username)
        if rez.count():
            user = rez.first()
            user.last_login = datetime.now()
        else:
            user = self.AllUsers(username)
            self.session.add(user)
            self.session.commit()

    def user_logout(self, username):
        """
        Функция вносит изменения в базу данных при выходе пользователя.
        :param username - имя пользователя.
        """
        user = self.session.query(self.AllUsers).filter_by(name=username).first()
        self.session.query(self.ActiveUsers).filter_by(user=user.id).delete()
        self.session.commit()

    def users_list(self):
        """
        Функция возвращает список пользователей.
        :return: list of tuples - all users.
        """
        query = self.session.query(
            self.AllUsers.login,
            self.AllUsers.last_login
        )
        return query.all()

    def active_users_list(self):
        """
        Функция возвращает список активных пользователей.
        :return: list of tuples - active users.
        """
        query = self.session.query(
            self.AllUsers.login,
            self.ActiveUsers.ip_addres,
            self.AllUsers.port,
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
            self.UsersHistory.date_time,
            self.UsersHistory.ip,
            self.UsersHistory.port
            ).join(self.AllUsers)
        if username:
            query = query.filter(self.AllUsers.name == username)
        return query.all()
