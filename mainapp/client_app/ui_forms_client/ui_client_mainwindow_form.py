"""
File contents structure of main window for client
graphical presence. Build by PyQtDesigner and then
edited by author. This work was completed during
educated DB_and_PyQt course lesson 5 by GeekBrains,
Moscow, November 2022.
Maksim_Sapunov, Jenny6199@yandex.ru
"""
# internal libraries import
import sys
import json
import logging
import base64

# internal modules import
from mainapp.client_app.client_transport import ClientTransport
from mainapp.client_app.client_database import ClientDatabase
from mainapp.client_app.ui_forms_client.ui_client_addcontactwindow_form import ClientAddContactWindow

# external libraries import
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, \
    QWidget, QLabel, QListView, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor
from PyQt5.QtCore import pyqtSlot, QEvent, Qt
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA


class ClientWindowMain(QMainWindow):
    """Start main window for server part of messenger"""

    def __init__(self, database, transport, keys):
        """
        Конструктор класса ClientWindowMain
        :param - database
        :param - transport
        """
        # Инициализация суперкласса (QMainWindow)
        super(ClientWindowMain, self).__init__()
        # Основные параметры
        self.database = database
        self.transport = transport
        self.ui = UiClientMainWindowForm()
        self.ui.setupUi(self)
        self.decrypter = PKCS1_OAEP.new(keys)
        # Connect
        self.ui.pushButton_add_contact.clicked.connect(self.add_contact_window)
        self.ui.pushButton_del_contact.clicked.connect(self.del_contact_window)
        self.ui.pushButton_clear_form.clicked.connect(self.refresh_button)
        self.ui.pushButton_send_message.clicked.connect(self.send_message)

        # Additional atribute
        self.contacts_model = None
        self.history_model = None
        self.messages = QMessageBox()
        self.current_chat = None
        self.ui.list_messages.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.list_messages.setWordWrap(True)
        self.ui.list_users.doubleClicked.connect(self.select_active_user)
        self.clients_list_update()
        self.set_disable_input()

        # Show
        self.show()

    def add_contact_window(self):
        """Обработчик нажатия кнопки  добавить контакт"""
        print("Button add contact was pressed!")
        add_contact_window = ClientAddContactWindow(database=self.database, transport=self.transport)
        add_contact_window.show()
        print("def add_contact_window was complite!")

    def del_contact_window(self):
        """Обработчик нажатия кнопки удалить контакт"""
        print("Button del contact was pressed!")

    def refresh_button(self):
        """Обработчик нажатия кнопки обновить"""
        print("Button del refresh was pressed!")

    def send_message(self):
        """Обработчик нажатия кнопки удалить контакт"""
        print("Button send message was pressed!")

    def select_active_user(self):
        pass

    def set_disable_input(self):
        pass

    def clients_list_update(self):
        contacts_list = self.database.get_contacts()
        self.contacts_model = QStandardItemModel()
        for i in sorted(contacts_list):
            item = QStandardItem(i)
            item.setEditable(False)
            self.contacts_model.appendRow(item)
        self.ui.list_users.setModel(self.contacts_model)

    def history_list_update(self):
        """
        Обеспечивает обновление истории сообщений и вывод их в диалоговое окно.
        :param - None
        :return - None
        """
        # Загружаем сообщения из базы данных сортированным списком
        history_list = sorted(self.database.get_history(self.current_chat),
                              key=lambda item: item[3]
                              )
        # Если запуск первый -> создаем модель.
        if not self.history_model:
            self.history_model = QStandardItemModel()
            self.ui.list_messages.setMode(self.history_model)
        self.history_model.clear()
        history_list_length = len(history_list)
        start_index = 0
        if history_list_length > 20:
            start_index = history_list_length - 20
        for i in range(start_index, history_list_length):
            item = list[i]
            # Разделяем стили оформления входящих и исходящих сообщений
            if item[1] == 'in':
                mess = QStandardItem(
                    f'Входящее сообщение от {item[3].replace(microsecond=0)}:\n'
                    f' {item[2]}'
                )
                mess.setEditable(False)
                mess.setBackground(QBrush(QColor(255, 213, 213)))
                mess.setTextAlignment(Qt.AlignLeft)
                self.history_model.appendRow(mess)
            else:
                mess = QStandardItem(
                    f'Входящее сообщение от {item[3].replace(microsecond=0)}:\n'
                    f' {item[2]}'
                )
                mess.setEditable(False)
                mess.setBackground(QBrush(QColor(204, 255, 204)))
                mess.setTextAlignment(Qt.AlignRight)
                self.history_model.appendRow(mess)
        self.ui.list_messages.scrollToBottom()

    @pyqtSlot()
    def message(self, sender):
        """Слот-обработчик приёма нового сообщения"""
        if sender == self.current_chat:
            pass

    def make_connection(self, transport_object):
        transport_object.new_message.connect(self.message)
        transport_object.connection_lost.connect(self.connection_lost)

    @pyqtSlot()
    def connection_lost(self):
        self.messages.warning(self, 'Сбой соединения', 'Потеряно соединение с сервером!')
        self.close()


class UiClientMainWindowForm(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(557, 539)
        MainWindow.setAcceptDrops(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 141, 21))
        self.label.setObjectName("label")
        self.list_users = QListView(self.centralwidget)
        self.list_users.setGeometry(QtCore.QRect(10, 40, 181, 281))
        self.list_users.setObjectName("list_users")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(200, 10, 231, 21))
        self.label_2.setObjectName("label_2")
        self.list_messages = QListView(self.centralwidget)
        self.list_messages.setGeometry(QtCore.QRect(200, 40, 341, 281))
        self.list_messages.setObjectName("list_messages")

        # Ярлык информационное сообщение
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(18, 321, 411, 31))
        self.label_3.setObjectName("label_3")

        # Поле ввода сообщения
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(200, 360, 341, 111))
        self.textBrowser.setObjectName("textBrowser")

        # Кнопки формы
        # Button 1 Добавить контакт
        self.pushButton_add_contact = QPushButton(self.centralwidget)
        self.pushButton_add_contact.setGeometry(QtCore.QRect(18, 360, 171, 25))
        self.pushButton_add_contact.setObjectName("pushButton")

        # Button 2 Удалить контакт
        self.pushButton_del_contact = QPushButton(self.centralwidget)
        self.pushButton_del_contact.setGeometry(QtCore.QRect(18, 390, 171, 25))
        self.pushButton_del_contact.setObjectName("pushButton_2")

        # Button 3 Очистить
        self.pushButton_clear_form = QPushButton(self.centralwidget)
        self.pushButton_clear_form.setGeometry(QtCore.QRect(18, 420, 171, 25))
        self.pushButton_clear_form.setObjectName("pushButton_3")

        # Button 4 Отправить
        self.pushButton_send_message = QPushButton(self.centralwidget)
        self.pushButton_send_message.setGeometry(QtCore.QRect(18, 450, 171, 25))
        self.pushButton_send_message.setObjectName("pushButton_4")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 557, 22))
        self.menubar.setObjectName("menubar")
        self.menuExit = QtWidgets.QMenu(self.menubar)
        self.menuExit.setObjectName("menuExit")
        self.menuRefresh = QtWidgets.QMenu(self.menubar)
        self.menuRefresh.setObjectName("menuRefresh")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuExit.menuAction())
        self.menubar.addAction(self.menuRefresh.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Мессенджер. Клиент v 0.2.0"))
        self.label.setText(_translate("MainWindow", "Список контактов"))
        self.label_2.setText(_translate("MainWindow", "История сообщений"))
        self.label_3.setText(_translate("MainWindow", "Для выбора получателя кликните его в списке контактов"))
        self.pushButton_add_contact.setText(_translate("MainWindow", "Добавить контакт"))
        self.pushButton_del_contact.setText(_translate("MainWindow", "Удалить контакт"))
        self.pushButton_clear_form.setText(_translate("MainWindow", "Очистить форму"))
        self.pushButton_send_message.setText(_translate("MainWindow", "Отправить сообщение"))
        self.menuExit.setTitle(_translate("MainWindow", "Файл"))
        self.menuRefresh.setTitle(_translate("MainWindow", "Контакты"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    application = ClientWindowMain(database=None, transport=None, keys=None)
    sys.exit(app.exec_())
