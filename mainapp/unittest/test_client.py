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

    def test_make_presence_message(self):
        """Проверка наличия поля user в сообщении"""
        self.assertEqual(
            'user' in make_presence_message(),
            True
        )
