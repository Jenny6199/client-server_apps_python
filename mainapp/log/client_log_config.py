"""
Логирование клиентской части программы.
----------------------------------------
К регистратору подключено два обработчика -
1 - для записи log-файла
2 - для вывода сообщений в консоль.
"""

import sys
import logging
import logging.handlers
import os

sys.path.append(os.path.join(os.getcwd(), '..'))
from common.variables import ENCODING_METHOD, LOGGING_LEVEL

# Путь к журналу
PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'client.log')

# Регистратор
client_log = logging.getLogger('client')

# Форматтеры
STREAM_FORMATTER = logging.Formatter(
    '%(asctime)-25s %(levelname)-8s %(filename)5s %(message)5s'
    )
RECORD_FORMATTER = logging.Formatter(
    '%(asctime)-25s %(levelname)-8s %(filename)5s %(message)5s'
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

# Подключаем обработчики к регистратору
client_log.addHandler(STREAM_HANDLER)
client_log.addHandler(RECORD_FILE)

# Устанавливаем уровни реагирования регистратора
client_log.setLevel(LOGGING_LEVEL)


if __name__ == '__main__':
    print('Тестовый запуск логера:')
    print(PATH)
    client_log.debug('Отладочная информация')
    client_log.info('Информационное сообщение')
    client_log.warning('Внимание!')
    client_log.error('Ошибка!')
    client_log.critical('Все сломалось!')
