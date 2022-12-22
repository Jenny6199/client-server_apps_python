"""
File contents structure of window client history for server
graphical presence. Build by PyQtDesigner and then
edited by author. This work was completed during
educated DB_and_PyQt course lesson 4 by GeekBrains,
Moscow, November 2022.
Maksim_Sapunov, Jenny6199@yandex.ru
"""


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QDialog


class UiServerClientHistoryForm(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 500)
        Dialog.setModal(True)

        # Кнопка закрытия окна
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(160, 460, 89, 25))
        self.pushButton.setObjectName("pushButton")

        # Таблица с данными
        self.tableView = QtWidgets.QTableView(Dialog)
        self.tableView.setGeometry(QtCore.QRect(10, 20, 381, 321))
        self.tableView.setObjectName("active_clients_tableView")

        # Ярлык с информацией
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 340, 251, 41))
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        self.pushButton.clicked.connect(Dialog.close)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Статистика клиентов"))
        self.pushButton.setText(_translate("Dialog", "Закрыть"))
        self.label.setText(_translate("Dialog", "Сведения о активности клиентов."))


class ServerWindowHistory(QDialog):
    """doc"""

    def __init__(self, database):
        super(ServerWindowHistory, self).__init__()
        self.database = database
        self.ui = UiServerClientHistoryForm()
        self.ui.setupUi(self)
        self.show()
        self.create_stat_table()

    def create_stat_table(self):
        """Метод реализующий заполнение таблицы истории пользователей"""
        list_history = self.database.message_history()
        list_table = QStandardItemModel()
        # Заголовки
        list_table.setHorizontalHeaderLabels(
            ['Имя клиента',
             'Последний вход',
             'Отправлено сообщений'
             'Получено сообщений'])
        # Заполняем ячейки данными из БД
        for row in list_history:
            user, last_seen, sent, received = row
            user = QStandardItem(user)
            last_seen = QStandardItem(str(last_seen.replace(microseconds=0)))
            sent = QStandardItem(str(sent))
            received = QStandardItem(str(received))
            # Делаем ячейки нередактируемыми
            user.setEditable(False)
            last_seen.setEditable(False)
            sent.setEditable(False)
            received.setEditable(False)
            list_table.appendRow([user, last_seen, sent, received])
        # Отображаем таблицу в окне приложения
        self.ui.tableView.setModel(list_table)
        self.ui.tableView.resizeColumnsToContents()
        self.ui.tableView.resizeRowsToContents()
