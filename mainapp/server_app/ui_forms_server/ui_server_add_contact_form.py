"""Виджет - добавление контактов для пользователя"""


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog
import sys


class UiServerAddContactForm(object):
    """Класс отображения окна добавления контактов"""
    def setupUi(self, ui_server_add_contact_form):
        """Настройки окна - добавление контактов."""
        ui_server_add_contact_form.setObjectName("ui_server_add_contact_form")
        ui_server_add_contact_form.resize(450, 150)
        ui_server_add_contact_form.setMinimumSize(QtCore.QSize(450, 150))
        ui_server_add_contact_form.setMaximumSize(QtCore.QSize(450, 450))
        ui_server_add_contact_form.setModal(True)
        self.gridLayout = QtWidgets.QGridLayout(ui_server_add_contact_form)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(ui_server_add_contact_form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.scrollArea = QtWidgets.QScrollArea(ui_server_add_contact_form)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 341, 107))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.listWidget = QtWidgets.QListWidget(self.scrollAreaWidgetContents)
        self.listWidget.setGeometry(QtCore.QRect(0, 0, 341, 111))
        self.listWidget.setObjectName("listWidget")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 1, 0, 1, 1)
        self.buttons_block = QtWidgets.QDialogButtonBox(ui_server_add_contact_form)
        self.buttons_block.setOrientation(QtCore.Qt.Vertical)
        self.buttons_block.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttons_block.setObjectName("buttons_block")
        self.gridLayout.addWidget(self.buttons_block, 1, 1, 1, 1)

        self.retranslateUi(ui_server_add_contact_form)
        self.buttons_block.accepted.connect(ui_server_add_contact_form.accept)  # type: ignore
        self.buttons_block.rejected.connect(ui_server_add_contact_form.close)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(ui_server_add_contact_form)

    def retranslateUi(self, ui_server_add_contact_form):
        """Переименование элементов виджета"""
        _translate = QtCore.QCoreApplication.translate
        ui_server_add_contact_form.setWindowTitle(_translate(
            "ui_server_add_contact_form",
            "Добавить в список контактов"))
        self.label.setText(_translate(
            "ui_server_add_contact_form",
            "Выбор пользователя для добавления:"))


class ServerAddContact(QDialog):
    """Отображение окна добавления контактов"""
    def __init__(self):
        super(ServerAddContact, self).__init__()
        self.ui = UiServerAddContactForm()
        self.ui.setupUi(self)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ServerAddContact()
    sys.exit(app.exec_())
