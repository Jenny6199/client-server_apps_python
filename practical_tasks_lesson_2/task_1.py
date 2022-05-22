"""
Практическое задание к уроку №2 'Клиент-серверные приложения на Python
Студент: Максим Сапунов Jenny6199@yandex.ru
Преподаватель: Илья Барбылев

Задание: Создать функцию get_data(), в которой в цикле осуществляется
перебор файлов с данными и считывание данных. В этой функции из считанных
данных необходимо с поомщью регулярных выражений извлечь значения параметров
"Изготовитель системы", "Название системы", "Название ОС", "Код продукта",
"Тип системы".
Значения каждого параметра поместить в соответствующий список.
Должно получиться четыре списка - например, os_prod_list, os_name_list,
os_code_list, os_type_list. В этой же функции создать главный список для
хранения данных отчета - например, main_data - и поместить в него названия
столбцов отчета в виде списка "Изготовитель системы", "Название системы",
"Название ОС", "Код продукта", "Тип системы".
Значения для других столбцов также оформить в виде списка и поместить
в файл main_data (также для каждого файла).
"""


import csv
from os import environ
import pwd
from chardet import detect


# Входящие данные:
INPUT_DATA = [
    '/input_data/info_1.txt',
#    '/input_data/info_2.txt',
#    '/input_data/info_3.txt',
]


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
    return result


def get_data_form_file(path, code):
    """
    Открывает указанный файл в заданной кодировке и 
    возвращает полученные данные в виде вложенных списков.
    :param - path:str path to file,
    :param - code:str encoding
    """
    with open(path, 'r+t', encoding=code) as f_d:
        try:
            content = f_d.readlines()
            export_data = []
            for row in content:
                data = row.rsplit(sep=':')
                work_list = [el.strip() for el in data]
                export_data.append(work_list)
        except TypeError or UnicodeDecodeError:
            print(f'Ошибка декодирования {path}')
    return export_data


def run(file_list: list):
    """
    :param file_list: list
    """
    for datafile in file_list:
        try:
            path = environ.get('PWD') + datafile 
            code = get_encoding(path)
            extract_data = get_data_form_file(path=path, code=code)
            with open('result.csv', 'w') as w_f:
                w_f_write = csv.writer(w_f)
                for row in extract_data:
                    w_f_write.writerow(row)
        except FileNotFoundError:
            print(f'Не найден файл: {datafile}')
    return


if __name__ == '__main__':
    run(INPUT_DATA)
