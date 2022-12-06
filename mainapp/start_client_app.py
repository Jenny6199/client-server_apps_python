import logging
from mainapp.log import client_log_config
import argparse
import sys
from PyQt5.QtWidgets import QApplication
from mainapp.common.variables import *
from mainapp.common.errors import ServerError
from mainapp.decorators.log_deco import debug_log
from mainapp.client_app.client_database import ClientDatabase
from mainapp.client_app.client_transport import ClientTransport
from mainapp.client_app.ui_forms_client.ui_client_mainwindow_form import ClientWindowMain
from mainapp.client_app.ui_forms_client.client_startwindow_form import ClientStartWindow


CLIENT_LOG = logging.getLogger('client')


@debug_log
def arg_parser():
    """
    Парсер аргументов коммандной строки
    Ожидаются параметры "-a" - ip-address, "-p" - port, "-n" - client_name
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', default=DEFAULT_IP, nargs='?')
    parser.add_argument('-p', default=PORT_LISTEN, type=int, nargs='?')
    parser.add_argument('-n', default=None, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    if not 1023 < namespace.p < 65536:    # Проверка доступности порта
        CLIENT_LOG.critical(f'Попытка запуска клиента с неподходящим номером порта: {namespace.p}.'
                            f'Допустимы адреса с 1024 до 65535. Клиент завершает работу.')
        sys.exit(1)
    return namespace.a, namespace.p, namespace.n    # server_address, server_port, client_name


if __name__ == '__main__':
    server_address, server_port, client_name = arg_parser()
    client_app = QApplication(sys.argv)

    # При отсутствии имени пользователя при запуске приложения
    # откроется стартовое диалоговое окно.
    if not client_name:
        start_dialog = ClientStartWindow()
        client_app.exec_()
        if start_dialog.start_pressed:
            client_name = start_dialog.ui.lineEdit.text()
            print(client_name)
            del start_dialog
        else:
            exit(0)

    CLIENT_LOG.info(f'Запуск клиентского приложения с параметрами: '
                f'адрес сервера - {server_address}, '
                f'порт для подключения - {server_port}, '
                f'имя пользователя - {client_name}.')

    # Database object
    database = ClientDatabase(client_name)

    # Transpot object
    try:
        transport = ClientTransport(server_port, server_address, database, client_name)
    except ServerError as transport_fail:
        print(transport_fail.text)
        exit(1)
    transport.setDaemon(True)
    transport.start()
    print('OK!')
