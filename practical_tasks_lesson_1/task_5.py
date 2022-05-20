"""
Практическое задание к уроку №1 курса Клиент-серверные приложения
на Python.
Студент: Максим Сапунов, Jenny6199@yanex.ru
Преподаватель: Илья Барбылев

Задание: Написать код, который выполняет пинг веб-ресурсов yandex.ru, 
youtube.com и преобразовывает результат из байтовового типа данных в
 строковый без ошибок для любой кодировки операционной системы.
"""
import subprocess
import os
import chardet
import locale


SERVERS = [
    '8.8.8.8',
    'yandex.ru',
    'youtube.com',
    '31.31.201.195',
]


def universal_decoding(repeat, aim):
    """
    Запускает утилиту ping к указанному серверу и возвращает
    декодированное сообщение содержащее ответ сервера.
    :param repeat: int number of cycles
    :param aim: str - url
    :return: str - decoding response of server
    """
    try:
        os.environ.get('OS').lower().__contains__('window')
        os_info = '-n'
    except AttributeError:
        os_info = '-c'

    result = ''

    subprocess_ping = subprocess.Popen(
        ['ping', os_info, str(repeat), aim],
        stdout=subprocess.PIPE
    )

    for line in subprocess_ping.stdout:
        encode_method = chardet.detect(line)
        line = line.decode(encode_method['encoding']).encode('utf-8')
        result += line.decode('utf-8')
    return result


def run():
    """Запуск программы"""
    default_encoding = locale.getpreferredencoding()
    print(f'В Вашей системе используется кодировка - {default_encoding}.')
    request_to = (el for el in SERVERS)
    for server in SERVERS:
        print(
            f'Будет произведен обмен данными со следующим сервером: '
            f' {(next(request_to)).upper()}'
        )
        try:
            message = universal_decoding(4, server)
            print(message)
        except TimeoutError:
            print(f'В процессе обмена данными c сервером возникла ошибка!')


if __name__ == '__main__':
    run()
