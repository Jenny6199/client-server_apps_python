"""
File contents structure of main window for client
graphical presence. Build by PyQtDesigner and then
edited by author. This work was completed during
educated DB_and_PyQt course lesson 5 by GeekBrains,
Moscow, November 2022.
Maksim_Sapunov, Jenny6199@yandex.ru
"""

import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, \
    QWidget, QLabel, QListView, QMessageBox
from PyQt5.QtCore import pyqtSlot, QEvent, Qt


class ClientWindowMain(QMainWindow):
    """Start main window for server part of messenger"""

    def __init__(self, database, transport):
        super(ClientWindowMain, self).__init__()
        self.ui = UiClientMainWindowForm()
        self.ui.setupUi(self)
        self.database = database
        self.transport = transport
        # Connect
        self.ui.pushButton_add_contact.clicked.connect(self.add_contact_window)
        self.ui.pushButton_del_contact.clicked.connect(self.del_contact_window)
        self.ui.pushButton_clear_form.clicked.connect(self.refresh_button)
        self.ui.pushButton_send_message.clicked.connect(self.send_message)

        # Additional atribute
        self.contact_model = None
        self.history_model = None
        self.messages = QMessageBox()
        self.current_chat = None
        self.ui.listView_2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.listView_2.setWordWrap(True)
        self.ui.listView.doubleClicked.connect(self.select_active_user)
        self.clients_list_update()
        self.set_disable_input()

        # Show
        self.show()

    def add_contact_window(self):
        """Обработчик нажатия кнопки  доабвить контакт"""
        print("Button add contact was pressed!")

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
        pass


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
        self.listView = QListView(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(10, 40, 181, 281))
        self.listView.setObjectName("listView")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(200, 10, 231, 21))
        self.label_2.setObjectName("label_2")
        self.listView_2 = QListView(self.centralwidget)
        self.listView_2.setGeometry(QtCore.QRect(200, 40, 341, 281))
        self.listView_2.setObjectName("listView_2")

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
    application = ClientWindowMain(database=None, transport=None)
    sys.exit(app.exec_())
