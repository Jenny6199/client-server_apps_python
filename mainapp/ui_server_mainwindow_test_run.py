"""test start of main window app"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from mainapp.ui_forms.ui_server_mainwindow_form import UiServerMainWindowForm


class ServerWindowMain(QMainWindow):
    """doc"""
    def __init__(self):
        super(ServerWindowMain, self).__init__()
        self.ui = UiServerMainWindowForm()
        self.ui.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    application = ServerWindowMain()
    application.show()
    sys.exit(app.exec_())
