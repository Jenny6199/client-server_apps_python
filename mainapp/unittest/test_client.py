"""Тестирование клиентской части программы"""

import unittest

# Обеспечиваем доступность пути к корню проекта
import sys
import os
sys.path.append(os.path.join(os.getcwd(), '..'))

from client import create_presence_message, exam_server_message
from common.variables import RESPONSE, ACTION, PRESENCE, USER, ACCOUNT_NAME
from common.errors import MessageHasNoResponse


class TestClient(unittest.TestCase):
    """
    Тестирование функций клиентской части программы.
    """

    def setUp(self):
        """Настройка тестов"""
        pass

    def tearDown(self):
        """Выполнить завершающие действия"""
        print(f'log: Успешное завершение теста: {self.__str__()}')

    def test_create_presence_message(self):
        """Проверка наличия полей user и action в сообщении"""
        self.assertEqual(
            'action' in create_presence_message(),
            'user' in create_presence_message(),
            True
        )

    def test_exam_server_message(self):
        """
        Проверка генерации исключения функцией exam_sever_message
        при получении ошибочного сообщения.
        """
        msg = ''
        with self.assertRaises(MessageHasNoResponse):
            exam_server_message(msg)

    def test_exam_server_message_with_right_message(self):
        """
        Проверка работы функции с корректным сообщением.
        """
        msg = {RESPONSE: 200}
        self.assertEqual(
            exam_server_message(msg)[RESPONSE],
            200
        )


if __name__ == '__main__':
    unittest.main()
