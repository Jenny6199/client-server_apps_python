"""Тестирование серверной части программы"""

import unittest

# Обеспечиваем доступность пути к корню проекта
import sys
import os
sys.path.append(os.path.join(os.getcwd(), '..'))
# PyCharm грубо ругается на пути и переменные, импорт но продолжает работать :)
from server import prepare_response
from common.variables import RESPONSE, ERROR


class TestPrepareResponse(unittest.TestCase):
    """
    Класс для тестирования функции prepare response
    в серверной части программы.
    """

    right_message = {
        'action': 'presence',
        'time': 'Mon May 30 01:10:47 2022',
        'user': {'account_name': 'Guest'}
    }

    wrong_message = {
        'hello': 'world',
        'time': '12:10:54 05/05/2022',
        'user': {'name': 'Maksim'}
    }

    error_result = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }

    def setUp(self):
        """Настройка тестов"""
        pass

    def tearDown(self):
        """Выполнить завершающие действия"""
        print('log: Успешное завершение теста.')

    def test_response_not_None(self):
        """
        Проверка, что результат работы функции не None
        """
        self.assertIsNotNone(
            prepare_response(self.right_message)
        )

    def test_response_is_json(self):
        """
        Проверка, что результат работы функции - словарь (json)
        """
        self.assertIsInstance(
            prepare_response(self.right_message),
            dict
        )

    def test_with_right_message(self):
        """
        Тестирование функции c правильным сообщением.
        """
        self.assertEqual(
            prepare_response(self.right_message)['response'],
            200
        )

    def test_with_wrong_message(self):
        """
        Тестирование функции с ошибочным сообщением.
        """
        self.assertEqual(
            prepare_response(self.wrong_message)['response'],
            400
        )

    def test_return_error(self):
        """
        Проверка возврата функцией ошибочного ответа
        при получении неправильных данных
        """
        self.assertEqual(
            prepare_response(self.wrong_message),
            self.error_result
        )


if __name__ == '__main__':
    unittest.main()
