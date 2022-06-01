"""Логирование серверной части программы"""
import sys
import logging

# Регистратор верхнего уровня
surface_log = logging.getLogger('server_log.basic')

# Потоковый обработчик
stream_handler = logging.StreamHandler(sys.stdout)

# Начальный форматтер
surface_formatter = logging.Formatter('%(levelname)-8s %(asctime)-25s %(message)5s')

# Подключение форметтера к обработчику
stream_handler.setFormatter(surface_formatter)

# Подключение обработчика к регистратору
surface_log.addHandler(stream_handler)

# Устанавливаем уровень реагирования регистратора.
surface_log.setLevel(logging.DEBUG)


if __name__ == '__main__':
    print('Тестовый запуск логера:')
    surface_log.debug('Отладочная информация')
    surface_log.info('Информационное сообщение')
    surface_log.warning('Внимание!')
    surface_log.error('Ошибка!')
    surface_log.critical('Все сломалось!')
