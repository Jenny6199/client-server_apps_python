"""
include class descriptor for port number
"""
from logging import getLogger
logger = getLogger('server')


class Port:
    def __set__(self, instance, value=7777):
        if not 1023 < value < 65536:
            logger.critical(f'Задан недопустимый номер порта {value}. '
                            f'Выбирайте порт в диапазоне 1024-65535.')
            exit(1)
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name
