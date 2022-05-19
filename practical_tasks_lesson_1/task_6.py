"""
Практическое задание к уроку №1 курса Клиент-серверные приложения
на Python.
Студент: Максим Сапунов, Jenny6199@yanex.ru
Преподаватель: Илья Барбылев

Задание: Создать текстовый файл test_file.txt, заполнить его тремя строками: 
«сетевое программирование», «сокет», «декоратор». 
Далее забыть о том, что мы сами только что создали этот файл и исходить 
из того, что перед нами файл в неизвестной кодировке. 
Задача: открыть этот файл БЕЗ ОШИБОК вне зависимости от того, в какой 
кодировке он был создан.
"""

import random
from chardet import detect

encode_list = [
    'cp1251',
    'IBM866',
    'utf-8',
]

file_content = 'сетевое программирование\n\rсокет\n\rдекоратор\n\r'

file_path = './test_file.txt'


def create_txt_with_shadow_encoding(path, text, encode_variant):
    """
    Создает текстовый файл в случайной кодировке
    :param - path: str - idicate place where file will be create
    :param - text: str - file content
    :param - encode_variant: list - list with variant of encoding
    """
    random_encode = encode_variant[random.randint(0, len(encode_variant)-1)]
    with open(
        path, 
        'w', 
        encoding=random_encode, 
        buffering=1,
        newline='\n',
    ) as f:
            f.write(text)
    print(f'Создан файл со случайной кодировкой: \n {path}')
    return


def get_encoding(filepath):
    """
    Выполняет тестовое открытие текстового файла и возвращает
    его кодировку
    :param - filepath: str - path to aim file f.e. './test.txt'
    :return - result: str - encoding method f.e. 'cp1251'
    """
    with open(filepath, 'r+b') as f_test:
        test_touch = f_test.read()
        result = detect(test_touch)['encoding']
    print(f'Кодировка файла - {result}')
    return result


def run():
    """Запуск программы"""
    # Создаем файл со случайной кодировкой.
    create_txt_with_shadow_encoding(file_path, file_content, encode_list)
    # Определяем кодировку файла.
    encode_method = get_encoding(file_path)
    # Открываем файл в выбранной кодировке.
    with open(file_path, 'r+t', encoding=encode_method) as f_n:
        text = f_n.read().encode(encode_method).decode('utf-8')
    # Выводим на дисплей его содержимое.
    print(text)


if __name__ == '__main__':
    run()
