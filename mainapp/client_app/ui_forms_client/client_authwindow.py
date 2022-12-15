"""
File is part of client's part of messenger,
created during completing practical task
for lesson_6 course DB_and_PyQt.
by Maksim Sapunov, Jenny6199@yandex.ru
december, 2022. GeekBrains
"""
# Created by: PyQt5 UI code generator 5.15.7


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, qApp, QLabel, QPushButton, QLineEdit
import sys


class UiClientAuthWindowForm(object):
    """Класс для отображения виджета авторизации пользователя"""
    def setupUi(self, auth_widget):
        """Настройка отображения виджета авторизации"""
        # Общие настройки окна
        auth_widget.setObjectName("auth_widget")
        auth_widget.resize(203, 222)
        auth_widget.setMinimumSize(QtCore.QSize(203, 222))
        auth_widget.setMaximumSize(QtCore.QSize(203, 222))
        auth_widget.setMouseTracking(False)

        # Строка ввода имени пользователя
        self.name_input = QLineEdit(auth_widget)    # QTextEdit(auth_widget)
        self.name_input.setGeometry(QtCore.QRect(10, 40, 181, 31))
        self.name_input.setObjectName("name_input")

        # Строка ввода пароля
        self.pass_input = QLineEdit(auth_widget)    # QTextEdit(auth_widget)
        self.pass_input.setGeometry(QtCore.QRect(10, 110, 181, 31))
        self.pass_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pass_input.setObjectName("pass_input")

        # Надпись над строкой ввода имени пользователя
        self.label = QLabel(auth_widget)
        self.label.setGeometry(QtCore.QRect(10, 10, 181, 21))
        self.label.setObjectName("label")

        # Надпись над строкой ввода пароля
        self.label_2 = QLabel(auth_widget)
        self.label_2.setGeometry(QtCore.QRect(10, 80, 181, 17))
        self.label_2.setObjectName("label_2")

        # Кнопка "начать"
        self.start_push_button = QPushButton(auth_widget)
        self.start_push_button.setGeometry(QtCore.QRect(8, 180, 91, 25))
        self.start_push_button.setShortcut("")
        self.start_push_button.setObjectName("start_push_button")

        # Кнопка "отмена"
        self.cancel_push_button = QPushButton(auth_widget)
        self.cancel_push_button.setGeometry(QtCore.QRect(110, 180, 81, 25))
        self.cancel_push_button.setShortcut("")
        self.cancel_push_button.setObjectName("cancel_push_button")

        # Вызываем функцию настройки отображения текста
        self.retranslateUi(auth_widget)

    def retranslateUi(self, auth_widget):
        """Настройка отображения текста"""
        _translate = QtCore.QCoreApplication.translate
        auth_widget.setWindowTitle(_translate("auth_widget", "Авторизация"))
        self.label.setText(_translate("auth_widget", "Имя пользователя:"))
        self.label_2.setText(_translate("auth_widget", "Пароль:"))
        self.start_push_button.setText(_translate("auth_widget", "Старт!"))
        self.cancel_push_button.setText(_translate("auth_widget", "Отмена"))


class ClientAuthWindow(QDialog):
    """Класс для отображения виджета авторизации пользователя"""
    def __init__(self):
        super(ClientAuthWindow, self).__init__()
        self.ui = UiClientAuthWindowForm()
        self.ui.setupUi(self)
        self.start_pressed = False
        self.ui.start_push_button.clicked.connect(self.press_start_button)
        self.ui.cancel_push_button.clicked.connect(qApp.quit)
        self.show()

    def press_start_button(self):
        """Обработчик нажатия кнопки 'начать'"""
        if self.ui.name_input.text() and self.ui.pass_input.text():
            self.start_pressed = True
            # print(self.ui.name_input.text(), self.ui.pass_input.text())
            qApp.exit()


if __name__ == '__main__':
    # Запуск и отладка
    app = QApplication(sys.argv)
    application = ClientAuthWindow()
    sys.exit(app.exec_())
