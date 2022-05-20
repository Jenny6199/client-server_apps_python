"""
Практическое задание к уроку №1 курса Клиент-серверные приложения
на Python.
Студент: Максим Сапунов, Jenny6199@yanex.ru
Преподаватель: Илья Барбылев

Задание: Преобразовать слова «разработка», «администрирование», 
«protocol», «standard» из строкового представления в байтовое и 
выполнить обратное преобразование (используя методы encode и decode)
"""

data = [
    'разработка',
    'администрирование',
    'protocol',
    'standard',
]


def convert_string_to_bytes(string, encode_type='utf-8'):
    """
    Преобразует строковый объект в байтовый используя
    метод encode.
    param: string - str, строка для преобразования
    param: encode_type - str, тип кодировки (default='utf-8')
    """
    return str.encode(string, encoding=encode_type)


def convert_bytes_to_string(byte_obj, decode_type='utf-8'):
    """
    Преобразует байтовый объект в строковый используя
    метод decode.
    param: byte_obj = byte, байтовый объект
    param: decode_type = str, тип кодировки (default='utf-8')
    """
    return byte_obj.decode(decode_type)


def run():
    """
    Запуск программы
    Выполняется создание списка с конвертированными значениями,
    обратное проовбразование и вывод в терминал полученные значения.
    """
    conversion_data = list(map(convert_string_to_bytes, data))
    reverse_conversation = []
    for elem in conversion_data:
        reverse_conversation.append(convert_bytes_to_string(elem))
    i = 0
    while i != len(conversion_data):
        print('%7s %7s %7s' % (
            data[i],
            conversion_data[i], 
            reverse_conversation[i],
            )
        )
        i += 1


if __name__ == '__main__':
    run()
