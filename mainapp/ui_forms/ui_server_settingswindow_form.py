from PyQt5 import QtCore, QtWidgets


class Ui_Server_settings(object):

    def setupUi(self, Server_settings):
        """
        Содержит настройки виджета
        """
        Server_settings.setObjectName("Server_settings")
        Server_settings.resize(400, 300)

        # Строка ввода 1 "путь к файлу базы данных"
        self.lineEdit = QtWidgets.QLineEdit(Server_settings)
        self.lineEdit.setGeometry(QtCore.QRect(10, 40, 281, 21))
        self.lineEdit.setObjectName("lineEdit")

        # Ярлык строки ввода 1
        self.label = QtWidgets.QLabel(Server_settings)
        self.label.setGeometry(QtCore.QRect(10, 10, 281, 21))
        self.label.setObjectName("label")

        # Кнопка 1 выбор пути к файлу базы данных.
        self.pushButton = QtWidgets.QPushButton(Server_settings)
        self.pushButton.setGeometry(QtCore.QRect(300, 40, 89, 25))
        self.pushButton.setObjectName("db_path")

        # Строка ввода 2 "имя файла базы данных"
        self.lineEdit_2 = QtWidgets.QLineEdit(Server_settings)
        self.lineEdit_2.setGeometry(QtCore.QRect(200, 80, 191, 21))
        self.lineEdit_2.setObjectName("db_file_name")

        # Строка ввода 3 "номер порта"
        self.lineEdit_3 = QtWidgets.QLineEdit(Server_settings)
        self.lineEdit_3.setGeometry(QtCore.QRect(200, 120, 191, 21))
        self.lineEdit_3.setObjectName("port_number")

        # Строка ввода 4 "разрешенные ip-адреса"
        self.lineEdit_4 = QtWidgets.QLineEdit(Server_settings)
        self.lineEdit_4.setGeometry(QtCore.QRect(200, 160, 191, 21))
        self.lineEdit_4.setObjectName("ip_access")

        # Кнопка 2 "Закрыть"
        self.pushButton_2 = QtWidgets.QPushButton(Server_settings)
        self.pushButton_2.setGeometry(QtCore.QRect(300, 260, 89, 25))
        self.pushButton_2.setObjectName("pushButton_2")

        # Кнопка 3 "Сохранить"
        self.pushButton_3 = QtWidgets.QPushButton(Server_settings)
        self.pushButton_3.setGeometry(QtCore.QRect(200, 260, 89, 25))
        self.pushButton_3.setObjectName("pushButton_3")

        # Ярлык к строке ввода 2
        self.label_2 = QtWidgets.QLabel(Server_settings)
        self.label_2.setGeometry(QtCore.QRect(10, 80, 171, 21))
        self.label_2.setObjectName("label_2")

        # Ярлык к строке ввода 3
        self.label_3 = QtWidgets.QLabel(Server_settings)
        self.label_3.setGeometry(QtCore.QRect(10, 120, 181, 16))
        self.label_3.setObjectName("label_3")

        # Ярлык к строке ввода 4
        self.label_4 = QtWidgets.QLabel(Server_settings)
        self.label_4.setGeometry(QtCore.QRect(10, 160, 181, 21))
        self.label_4.setObjectName("label_4")

        # Текст примечания
        self.label_5 = QtWidgets.QLabel(Server_settings)
        self.label_5.setGeometry(QtCore.QRect(120, 190, 231, 71))
        self.label_5.setObjectName("label_5")

        self.retranslateUi(Server_settings)

        # присоединение слота close() к кнопке "закрыть"
        self.pushButton_2.clicked.connect(Server_settings.close)    # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Server_settings)

    def retranslateUi(self, Server_settings):
        """
        Задает текст кнопок и ярлыков в приложении
        :param - Server_settings(object)
        """
        _translate = QtCore.QCoreApplication.translate
        Server_settings.setWindowTitle(_translate("Server_settings", "Form"))
        self.label.setText(_translate("Server_settings",
                                      "<html><head/><body>"
                                      "<p><span style=\" font-size:10pt; font-weight:600;\">"
                                      "Путь до файла базы данных"
                                      "</span></p>"
                                      "</body></html>"))
        self.pushButton.setText(_translate("Server_settings", "Обзор..."))
        self.pushButton_2.setText(_translate("Server_settings", "Закрыть"))
        self.pushButton_3.setText(_translate("Server_settings", "Сохранить"))
        self.label_2.setText(_translate("Server_settings",
                                        "<html><head/><body>"
                                        "<p><span style=\" font-size:10pt; font-weight:600;\">"
                                        "Имя файла базы данных"
                                        "</span></p>"
                                        "</body></html>"))
        self.label_3.setText(_translate("Server_settings",
                                        "<html><head/><body>"
                                        "<p><span style=\" font-size:10pt; font-weight:600;\">"
                                        "Изменить номер порта"
                                        "</span></p>"
                                        "<p><span style=\" font-size:10pt; font-weight:600;\">"
                                        "<br/></span></p></body></html>"))
        self.label_4.setText(_translate("Server_settings",
                                        "<html><head/><body>"
                                        "<p><span style=\" font-size:10pt; font-weight:600;\">"
                                        "Разрешенный IP- адрес*"
                                        "</span></p>"
                                        "</body></html>"))
        self.label_5.setText(_translate("Server_settings",
                                        "<html><head/><body>"
                                        "<p align=\"justify\"><span style=\" font-size:9pt;\">"
                                        "прим.*  Чтобы принимать соединения</span></p><p align=\"justify\">"
                                        "<span style=\" font-size:9pt;\">"
                                        "с любых IP-адресов, оставьте это поле</span></p><p align=\"justify\">"
                                        "<span style=\" font-size:9pt;\">"
                                        "пустым.</span></p></body></html>"))

    def open_file_dialog(self):
        global dialog
        dialog = QFileDialog(self)
        pass
