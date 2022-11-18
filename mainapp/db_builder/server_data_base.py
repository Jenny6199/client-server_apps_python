from sqlalchemy import create_engine, Table, Column, Integer, String,\
    MetaData, ForeignKey, DateTime
from sqlalchemy.orm import mapper, sessionmaker
from ..common.variables import *
from uuid import uuid4
import datetime


class ServerDB:
    """Серверная база данных"""

    class AllUsers:
        """Таблица для хранения всех пользователей"""
        def __init__(self, login):
            self.login = login

    class ActiveUsers:
        """Таблица для активных пользователей"""
        pass

    class UserHistory:
        """Таблица для хранения истории входов"""
        pass
