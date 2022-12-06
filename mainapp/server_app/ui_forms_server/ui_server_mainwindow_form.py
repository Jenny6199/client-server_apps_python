"""
File contents structure of main window for server
graphical presence. Build by PyQtDesigner and then
edited by author. This work was completed during
educated DB_and_PyQt course lesson 4 by GeekBrains,
Moscow, November 2022.
Maksim_Sapunov, Jenny6199@yandex.ru
"""

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import qApp, QMainWindow, QApplication
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QTableView, QFrame, QWidget, QLabel
import sys


# from PyQt5.QtCore import Qt
# from ui_forms_server.ui_server_settingswindow_form import ServerWindowSettingsForm


class ServerWindowMain(QMainWindow):
    """Start main window for server part of messenger"""

    def __init__(self):
        super(ServerWindowMain, self).__init__()
        self.ui = UiServerMainWindowForm()
        self.ui.setupUi(self)
        self.show()


class UiServerMainWindowForm(object):
    """
    Class contents form for server part of messenger.
    Created by QtDesigner.
    """
    def setupUi(self, ServerMainWindow):
        """
        Base filling of main window form.
        Created automaticaly by QtDesigner and then edited and
        commented.
        """
        ServerMainWindow.setObjectName("ServerMainWindow")
        ServerMainWindow.resize(635, 602)
        # CentralWidget
        self.centralwidget = QWidget(ServerMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.show()

        # VerticalWidget
        self.verticalWidget = QWidget(self.centralwidget)
        self.verticalWidget.setGeometry(QtCore.QRect(10, 70, 611, 271))
        self.verticalWidget.setObjectName("verticalWidget")

        # Verticallayout
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        # Line 1
        self.line = QFrame(self.verticalWidget)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)

        # Label
        self.label = QLabel(self.verticalWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)

        # Table
        self.active_clients_tableView = QTableView(self.verticalWidget)
        self.active_clients_tableView.setEnabled(True)
        self.active_clients_tableView.setObjectName("active_clients_tableView")
        self.verticalLayout.addWidget(self.active_clients_tableView)

        # Line_2
        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(10, 340, 611, 16))
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.line_2.setObjectName("line_2")

        # HorizontalLayout
        self.horizontalLayoutWidget_3 = QWidget(self.centralwidget)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(10, 10, 611, 51))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        # Buttons
        # 1 Exit
        self.button_exit = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.button_exit.setObjectName("button_exit")
        self.horizontalLayout_3.addWidget(self.button_exit)
        self.button_exit.clicked.connect(qApp.quit)

        # 2 Refresh
        self.button_refresh = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.button_refresh.setObjectName("button_refresh")
        self.horizontalLayout_3.addWidget(self.button_refresh)
        self.button_refresh.clicked.connect(call_refresh)

        # 3 Log
        self.button_log = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.button_log.setObjectName("button_log")
        self.horizontalLayout_3.addWidget(self.button_log)
        self.button_log.clicked.connect(call_log)

        # 4 Settings
        self.button_settings = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.button_settings.setObjectName("button_settings")
        self.horizontalLayout_3.addWidget(self.button_settings)
        self.button_settings.clicked.connect(call_settings)

        ServerMainWindow.setCentralWidget(self.centralwidget)

        # Изменяем названия ярлыков и надписей
        self.retranslateUi(ServerMainWindow)

        QtCore.QMetaObject.connectSlotsByName(ServerMainWindow)

    def retranslateUi(self, ServerMainWindow):
        """
        Contains indications for text`s fields in the main window form.
        """
        _translate = QtCore.QCoreApplication.translate
        ServerMainWindow.setWindowTitle(_translate("ServerMainWindow", "Мессенджер 0.2.0. Сервер"))
        self.label.setText(_translate("ServerMainWindow", "Активные пользователи"))
        self.button_exit.setText(_translate("ServerMainWindow", "Выход"))
        self.button_refresh.setText(_translate("ServerMainWindow", "Обновить"))
        self.button_log.setText(_translate("ServerMainWindow", "Лог"))
        self.button_settings.setText(_translate("ServerMainWindow", "Настройки"))


def call_settings():
    """Функция обработчик нажатия клавиши настроек сервера"""
    print('Нажата клавиша вызова окна настроек сервера')


def call_log():
    """Функция обработчик нажатия клавиши истории пользователей"""
    print('Нажата клавиша вызова окна истории пользователей')


def call_refresh():
    """Функция обработчик нажатия клавиши обновления данных"""
    print('Нажата клавиша обновления данных')


def create_main_table(database):
    user_list = database.active_users_list()
    table_list = QStandardItemModel()
    table_list.setHorizontalHeaderLabels(['Имя клиента', 'Адрес', 'Порт', 'Время подключения'])
    for row in user_list:
        user, ip, port, time = row
        user = QStandardItem(user)
        user.setEditable(False)
        ip = QStandardItem(ip)
        ip.setEditable(False)
        port = QStandardItem(port)
        port.setEditable(False)
        time = QStandardItem(str(time.replace(microseconds=0)))
        time.setEditable(False)
        table_list.appendRow([user, ip, port, time])
    return table_list


def create_stat_table(database):
    list_history = database.message_history()
    list_table = QStandardItemModel()
    list_table.setHorizontalHeaderLabels(
        ['Имя клиента',
         'Последний вход',
         'Отправлено сообщений'
         'Получено сообщений'])
    for row in list_history:
        user, last_seen, sent, recvd = row
        user = QStandardItem(user)
        last_seen = QStandardItem(str(last_seen.replace(microseconds=0)))
        sent = QStandardItem(str(sent))
        recvd = QStandardItem(str(recvd))
        user.setEditable(False)
        last_seen.setEditable(False)
        sent.setEditable(False)
        recvd.setEditable(False)
        list_table.appendRow([user, last_seen, sent, recvd])
    return list_table


if __name__ == '__main__':
    app = QApplication(sys.argv)
    application = ServerWindowMain()
    test_user_list = QStandardItemModel(application)
    test_user_list.setHorizontalHeaderItem(0, QStandardItem('Имя клиента'))
    test_user_list.setHorizontalHeaderItem(1, QStandardItem('IP-адрес'))
    test_user_list.setHorizontalHeaderItem(2, QStandardItem('Порт'))
    test_user_list.setHorizontalHeaderItem(3, QStandardItem('Время подключения'))
    test_user_list.appendRow([QStandardItem('test_user_1'),
                              QStandardItem('192.155.14.22'),
                              QStandardItem('7221'),
                              QStandardItem('22:14:38'),
                              ])
    test_user_list.appendRow([QStandardItem('test_user_2'),
                              QStandardItem('192.155.14.23'),
                              QStandardItem('7221'),
                              QStandardItem('22:14:39'),
                              ])
    application.ui.active_clients_tableView.setModel(test_user_list)
    sys.exit(app.exec_())
