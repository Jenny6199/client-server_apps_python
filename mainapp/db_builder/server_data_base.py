from sqlalchemy import create_engine, Table, Column, Integer, String, \
    MetaData, ForeignKey, DateTime
from sqlalchemy.orm import mapper, sessionmaker
from ..common.variables import *
from uuid import uuid4
import datetime


class ServerDB:
    """Серверная база данных"""

    class AllUsers:
        """Таблица для всех пользователей"""
        def __init__(self, login):
            self.login = login
            self.id

    class ActiveUsers:
        """Таблица для актитвных пользователей"""
        pass

    class UsersHistory:
        """Таблица для истории пользователей"""
        pass
