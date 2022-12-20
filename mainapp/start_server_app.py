# Консольный мессенджер
# Серверная часть программы. v 0.2.2
# Продолжение работы над проектом на курсе
# "Базы данных и PyQt", Geekbrains
# Преподаватели: Сергей Акопович Акопян, Барбылев Илья.
# Автор: Максим Сапунов, Jenny6199@yandex.ru
# Москва, 2022

import argparse
import sys
import os
import threading
import configparser
from common.variables import PORT_LISTEN
import logging
from decorators.log_deco import debug_log
from mainapp.server_app.db_builder.server_data_base import ServerDB
from mainapp.server_app.server_core import MessageProcessor
from PyQt5.QtWidgets import QApplication
from mainapp.server_app.ui_forms_server.ui_server_mainwindow_form import ServerWindowMain

# Инициализация журнала логирования сервера.
SERVER_LOG = logging.getLogger('server')
# Флаги
new_connection = False
conflag_lock = threading.Lock()


def arg_parser(default_port=PORT_LISTEN, default_address=''):
    """
    Парсер аргументов коммандной строки.
    :param default_port: порт по умолчанию
    :param default_address:  ip-адресс по умолчанию
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=default_port, type=int, nargs='?')
    parser.add_argument('-a', default=default_address, nargs='?')
    parser.add_argument('--no_gui', action='store_true')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p
    gui_flag = namespace.no_gui
    SERVER_LOG.info('Обработка аргументов коммандной строки прошла успешно.')
    return listen_address, listen_port, gui_flag


@debug_log
def config_load():
    """
    функция обеспечивает обработку конфигурационного файла
    для сервера.
    """
    config = configparser.ConfigParser()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config.read(f"{dir_path}/server_app/{'server.ini'}")
    if 'SETTINGS' in config:
        return config
    else:
        config.add_section('SETTINGS')
        config.set('SETTINGS', 'Default_port', str(PORT_LISTEN))
        config.set('SETTINGS', 'Listen_Address', '')
        config.set('SETTINGS', 'Database_path', '')
        config.set('SETTINGS', 'Database_file', 'server_database.db3')
        return config


@debug_log
def main():
    """Основной цикл работы сервера"""
    # Загрузка файла конфигурации сервера
    config = config_load()

    # Загрузка параметров командной строки, если нет параметров, то задаём
    # значения по умоланию.
    listen_address, listen_port, gui_flag = arg_parser(
        config['SETTINGS']['Default_port'],
        config['SETTINGS']['Listen_Address'],
    )

    # Инициализация базы данных
    database = ServerDB()

    # Создание экземпляра класса - сервера и его запуск:
    server = MessageProcessor(listen_address, listen_port, database)
    server.daemon = True
    server.start()

    # Если  указан параметр без GUI то запускаем простенький обработчик
    # консольного ввода
    if gui_flag:
        while True:
            command = input('Введите exit для завершения работы сервера.')
            if command == 'exit':
                # Если выход, то завршаем основной цикл сервера.
                server.running = False
                server.join()
                break
    else:
        # Создаём графическое окуружение для сервера:
        server_app = QApplication(sys.argv)
        main_window = ServerWindowMain(database, server, config)
        server_app.exec_()
        server.running = False


if __name__ == '__main__':
    main()
