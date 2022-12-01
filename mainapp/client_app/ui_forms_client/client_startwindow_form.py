"""
File is part of client's part of messenger,
created during completing practical task
for lesson_5 course DB_and_PyQt.
by Maksim Sapunov, Jenny6199@yandex.ru
november, 2022. GeekBrains
"""

from PyQt5.QtCore import QRect, QSize, QMetaObject, QCoreApplication
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QLineEdit, qApp
import sys


class UiClientStartWindowForm(object):
    def setupUi(self, dialog):
        dialog.setObjectName("dialog")
        dialog.resize(300, 150)
        dialog.setMinimumSize(QSize(200, 100))
        dialog.setMaximumSize(QSize(300, 150))
        dialog.setModal(True)

        # Start button
        self.start_button = QPushButton(dialog)
        self.start_button.setGeometry(QRect(40, 100, 89, 25))
        self.start_button.setObjectName("start_button")

        # Cancel button
        self.cancel_button = QPushButton(dialog)
        self.cancel_button.setGeometry(QRect(170, 100, 89, 25))
        self.cancel_button.setObjectName("cancel_button")

        # Label
        self.label = QLabel(dialog)
        self.label.setGeometry(QRect(50, 10, 201, 31))
        self.label.setObjectName("label")

        # Input line
        self.lineEdit = QLineEdit(dialog)
        self.lineEdit.setGeometry(QRect(30, 40, 241, 31))
        self.lineEdit.setObjectName("lineEdit")

        self.retranslateUi(dialog)
        QMetaObject.connectSlotsByName(dialog)

    def retranslateUi(self, dialog):
        _translate = QCoreApplication.translate
        dialog.setWindowTitle(_translate("dialog", "Давайте начнем!"))
        self.start_button.setText(_translate("dialog", "Начать"))
        self.cancel_button.setText(_translate("dialog", "Выход"))
        self.label.setText(_translate("dialog", "Введите имя пользователя:"))


class ClientStartWindow(QDialog):
    """Класс для отображения виджета стартового диалога"""
    def __init__(self):
        super(ClientStartWindow, self).__init__()
        self.ui = UiClientStartWindowForm()
        self.ui.setupUi(self)
        self.show()

        # Connect
        self.ui.cancel_button.clicked.connect(qApp.quit)
        self.ui.start_button.clicked.connect(self.press_start_button)

    def press_start_button(self):
        """Обработчик нажатия кнопки 'начать'"""
        print('Button start was pressed!')


if __name__ == '__main__':
    # Запуск и отладка
    app = QApplication(sys.argv)
    application = ClientStartWindow()
    sys.exit(app.exec_())
