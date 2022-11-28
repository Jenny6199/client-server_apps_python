from sqlalchemy import create_engine, Table, Column, Integer, String,\
    Text, MetaData, DateTime
from sqlalchemy.orm import mapper, sessionmaker
from os.path import dirname, realpath, join
import sys
from mainapp.common.variables import *
from datetime import datetime


class ClientDatabase:
    """
    Класс формирует клиенсткую базу данных и содержит методы
    позволяющие с ней взаимодействовать.
    (add_contact, del_contact, add_user, save_message, get_contacts,
    get_users, check_user, check_contact, get_history).
    База данных содержит три таблицы для хранения соответствующей информации:
    1) Таблица пользователей (class KnownUsers),
    2) Таблица истории сообщений (class MessageHistory),
    3) Таблица контактов пользователей (class Contacts)
    """
    class KnownUsers:
        """Отображение таблицы пользователей"""
        def __init__(self, user):
            self.id = None
            self.username = user

    class MessageHistory:
        """Отображение таблицы истории сообщений"""
        def __init__(self, contact, direction, message):
            self.id = None
            self.contact = contact
            self.direction = direction
            self.message = message
            self.date = datetime.now()

    class Contacts:
        """Отображение таблицы списка контактов"""
        def __init__(self, contact):
            self.id = None
            self.name = contact

    def __init__(self, name):
        """Конструктор класса ClientDatabase"""
        # Обозначение пути к файлу базы данных и его название
        db_path = dirname(realpath(__file__))
        db_name = f'database_client_{name}'

        # 1.Создание движка базы данных
        self.database_engine = create_engine(
            f'sqlite:///{join(db_path, db_name)}',
            echo=False,
            pool_recycle=7200,
            connect_args={'check_same_thread': False}
        )

        # 2. Создание объекта MetaData
        self.metadata = MetaData()

        # 3. Создание таблиц
        users = Table('known_users', self.metadata,
                      Column('id', Integer, primary_key=True),
                      Column('username', String)
                      )

        history = Table('message_history', self.metadata,
                        Column('id', Integer, primary_key=True),
                        Column('contact', String),
                        Column('direction', String),
                        Column('message', Text),
                        Column('date', DateTime)
                        )

        contacts = Table('contacts', self.metadata,
                         Column('id', Integer, primary_key=True),
                         Column('name', String, unique=True)
                         )

        # 4. Связываем таблицы с движком
        self.metadata.create_all(self.database_engine)

        # 5. Mapping
        mapper(self.KnownUsers, users)
        mapper(self.MessageHistory, history)
        mapper(self.Contacts, contacts)

        # 6. Session
        current_session = sessionmaker(bind=self.database_engine)
        self.session = current_session()

        # 7. Cleaning
        self.session.query(self.Contacts).delete()
        self.session.commit()

    def get_contacts(self):
        return [contact[0] for contact in self.session.query(self.Contacts.name).all()]

    def check_contact(self):
        pass

    def add_contact(self, contact):
        pass

    def del_contact(self, contact):
        pass

    def get_users(self):
        pass

    def add_user(self, user):
        pass

    def check_user(self):
        pass

    def save_message(self, contact, direction, message):
        pass

    def get_history(self):
        pass
