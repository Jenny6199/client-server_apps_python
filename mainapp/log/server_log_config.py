"""
Логирование серверной части программы
В процессе работы программы используется два обработчика. 
Реализован вывод сообщений в консоль и запись в log-файл.
"""
import sys
import logging
import logging.handlers
import os

sys.path.append(os.path.join(os.getcwd(), '..'))
from common.variables import ENCODING_METHOD, LOGGING_LEVEL

# Путь к журналу
PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'server.log')

# Регистратор
server_log = logging.getLogger('server')

# Форматтеры
STREAM_FORMATTER = logging.Formatter(
    '%(asctime)-25s %(levelname)-8s %(filename)-15s %(message)5s'
    )
RECORD_FORMATTER = logging.Formatter(
    '%(asctime)-25s %(levelname)-8s %(filename)-15s %(message)5s'
    )

# Обработчики
STREAM_HANDLER = logging.StreamHandler(
    sys.stdout    # Вывод информационных сообщений в консоль.
    )
RECORD_FILE = logging.handlers.TimedRotatingFileHandler(
    PATH,     # Путь к log-файлу.
    encoding=ENCODING_METHOD,  # Кодировка задана в общих настройках.
    interval=1,    # 1-ежедневно, 2-раз в 2 дня, и.т.д.
    when='D',    # S-сек., M-мин., H-час, D-день, W-неделя, midnight-полночь.
    )

# Подключение форматтеров к обработчикам
STREAM_HANDLER.setFormatter(STREAM_FORMATTER)
RECORD_FILE.setFormatter(RECORD_FORMATTER)

# Подключение обработчиков к регистратору
server_log.addHandler(STREAM_HANDLER)
server_log.addHandler(RECORD_FILE)

# Устанавливаем уровни реагирования регистратора.
server_log.setLevel(LOGGING_LEVEL)


if __name__ == '__main__':
    print('Тестовый запуск логера:')
    print(PATH)
    server_log.debug('Отладочная информация')
    server_log.info('Информационное сообщение')
    server_log.warning('Внимание!')
    server_log.error('Ошибка!')
    server_log.critical('Все сломалось!')
