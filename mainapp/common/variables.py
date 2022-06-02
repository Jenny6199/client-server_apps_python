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

# Список пользователей
ALLOWED_USERS = [
    'Guest',
    'Maksim',
    'Sergey',
]

# Прочие ключи
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'


# Уровень реагирования обработчиков
# CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
LOGGING_LEVEL = 'DEBUG'