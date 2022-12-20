# -*- coding: utf-8 -*-
import binascii
# Form implementation generated from reading ui file 'server_add_user.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import sys
import hashlib
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtWidgets import QLabel, QPushButton, QLineEdit, QFrame


class UiServerAddUserForm(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(308, 321)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Fixed,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            Form.sizePolicy().hasHeightForWidth()
        )
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(308, 321))
        Form.setMaximumSize(QtCore.QSize(308, 321))
        Form.setMouseTracking(True)
        # 1. Кнопка регистрация
        self.register_button = QPushButton(Form)
        self.register_button.setGeometry(QtCore.QRect(10, 280, 191, 25))
        self.register_button.setObjectName("register_button")
        # 2. Кнопка отмена
        self.cancel_button = QPushButton(Form)
        self.cancel_button.setGeometry(QtCore.QRect(220, 280, 81, 25))
        self.cancel_button.setObjectName("cancel_button")
        # 3. Поле ввода имени пользователя
        self.username_input = QLineEdit(Form)
        self.username_input.setGeometry(QtCore.QRect(50, 50, 201, 25))
        self.username_input.setMaxLength(50)
        self.username_input.setObjectName("username_input")
        # 4. Поле ввода пароля
        self.password_input = QLineEdit(Form)
        self.password_input.setGeometry(QtCore.QRect(50, 150, 201, 25))
        self.password_input.setMaxLength(100)
        self.password_input.setObjectName("password_input")
        # 5. Поле подтверждения пароля
        self.confirm_password_input = QLineEdit(Form)
        self.confirm_password_input.setGeometry(QtCore.QRect(50, 210, 201, 25))
        self.confirm_password_input.setMaxLength(100)
        self.confirm_password_input.setObjectName("confirm_password_input")
        # 6. Надпись над полем ввода имени пользователя
        self.username_label = QLabel(Form)
        self.username_label.setGeometry(QtCore.QRect(50, 16, 201, 31))
        self.username_label.setObjectName("username_label")
        # 7. Надпись над полем ввода пароля
        self.password_label = QLabel(Form)
        self.password_label.setGeometry(QtCore.QRect(50, 106, 201, 31))
        self.password_label.setObjectName("password_label")
        # 8. Надпись над полем ввода подтверждения пароля
        self.confirm_password_label = QLabel(Form)
        self.confirm_password_label.setGeometry(QtCore.QRect(50, 180, 201, 31))
        self.confirm_password_label.setObjectName("confirm_password_label")
        # 9. Разделитель 1
        self.line = QFrame(Form)
        self.line.setGeometry(QtCore.QRect(10, 90, 291, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        # 10. Разделитель 2
        self.line_2 = QFrame(Form)
        self.line_2.setGeometry(QtCore.QRect(10, 250, 291, 20))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Регистрация пользователя"))
        self.register_button.setText(_translate("Form", "Регистрация"))
        self.cancel_button.setText(_translate("Form", "Отмена"))
        self.username_label.setText(_translate("Form", "Имя пользователя:"))
        self.password_label.setText(_translate("Form", "Пароль"))
        self.confirm_password_label.setText(_translate("Form", "Подтверждение пароля:"))


class ServerAddUser(QDialog):
    """Отображение окна добавления пользователя"""
    def __init__(self, database, server):
        super(ServerAddUser, self).__init__()
        self.ui = UiServerAddUserForm()
        self.ui.setupUi(self)
        self.messages = QMessageBox()
        self.server = server
        self.database = database

        self.ui.register_button.clicked.connect(self.save_data)
        self.ui.cancel_button.clicked.connect(self.close)
        self.show()

    def save_data(self):
        """Метод проверки ввода данных и сохранения в базу данных нового пользователя."""
        if not self.ui.username_input.text():
            self.messages.critical(self, 'Внимание!', 'Не указано имя пользователя!')
            return
        elif not self.ui.password_input.text():
            self.messages.critical(self, 'Внимание!', 'Не указан пароль!')
            return
        elif self.ui.password_input.text() != self.ui.confirm_password_input.text():
            self.messages.critical(self, 'Внимание!', 'Введенные пароли не совпадают')
            return
        elif self.database.check_user(self.client_name.text()):
            self.messages.critical(self, 'Ошибка!', 'Пользователь уже зарегистрирован!')
            return
        else:
            password_bytes = self.ui.password_input.text().encode('utf-8')
            salt = self.ui.username_input.text().lower().encode('utf-8')
            password_hash = hashlib.pbkdf2_hmac(
                'sha512',
                password_bytes,
                salt,
                10000,
            )
            self.database.add_user(
                self.ui.username_input.text(),
                binascii.hexlify(password_hash),
            )
            self.messages.information(
                self, 'Успех!', 'Регистрация пользователя завершена успешно!'
            )
            self.server.service_update_lists()
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ServerAddUser(None, None)
    sys.exit(app.exec_())
