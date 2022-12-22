import logging
import argparse
import os.path
import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from mainapp.common.variables import *
from mainapp.common.errors import ServerError
from mainapp.decorators.log_deco import debug_log
from mainapp.client_app.client_database import ClientDatabase
from mainapp.client_app.client_transport import ClientTransport
from mainapp.client_app.ui_forms_client.ui_client_mainwindow_form import ClientWindowMain
# from mainapp.client_app.ui_forms_client.ui_client_startwindow_form import ClientStartWindow
from mainapp.client_app.ui_forms_client.ui_client_authwindow import ClientAuthWindow
from Cryptodome.PublicKey import RSA

CLIENT_LOG = logging.getLogger('client')


@debug_log
def arg_parser():
    """
    Парсер аргументов коммандной строки
    Ожидаются параметры "-a" - ip-address, "-p" - port, "-n" - client_name
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('address', default=DEFAULT_IP, nargs='?')
    parser.add_argument('port', default=PORT_LISTEN, type=int, nargs='?')
    parser.add_argument('-n', '--name', default=None, nargs='?')
    parser.add_argument('-p', '--password', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.address
    server_port = namespace.port
    client_name = namespace.name
    client_passwd = namespace.password

    if not 1023 < namespace.port < 65536:  # Проверка доступности порта
        CLIENT_LOG.critical(f'Попытка запуска клиента с неподходящим номером порта: {namespace.p}.'
                            f'Допустимы адреса с 1024 до 65535. Клиент завершает работу.')
        sys.exit(1)
    return server_address, server_port, client_name, client_passwd


if __name__ == '__main__':
    server_address, server_port, client_name, client_passwd = arg_parser()
    CLIENT_LOG.info(f'Получены аргументы из функции arg_parser - '
                f'{server_address}, {server_port} {client_name} + {client_passwd}')
    client_app = QApplication(sys.argv)

    # При отсутствии имени пользователя при запуске приложения
    # откроется стартовое диалоговое окно.
    if not client_name:
        start_dialog = ClientAuthWindow()
        client_app.exec_()
        if start_dialog.start_pressed:
            client_name = start_dialog.ui.name_input.text()
            print(client_name)
            del start_dialog
        else:
            exit(0)

    CLIENT_LOG.info(f'Запуск клиентского приложения с параметрами: '
                    f'адрес сервера - {server_address}, '
                    f'порт для подключения - {server_port}, '
                    f'имя пользователя - {client_name}.')

    # Загрузка ключей
    dir_path = os.path.dirname(os.path.realpath(__file__))
    key_file = os.path.join(dir_path, f'{client_name}.shadow')
    if not os.path.exists(key_file):    # Если файла нет создаем
        keys = RSA.generate(2048, os.urandom)
        with open(key_file, 'wb') as key:
            key.write(keys.export_key())
        CLIENT_LOG.info(f'Успешно записан ключ для клиента {client_name}')
    else:   # Если файл найден загружаем ключ
        with open(key_file, 'rb') as key:
            keys = RSA.import_key(key.read())
    CLIENT_LOG.info('Ключи загружены успешно')


    # Database object
    database = ClientDatabase(client_name)

    # Transport object
    transport = ClientTransport(server_port, server_address, database, client_name, client_passwd, keys)
    CLIENT_LOG.info('Транспорт - ОК!')
    try:
        transport.setDaemon(True)
        transport.start()
    except ServerError as transport_fail:
        message = QMessageBox()
        message.critical(start_dialog, 'Ошибка сервера!', transport_fail.text)
        exit(1)
    transport.setDaemon(True)
    transport.start()

    del start_dialog

    # MainWindow object
    main_window = ClientWindowMain(database, transport)
    main_window.make_connection(transport)
    main_window.setWindowTitle(f'GeekBrains. Сетевой чат. Клиент - {client_name}.')
    client_app.exec_()

    transport.transport_shutdown()
    transport.join()
    print('Bye!')
