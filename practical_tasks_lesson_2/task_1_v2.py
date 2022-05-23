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


def get_data(data: list):
    """
    Получает данные из текстового файла формирует список данных
    :return: data_list
    """
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    main_data = []

    for text_data in data:
        code = get_encoding(text_data)
        with open(text_data, 'r', encoding=code) as file_obj:
            content = file_obj.read()

        reg_for_os_prod = re.compile(r'Изготовитель системы:\s*\S*')
        reg_for_os_name = re.compile(r'Windows\s\S*')
        reg_for_os_code = re.compile(r'Код продукта:\s*\S*')
        reg_for_os_type = re.compile(r'Тип системы:\s*\S*')

        os_prod_list.append(reg_for_os_prod.findall(content)[0].split()[2])
        os_name_list.append(reg_for_os_name.findall(content)[0])
        os_code_list.append(reg_for_os_code.findall(content)[0].split()[2])
        os_type_list.append(reg_for_os_type.findall(content)[0].split()[2])

    headers = [
        'Изготовитель системы',
        'Название ОС',
        'Код продукта',
        'Тип системы',
    ]

    main_data.append(headers)

    data_for_rows = [os_prod_list, os_name_list, os_code_list, os_type_list]

    for idx in range(len(data_for_rows[0])):
        line = [row[idx] for row in data_for_rows]
        main_data.append(line)

    print(main_data)


if __name__ == '__main__':
    get_data(INPUT_DATA)
