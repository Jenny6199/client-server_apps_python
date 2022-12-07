from sqlalchemy import create_engine, Table, Column, Integer, String,\
    Text, MetaData, DateTime
from sqlalchemy.orm import mapper, sessionmaker
from os.path import dirname, realpath, join
from datetime import datetime
from logging import getLogger

CLIENT_LOG = getLogger('client')


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
        """
        Осуществляет запрос списка контактов
        :return - list(Contacts.name)
        """
        return [contact[0] for contact in self.session.query(self.Contacts.name).all()]

    def check_contact(self, contact):
        """
        Проверяет наличие контакта в списке контактов
        :param - contact
        :return - True if contact in Contacts.name else False
        """
        if self.session.query(self.Contacts).filter_by(name=contact).count():
            return True
        else:  # count = 0
            return False

    def add_contact(self, contact):
        """
        Осуществляет добавление контакта в список контактов
        :param - contact
        :return - None
        """
        CLIENT_LOG.debug(f'Запущена функция add_contact c параметрами {contact}.')
        if not self.session.query(self.Contacts).filter_by(name=contact).count():
            contact_row = self.Contacts(contact)
            self.session.add(contact_row)
            self.session.commit()

    def del_contact(self, contact):
        """
        Осуществляет удаление контакта из списка контактов
        :param - contact
        :return - None
        """
        self.session.query(self.Contacts).filter_by(name=contact).delete()

    def get_users(self):
        """
        Осуществляет запрос списка известных пользователей
        :return - list(KnownUsers.username)
        """
        return [user[0] for user in self.session.query(self.KnownUsers.username).all()]

    def add_user(self, users_list):
        """
        Осуществляет добавление в список известных пользователей
        :param - user_list
        :return - None
        """
        self.session.query(self.KnownUsers).delete()
        for user in users_list:
            row = self.KnownUsers(user)
            self.session.add(row)
        self.session.commit()

    def check_user(self, user):
        """
        Проверяет наличие пользователя в списке известных пользователей
        :param - user
        :return - True if user in KnownUsers, else False.
        """
        if self.session.query(self.KnownUsers).filter_by(username=user).count():
            return True
        else:
            return False
        pass

    def save_message(self, contact, direction, message):
        """
        Осуществляет сохранение сообщений в истории сообщений
        :param - contact
        :param - direction
        :param - message (str)
        :return - None
        """
        row = self.MessageHistory(contact, direction, message)
        self.session.add(row)
        self.session.commit()

    def get_history(self, contact):
        """
        Осуществляет запрос истории сообщений
        :param - contact
        :return - list[(contact, direction, message, date),]
        """
        query = self.session.query(self.MessageHistory).filter_by(contact=contact)
        return [(row.contact,
                row.direction,
                row.message,
                row.date) for row in query.all()
                ]


if __name__ == "__main__":
    # Тестовый запуск клиентской базы данных
    test_client_db = ClientDatabase('test_1')
    # Тест функции добавления контактов
    for test_user in ['test_2', 'test_3', 'test_4', 'test_5']:
        test_client_db.add_contact(test_user)
    # Добавляем существующий
    test_client_db.add_contact('test_4')
    # Тест функции добавления пользователей
    test_client_db.add_user(['test_1', 'test_2', 'test_3', 'test_4', 'test_5'])
    # Тест функции save_message
    test_client_db.save_message('test_4', 'in', 'Test message!')
    print(test_client_db.get_contacts())
    print(test_client_db.get_users())
    print(test_client_db.check_user('test_2'))
    # Тест функции del_contact
    test_client_db.del_contact('test_3')
    print(test_client_db.get_contacts())
    # Тесты пройдены
    print('Success!')
