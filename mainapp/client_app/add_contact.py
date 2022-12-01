"""
File is part of client's part of messenger,
created during completing practical task
for lesson_5 course DB_and_PyQt.
by Maksim Sapunov, Jenny6199@yandex.ru
november, 2022. GeekBrains
"""

import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QPushButton

logger = logging.getLogger('client')


class AddContactDialog(QDialog):
    """
    Класс обеспечивает отображение диалогового окна
    'добавление контактов' в клиентской части программы
    'мессенджер'.
    """
    def __init__(self, transport, database):
        """
        Конструктор класса AddContactDialog
        """
        super().__init__()
        self.transport = transport
        self.database = database
        # Size of dialog window
        self.setFixedSize(350, 120)
        self.setWindowTitle("Выбор контакта для добавления")
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setModal(True)
        # Label_1
        self.label_of_selector = QLabel("Выберете контакт для добавления: ", self)
        self.label_of_selector.setFixedSize(200, 20)
        self.label_of_selector.move(10, 0)
        # Selector
        self.selector = QComboBox(self)
        self.selector.setFixedSize(200, 20)
        self.selector.move(10, 30)
        # Button_1_refresh
        self.refresh_button = QPushButton("Обновить список", self)
        self.refresh_button.setFixedSize(100, 30)
        self.refresh_button.move(60, 60)
        self.refresh_button.clicked.connect(self.refresh_possible_contacts)
        # Button_2_ok
        self.ok_button = QPushButton("Добавить", self)
        self.ok_button.setFixedSize(100, 30)
        self.ok_button.move(230, 20)
        # Button_3_cancel
        self.cancel_button = QPushButton("Отмена", self)
        self.cancel_button.setFixedSize(100, 30)
        self.cancel_button.move(230, 60)
        self.cancel_button.clicked.connect(self.close)

        # Upgrade list finally
        self.update_possible_contacts()

    def update_possible_contacts(self):
        """
        Возвращает список контактов доступных для добавления
        """
        self.selector.clear()
        list_of_contacts = set(self.database.get_contacts())
        list_of_users = set(self.database.users_list())
        list_of_users.remove(self.transport.username)
        self.selector.addItems(list_of_users - list_of_contacts)

    def refresh_possible_contacts(self):
        """
        Обработчик нажатия кнопки обновить список доступных контактов
        """
        try:
            self.transport.user_list_update()
        except OSError:
            pass
        else:
            logger.debug('Выполнено обновление списка доступных контактов')
            self.update_possible_contacts()
