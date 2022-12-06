from sqlalchemy import create_engine, Integer, String, DateTime, ForeignKey, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from pprint import pprint


def print_func_log(func):
    """Декоратор для тестирования"""
    def wrapper():
        print(f'-----Вызов функции: {func.__name__}------')
        return func
    return wrapper()


class ServerDB:
    base = declarative_base()

    class AllUsers(base):
        """Класс для взаимодействия с таблицей базы данных users_all"""
        __tablename__ = 'users_all'
        id = Column(Integer, primary_key=True)
        login = Column(String, unique=True)
        last_login = Column(DateTime)

        def __init__(self, login):
            """Конструктор класса AllUsers"""
            self.login = login
            self.last_login = datetime.now()

    class ActiveUsers(base):
        __tablename__ = 'users_active'
        id = Column(Integer, primary_key=True)
        user = Column(String, ForeignKey('users_all.id'), unique=True)
        ip_address = Column(String)
        port = Column(Integer)
        time_in = Column(DateTime)

        def __init__(self, user, ip_address, port, connect_time):
            self.user = user
            self.ip_address = ip_address
            self.port = port
            self.time_in = connect_time

    class UserLoginHistory(base):
        """Класс для взаимодействия с таблицей user_login_history"""
        __tablename__ = 'user_login_history'
        id = Column(Integer, primary_key=True)
        user = Column(String, ForeignKey('users_all.id'))
        ip_address = Column(String)
        port = Column(Integer)
        last_login = Column(DateTime)

        def __init__(self, user, ip_address, port, last_login):
            """Конструктор класса UserLoginHistory"""
            self.user = user
            self.ip_address = ip_address
            self.port = port
            self.last_login = last_login

    def __init__(self):
        """
        Конструктор класса ServerDB
        У каждого экземпляра класса будет свой движок и сессия.
        """
        self.engine = create_engine(
            'sqlite:///server_base_declarative.db3',
            echo=False,
            pool_recycle=7200
            # В функции create_engine есть возможность задать
            # и другие параметры (см. документацию)
        )
        self.base.metadata.create_all(self.engine)
        start_session = sessionmaker(bind=self.engine)
        self.session = start_session()
        self.session.query(self.ActiveUsers).delete()
        self.session.commit()

    def user_login(self, username, ip_address, port):
        """
        Фукнция-обработчик входа пользователя в систему
        :param username: str - имя пользователя
        :param ip_address: str - ip-адресс пользователя
        :param port: int - порт соединения
        :return: None
        """
        # формируется запрос в таблицу users_all
        result = self.session.query(self.AllUsers).filter_by(login=username)
        # если пользователь есть в таблице
        if result.count():
            user = result.first()
            user.last_login = datetime.now()
        # если регистрируется новый пользователь
        else:
            user = self.AllUsers(username)
            self.session.add(user)
            self.session.commit()

        new_active_user = self.ActiveUsers(user.id, ip_address, port, datetime.now())
        self.session.add(new_active_user)
        history = self.UserLoginHistory(user.id, ip_address, port, datetime.now())
        self.session.add(history)
        self.session.commit()

    def user_logout(self, username):
        """
        Функция-обработчик выхода пользователя из системы
        :param username: str - имя пользователя
        :return: None
        """
        # Запрос к таблице активных пользователей, выбираем первую запись.
        user = self.session.query(self.AllUsers).filter_by(login=username).first()
        # Удаление пользователя из таблицы активных пользователей.
        self.session.query(self.ActiveUsers).filter_by(user=user.id).delete()
        # Фиксируем изменения
        self.session.commit()

    def active_users_list(self):
        """
        Функция возвращает список с данными активных пользователей
        :return: list of tuples
        """
        query = self.session.query(
            self.AllUsers.login,
            self.ActiveUsers.ip_address,
            self.ActiveUsers.port,
            self.ActiveUsers.time_in
        ).join(self.AllUsers)  # Пример использования join  в запросе.
        return query.all()

    def all_users_list(self):
        """
        Функция возвращает список с данными всех пользователей
        :return: list of tuples
        """
        query = self.session.query(
            self.AllUsers.login,
            self.AllUsers.last_login,
        )
        return query.all()

    def login_history(self, user=None):
        """
        Функция возвращает историю входа пользователей в систему.
        Если в параметрах передано имя пользователя - результат фильтруется
        по имени пользователя.
        :param user: str - имя пользователя
        :return: list of tuples
        """
        query = self.session.query(
            self.AllUsers.login,
            self.UserLoginHistory.last_login,
            self.UserLoginHistory.ip_address,
            self.UserLoginHistory.port,
        ).join(self.AllUsers)
        # Фильтрация по имени пользователя
        if user:
            query = query.filter(self.AllUsers.login == user)
        return query.all()


if __name__ == '__main__':
    test_db = ServerDB()
    test_db.user_login('tester_1', '196.118.72.221', 7771)
    test_db.user_login('tester_2', '196.118.72.222', 7771)
    test_db.user_login('tester_3', '196.118.72.223', 8081)
    pprint(test_db.active_users_list())
    test_db.user_logout('tester_1')
    pprint(test_db.active_users_list())
    pprint(test_db.login_history('tester_3'))
    pprint(test_db.all_users_list())
