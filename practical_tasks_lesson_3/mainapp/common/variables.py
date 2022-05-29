""" Переменные."""
<<<<<<< HEAD

# ip-адрес сервера
ADDR_LISTEN = str('')

=======
# IP-адрес по умолчанию
DEFAULT_IP = '127.0.0.1'
# IP-адреса для сервера
ADDR_LISTEN = ''
>>>>>>> c5d01734998cdbfe32fc7b0d33f0b0c0bc579a56
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
