"""
Практическое задание к уроку №1 курса Клиент-серверные приложения
на Python.
Студент: Максим Сапунов, Jenny6199@yanex.ru
Преподаватель: Илья Барбылев

Задание:
- Каждое из слов 'class', 'function', 'method' записать в байтовом
типе без преобразования в последовательность кодов (не используя
методы encode и decode) и определить их тип, содержимое и длину
соответствующих переменных.
"""


incoming_data = [
    'class', 
    'function', 
    'method',
    'lambda',
    'interpretator',
]


def get_byte_type(data:list):
    """
    Получает на вход список данными, возвращает
    список данные в котором преобразованы в байтовый
    формат.
    param: list[el1, el2, ...]
    return: list[b'el1', b'el2', ... ]
    """
    return [bytes(elem, encoding = 'utf-8') for elem in data]


def prepeare_information_array(data:list):
    """
    Получает на вход список с данными, возвращает
    данные в виде списка списков, заполненных информацией
    о элементе, его типе и длине.
    param: list
    return list [[elem, type(elem), len(elem)], ...]
    """
    output_data = []
    for elem in data:
        info = []
        info = [elem, type(elem), len(elem)]
        output_data.append(info)
    return output_data


def get_descriptive_output(data):
    """
    Обеспечивает аккуратный вывод информации
    на экран.
    param: list
    return: None
    """
    decor = '-'*20
    print('%22s %16s %22s' %(decor, 'начало сообщения', decor))
    print('%-17s %17s %15s' %('Переменная', 'Тип данных', 'Длина'))
    for elem in data:
        print('%-20s %17s %15d' %(elem[0], elem[1], elem[2]))
    print('%22s %16s %22s' %(decor, 'конец сообщения', decor))


def run():
    """Запуск работы программы"""
    transform_data = get_byte_type(incoming_data)
    data_dict = prepeare_information_array(transform_data)
    get_descriptive_output(data_dict)


if __name__ == '__main__':
    run()
