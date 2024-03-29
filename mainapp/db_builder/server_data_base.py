from sqlalchemy import create_engine, Table, Column, Integer, String, \
    MetaData, ForeignKey, DateTime
from sqlalchemy.orm import mapper, sessionmaker
# from ..common.variables import SERVER_DB
# from uuid import uuid4
from _datetime import datetime
from pprint import pprint

SERVER_DB = 'sqlite:///server_base.db3'


class ServerDB:
    """Серверная база данных"""

    class AllUsers:
        """Таблица для всех пользователей"""

        def __init__(self, username):
            self.name = username
            self.id = None
            self.last_login = datetime.now()

    class ActiveUsers:
        """Таблица для актитвных пользователей"""

        def __init__(self, user_id, ip_address, port, login_time):
            self.user = user_id
            self.ip_address = ip_address
            self.port = port
            self.login_time = login_time
            self.id = None

    class UsersHistory:
        """Таблица для истории пользователей"""

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
                            Column('id', Integer, primary_key=True),
                            Column('name', String, unique=True),
                            Column('last_login', DateTime)
                            )
        # Таблица активных пользователей
        active_users_table = Table('Active_users', self.metadata,
                                   Column('id', Integer, primary_key=True),
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
                                   Column('ip', String),
                                   Column('port', String)
                                   )

        # Cоздание таблиц
        self.metadata.create_all(self.database_engine)

        # Связывание таблиц БД с классами Python с помощью mapper
        mapper(self.AllUsers, users_table)
        mapper(self.ActiveUsers, active_users_table)
        mapper(self.UsersHistory, user_login_history)

        # Cоздание сессии
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
        new_active_user = self.ActiveUsers(user.id, ip_address, port, datetime.now())
        self.session.add(new_active_user)
        history = self.UsersHistory(user.id, datetime.now(), ip_address, port)
        self.session.add(history)
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
            self.AllUsers.name,
            self.AllUsers.last_login
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
            self.UsersHistory.date_time,
            self.UsersHistory.ip,
            self.UsersHistory.port
            ).join(self.AllUsers)
        if username:
            query = query.filter(self.AllUsers.name == username)
        return query.all()


if __name__ == '__main__':
    # создание базы
    test_DB = ServerDB()
    print('подключение тестовых пользователей')
    test_DB.user_login('user_1', '174.16.2.28', 7777)
    test_DB.user_login('user_2', '174.16.2.30', 7171)
    print('проверка функции active_users_list')
    pprint(test_DB.active_users_list())

    print('проверка функции user_logout')
    test_DB.user_logout('user_1')
    print(test_DB.active_users_list())

    print('проверка функции login_history')
    pprint(test_DB.login_history('user_1'))

    print('проверка функции history_login')
    pprint(test_DB.users_list())
