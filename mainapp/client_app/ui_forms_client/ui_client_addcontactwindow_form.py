"""
File is part of client's part of messenger,
created during completing practical task
for lesson_5 course DB_and_PyQt.
by Maksim Sapunov, Jenny6199@yandex.ru
november, 2022. GeekBrains
"""

import logging
import sys

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QPushButton
from PyQt5.QtCore import Qt

logger = logging.getLogger('client')


class UiClientAddContactDialogForm(object):
    """
    Класс обеспечивает отображение диалогового окна
    'добавление контактов' в клиентской части программы
    'мессенджер'.
    """

    def setupUi(self, add_contact):
        """
        Настройки виджета добавление контакта
        """
        # Size of dialog window
        add_contact.setObjectName("add_contact")
        add_contact.setFixedSize(350, 120)
        add_contact.setWindowTitle("Выбор контакта для добавления")
        add_contact.setAttribute(Qt.WA_DeleteOnClose)
        add_contact.setModal(True)
        self.centralwidget = QWidget(add_contact)
        self.centralwidget.setObjectName("centralwidget")

        # Label_1
        self.label_of_selector = QLabel(self.centralwidget)
        self.label_of_selector.setObjectName("label_of_selector")
        self.label_of_selector.setText("Выбрать контакт: ")
        self.label_of_selector.setFixedSize(200, 20)
        self.label_of_selector.move(10, 10)

        # Selector
        self.selector = QComboBox(self.centralwidget)
        self.selector.setObjectName("selector")
        self.selector.setFixedSize(200, 20)
        self.selector.move(10, 35)

        # Button_1_refresh
        self.refresh_button = QPushButton(self.centralwidget)
        self.refresh_button.setObjectName("refresh_button")
        self.refresh_button.setText("Обновить")
        self.refresh_button.setFixedSize(100, 30)
        self.refresh_button.move(60, 65)

        # Button_2_ok
        self.ok_button = QPushButton(self.centralwidget)
        self.ok_button.setObjectName("ok_button")
        self.ok_button.setText("Добавить")
        self.ok_button.setFixedSize(100, 30)
        self.ok_button.move(230, 20)

        # Button_3_cancel
        self.cancel_button = QPushButton(self.centralwidget)
        self.cancel_button.setObjectName("cancel_button")
        self.cancel_button.setText("Отмена")
        self.cancel_button.setFixedSize(100, 30)
        self.cancel_button.move(230, 60)


class ClientAddContactWindow(QDialog):
    def __init__(self, database, transport):
        super(ClientAddContactWindow, self).__init__()
        self.transport = transport
        self.database = database
        self.ui = UiClientAddContactDialogForm()
        self.ui.setupUi(self)
        self.show()

        # Connect
        self.ui.refresh_button.clicked.connect(self.refresh_possible_contacts)
        self.ui.ok_button.clicked.connect(self.button_add_contact)

    def update_possible_contacts(self):
        """
        Возвращает список контактов доступных для добавления
        """
        self.ui.selector.clear()
        list_of_contacts = set(self.database.get_contacts())
        list_of_users = set(self.database.users_list())
        list_of_users.remove(self.transport.username)
        self.ui.selector.addItems(list_of_users - list_of_contacts)

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

    def button_add_contact(self):
        """Обработчик нажатия кнопки добавить контакт"""
        pass


if __name__ == '__main__':
    # Тестовый запуск и отладка
    app = QApplication(sys.argv)
    application = ClientAddContactWindow(database=None, transport=None)
    sys.exit(app.exec_())
