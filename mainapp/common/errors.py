"""Обработка ошибок"""


class DictionaryNotReceived(Exception):
    """
    Ошибка-исключение:
    Полученные данные не являются словарем.
    """
    def __str__(self):
        return 'Данные не являются словарем'


class SenderIndicationError(Exception):
    """
    Ошибка-исключение:
    Указан неверный инициатор вызова функции
    """
    def __str__(self):
        return 'Вызов данной функции могут осуществлять' \
               'или server, или client'


class NonBytesMessage(Exception):
    """
    Ошибка-исключение:
    Получены данные не в байтовом формате.
    """
    def __str__(self):
        return 'Необходимо передать данные в байтовом формате.'


class NonStrData(Exception):
    """
    Ошибка-исключение:
    Получены данные не в строковом формате.
    """
    def __str__(self):
        return 'Ожидалась строка.'


class JsonEncodeError(Exception):
    """
    Ошибка-исключение:
    Ошибка декодирования сообщения.
    """
    def __str__(self):
        return 'Не удалось декодировать сообщение'


class MessageHasNoResponse(Exception):
    """
    Ошибка-исключение.
    Получены некорректные данные.
    """
    def __str__(self):
        return 'Сообщение не содержит необходимых данных.'


class PortNumberError(Exception):
    """
    Попытка выбрать недоступный номер порта.
    """
    def __str__(self):
        return 'Получено недопустимое значение порта.'


class ServerError(Exception):
    """Исключение - ошибка сервера"""
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text


class ReqFieldMissingError(Exception):
    """Ошибка - отсутствует обязательное поле в принятом словаре"""
    def __init__(self, missing_field):
        self.missing_field = missing_field

    def __str__(self):
        return f'В принятом словаре отсутствует обязательное поле {self.missing_field}.'


class IncorrectDataRecivedError(Exception):
    def __str__(self):
        return 'Получено некорректное сообщение от удаленного компьютера'
