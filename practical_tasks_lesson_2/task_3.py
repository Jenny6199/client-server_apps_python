"""
Практическое задание к уроку №2 'Клиент-серверные приложения на Python
Студент: Максим Сапунов Jenny6199@yandex.ru
Преподаватель: Илья Барбылев

Задание: Написать скрипт автоматизирующий сохранение данных в файле
YAML-формата. Для этого:
- подготовить данные для записи в виде словаря, в котором первому ключу
соответствует список, второму целое число, третьему - вложенный словарь,
где значение каждого ключа - это целое число с юникодсимволом, отсутствующим
в кодировке ASCII is None:
"""

import yaml

data_from_recording = {
    'trip': ['Mallorca', 'Parga', 'Limassol'],
    'count': 3,
    'airlines': {'Lufthansa': '300€',
                 'Aeroflot': '500€',
                 'Turkish airlines': '200€'}
}


work_file = './results/task_3.yaml'

with open(work_file, 'w', encoding='utf-8') as yaml_write:
    yaml.dump(data_from_recording, yaml_write, default_flow_style=False, allow_unicode=True, sort_keys=False)
print('Данные записаны в файл!')

with open(work_file, 'r', encoding='utf-8') as yaml_read:
    print(yaml_read.read())
