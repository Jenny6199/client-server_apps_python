"""
File contents structure of main window for server
graphical presence. Build by PyQtDesigner and then
edited by author. This work was completed during
educated DB_and_PyQt course lesson 4 by GeekBrains,
Moscow, November 2022.
Maksim_Sapunov, Jenny6199@yandex.ru
"""

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import qApp
# from ui_forms.ui_server_settingswindow_form import ServerWindowSettingsForm


class UiServerMainWindowForm(object):
    """
    Class contents form for server part of messenger.
    Created by QtDisigner.
    """
    def setupUi(self, ServerMainWindow):
        """
        Base filling of main window form.
        Created automaticaly by QtDisigner and then edited and
        commented.
        """
        ServerMainWindow.setObjectName("ServerMainWindow")
        ServerMainWindow.resize(635, 602)
        # CentralWidget
        self.centralwidget = QtWidgets.QWidget(ServerMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.show()

        # VerticalWidget
        self.verticalWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalWidget.setGeometry(QtCore.QRect(10, 70, 611, 271))
        self.verticalWidget.setObjectName("verticalWidget")

        # Verticallayout
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        # Line 1
        self.line = QtWidgets.QFrame(self.verticalWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        # VerticalLayout_2
        self.verticalLayout.addWidget(self.line)
        self.label = QtWidgets.QLabel(self.verticalWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.tableView = QtWidgets.QTableView(self.verticalWidget)
        self.tableView.setEnabled(True)
        self.tableView.setObjectName("tableView")
        self.verticalLayout.addWidget(self.tableView)

        # Line_2
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(10, 340, 611, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")

        # HorizontalLayout
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
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

        # 3 Log
        self.button_log = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.button_log.setObjectName("button_log")
        self.horizontalLayout_3.addWidget(self.button_log)

        # 4 Settings
        self.button_settings = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.button_settings.setObjectName("button_settings")
        self.horizontalLayout_3.addWidget(self.button_settings)
        # self.button_settings.clicked.connect(ServerWindowSettingsForm())

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
