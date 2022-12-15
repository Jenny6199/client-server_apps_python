""" Переменные."""
# IP-адрес по умолчанию
DEFAULT_IP = '127.0.0.1'
# IP-адреса для сервера
ADDR_LISTEN = ''
# Порт по умолчанию
PORT_LISTEN = '7777'
# Максимальное количество подключений
CONNECTION_LIMIT = 5
# Максимальный размер пакета
PACKAGE_SIZE = 1024
# Кодировка
ENCODING_METHOD = 'utf-8'

# Ключи протокола JIM
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
DESTINATION = 'to'

# Список пользователей
ALLOWED_USERS = [
    'Guest',
    'Maksim',
    'Sergey',
]

# Прочие ключи
PRESENCE = 'presence'
PUBLIC_KEY = 'public_key'
WHOS_HERE = 'show_online_users'
RESPONSE = 'response'
LEAVE_MESSAGE = 'exit'
ERROR = 'error'
MESSAGE = 'message'
MESSAGE_TEXT = 'mess_text'
SENDER = 'sender'
CONTACT_LIST = 'get_contact_list'
ADD_CONTACT = 'add_contact'
DEL_CONTACT = 'del_contact'
LIST_INFO = 'data_list'
USERS_REQUEST = 'get_users'
REMOVE_CONTACT = 'remove'
EXIT = 'exit'
DATA = 'bin'


# Уровень реагирования обработчиков
# CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
LOGGING_LEVEL = 'DEBUG'


# Стандартные словари ответов:
RSP_200 = {
    RESPONSE: 200,
}

RSP_400 = {
    RESPONSE: 400,
    ERROR: None,
}

RSP_202 = {
    RESPONSE: 202,
    LIST_INFO: None,
}

# 205
RESPONSE_205 = {
    RESPONSE: 205
}

# 511
RESPONSE_511 = {
    RESPONSE: 511,
    DATA: None
}

# Переменные для базы данных
SERVER_DB = 'sqlite:///server_app//server_base.db3'
