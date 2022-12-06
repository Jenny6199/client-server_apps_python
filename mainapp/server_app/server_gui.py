"""Создание таблиц для отображения в окнах программы"""

import sys
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, \
    QLabel, ,QDialog, QPushButton, QLineEdit, QFileDialog, QMessageBox
from PyQt5.QtGui import  QStandardItem, QStandardItemModel
from PyQt5.QtCore import Qt
import os

def gui_create_model(database):
    """
    Подготавливает для отображения список активных пользователей
    :param - database
    :return - table_view
    """
    list_users = database.active_users_list()
    table_view = QStandardItemModel()
    table_view.setHorizontalHeaderLabels(['Имя клиента', 'Ip-адресс', 'Порт', 'Время подключения'])
    for row in list_users:
        user, ip, port, conn_time = row
        user = QStandardItem(user)
        user.setEditable(False)
        ip = QStandardItem(ip)
        ip.setEditable(False)
        port = QStandardItem(str(port))
        port.setEditable(False)
        time = QStandardItem(str(conn_time.replace(microsecond=0)))
        time.setEditable(False)
        table_view.appendRow([user, ip, port, time])
    return table_view


def gui_create_stat_model(database):
    pass
