import logging
import sys

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QPushButton
from PyQt5.QtCore import Qt

logger = logging.getLogger('client')


class UiClientDelContactDialogForm(object):
    """
    Класс обеспечивает отображение диалогового окна
    'удаление контактов' в клиентской части программы
    'мессенджер'.
    """

    def setupUi(self, del_contact):
        """
        Настройки виджета добавление контакта
        """
        # Size of dialog window
        del_contact.setObjectName("del_contact")
        del_contact.setFixedSize(350, 120)
        del_contact.setWindowTitle("Выбор контакта для добавления")
        del_contact.setAttribute(Qt.WA_DeleteOnClose)
        del_contact.setModal(True)
        self.centralwidget = QWidget(del_contact)
        self.centralwidget.setObjectName("centralwidget")

        # Label_1
        self.label_of_selector = QLabel(self.centralwidget)
        self.label_of_selector.setObjectName("label_of_selector")
        self.label_of_selector.setText("Выбрать контакт: ")
        self.label_of_selector.setFixedSize(200, 20)
        self.label_of_selector.move(10, 10)

        # Selector
        self.selector = QComboBox(self.centralwidget)
        self.selector.setObjectName("selector")
        self.selector.setFixedSize(200, 20)
        self.selector.move(10, 35)

        # Button_1_ok
        self.ok_button = QPushButton(self.centralwidget)
        self.ok_button.setObjectName("ok_button")
        self.ok_button.setText("Удалить")
        self.ok_button.setFixedSize(100, 30)
        self.ok_button.move(230, 20)

        # Button_2_cancel
        self.cancel_button = QPushButton(self.centralwidget)
        self.cancel_button.setObjectName("cancel_button")
        self.cancel_button.setText("Отмена")
        self.cancel_button.setFixedSize(100, 30)
        self.cancel_button.move(230, 60)


class ClientDelContactWindow(QDialog):
    def __init__(self, database, transport):
        super(ClientDelContactWindow, self).__init__()
        self.transport = transport
        self.database = database
        self.ui = UiClientDelContactDialogForm()
        self.ui.setupUi(self)
        self.show()

        # Connect
        self.ui.ok_button.clicked.connect(self.button_del_contact)

    def button_del_contact(self):
        """Обработчик нажатия кнопки удалить контакт"""
        print("Button del_contact pressed!")


if __name__ == '__main__':
    # Тестовый запуск и отладка
    app = QApplication(sys.argv)
    application = ClientDelContactWindow(database=None, transport=None)
    sys.exit(app.exec_())
