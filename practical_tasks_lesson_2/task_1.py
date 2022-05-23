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
import re
from os import environ
from chardet import detect


# Входящие данные:
INPUT_DATA = [
    'input_data/info_1.txt',
    'input_data/info_2.txt',
    'input_data/info_3.txt',
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


def extract_data_form_file(path, code):
    """
    Открывает указанный файл в заданной кодировке и 
    возвращает полученные данные в виде списка
    :param - path:str path to file,
    :param - code:str encoding
    """
  
    with open(path, 'r+t', encoding=code) as f_d:
        content = f_d.read()
        data = []

        re_compile = re.compile(r'Изготовитель системы:\s*\S*')
        find_string = re.findall(re_compile, content)
        data.append([el.strip() for el in find_string[0].split(':')][1])
        
        re_compile = re.compile(r'Название ОС:\s*\S*')
        find_string = re.findall(re_compile, content)
        data.append([el.strip() for el in find_string[0].split(':')][1])

        re_compile = re.compile(r'Код продукта:\s*\S*')
        find_string = re.findall(re_compile, content)
        data.append([el.strip() for el in find_string[0].split(':')][1])

        re_compile = re.compile(r'Тип системы:\s*\S*')
        find_string = re.findall(re_compile, content)
        data.append([el.strip() for el in find_string[0].split(':')][1])

    return data


def get_data(file_list: list):
    """
    :param file_list: list
    """
    # Добавляем заголовки
    export_data = [['manufacturer', 'system_name', 'product_code', 'system_type']]
    # Последовательно обрабатываем файлы из списка
    for datafile in file_list:
        path = datafile
        # Определяем кодировку с помощью заготовленной функции. 
        code = get_encoding(path)
        # Добавляем результат поиска совпадений в список с помощью заготовленной функции.
        export_data.append(extract_data_form_file(path=path, code=code))
        # Формируем csv-файл из полученного списка списков (заголовки добавлены ранее)
        with open('result.csv', 'w') as w_f:
            w_f_write = csv.writer(w_f)
            for row in export_data:
                w_f_write.writerow(row)
    print('Создан файл отчета - result.csv')
    return


if __name__ == '__main__':
    get_data(INPUT_DATA)


# Вышеприведнное решение работает, формирует целевой файл csv,
# но в процессе работы отклонился от тех.задания,
# потому решено было исправить в соответствии.
# Было решено сохранить эту реализацию, для демонстрации хода рассуждения 
# при выполнени практической работы.
