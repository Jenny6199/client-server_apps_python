"""
File contents structure of window client history for server
graphical presence. Build by PyQtDesigner and then
edited by author. This work was completed during
educated DB_and_PyQt course lesson 4 by GeekBrains,
Moscow, November 2022.
Maksim_Sapunov, Jenny6199@yandex.ru
"""


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog
import sys


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
        self.tableView.setObjectName("tableView")

        # Ярлык с информацией
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 340, 251, 41))
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        self.pushButton.clicked.connect(Dialog.close) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Статистика клиентов"))
        self.pushButton.setText(_translate("Dialog", "Закрыть"))
        self.label.setText(_translate("Dialog", "Сведения о активности клиентов."))


class ServerWindowHistory(QDialog):
    """doc"""

    def __init__(self):
        super(ServerWindowHistory, self).__init__()
        self.ui = UiServerClientHistoryForm()
        self.ui.setupUi(self)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ServerWindowHistory()
    sys.exit(app.exec_())
