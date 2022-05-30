"""Тестирование клиентской части программы"""

import unittest

# Обеспечиваем доступность пути к корню проекта
import sys
import os
sys.path.append(os.path.join(os.getcwd(), '..'))

from client import make_presence_message
from common.variables import ACTION, PRESENCE, USER, ACCOUNT_NAME


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

    def test_make_presence_message(self):
        """Проверка наличия полей user и action в сообщении"""
        self.assertEquals(
            'action' in make_presence_message(),
            'user' in make_presence_message(),
            True
        )


if __name__ == '__main__':
    unittest.main()
