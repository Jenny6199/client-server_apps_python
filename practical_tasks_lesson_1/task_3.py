"""
Практическое задание к уроку №1 курса Клиент-серверные приложения
на Python.
Студент: Максим Сапунов, Jenny6199@yanex.ru
Преподаватель: Илья Барбылев

Задание:
Определить какие из слов 'attribute', 'функция', 'класс', 'type'
невозможно записать в байтовом типе
"""

data = [
    'attribute',
    'функция', 
    'класс', 
    'type',
    'abraкадабra',
]


class ASCIIException(Exception):
    """Исключение по заданному условию"""
    def __init__(self, string=None):
        self.text = 'contains non ASCII symbols'
        self.string = string


def convert_string_to_bytes(string: str):
    """
    Функция получает строку, проверяет составляющие её
    символы на соответствие ASCII. В случае успеха возвращает
    строку в байтовом виде, в противном случае возвращает
    информационное сообщение о несоответствии.
    param: string - str
    return: b'string' or message
    """
    try:
        for symbol in string:
            if ord(symbol) > 127:
                raise ASCIIException(string)
        return bytes(string, encoding='utf-8')
    except ASCIIException as mr:
        message = f'"{mr.string}" {mr.text}'
        return message


def run():
    """Запуск работы программы"""
    decor = '-'*30
    result = map(convert_string_to_bytes, data)
    print(decor)
    for message in result:
        print('%7s' % message)
    print(decor)


if __name__ == '__main__':
    run()
