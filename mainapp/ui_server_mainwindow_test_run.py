"""test start of main window app"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from mainapp.ui_forms.ui_server_mainwindow_form import UiServerMainWindowForm
from PyQt5.QtCore import Qt


class ServerWindowMain(QMainWindow):
    """doc"""
    def __init__(self):
        super(ServerWindowMain, self).__init__()
        self.ui = UiServerMainWindowForm()
        self.ui.setupUi(self)


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
    application.ui.tableView.setModel(test_user_list)
    application.show()
    sys.exit(app.exec_())
