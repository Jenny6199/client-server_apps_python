"""
Практическое задание к уроку №1 курса Клиент-серверные приложения
на Python.
Студент: Максим Сапунов, Jenny6199@yanex.ru
Преподаватель: Илья Барбылев

Задание: 
- Каждое из слов 'разработка', 'сокет', 'декоратор', 
представить в строковом формате. 
- Проверить тип и содержание соответствующих переменных.
- Затем с помощью онлайн-конвертора преобразовать строковые
представления в формат Unicode и также проверить тип и содержимое
переменных.
"""


data_str = [
    'разработка', 
    'сокет', 
    'декоратор',
    ]


data_unicode = [
    '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430',
    '\u0441\u043e\u043a\u0435\u0442',
    '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440',
    ]


def get_type_of_data(list):
    """
    Принимает список и возвращает словарь значениями
    которого являются типы данных элементов полученного списка.
    param: list[elem1, elem2 ... elem(n)]
    return: dict{elem1: type(elem1), elem2: type(elem2),...} 
    """
    output_data = {}
    for elem in list:
        output_data[elem] = type(elem)
    return output_data


def get_descriptive_output(dict):
    """
    Обеспечивает вывод в терминал информационного сообщения
    param: dict
    return: None
    """
    decor = '-'*20
    print('%22s %16s %22s' %(decor, 'начало сообщения', decor))
    for keys, values in dict.items():
        print('%-18s %-10s' %(keys, values))
    print('%22s %16s %22s' %(decor, 'конец сообщения', decor))
    

def run():
    """Запуск работы программы"""
    dict_1 = get_type_of_data(data_str)
    dict_2 = get_type_of_data(data_unicode)
    get_descriptive_output(dict_1)
    get_descriptive_output(dict_2)


if __name__ == '__main__':
    run()

# Выводы: результате сравнения для символьной записи 
# и записи в формате Unicode получены идентичные значения.
