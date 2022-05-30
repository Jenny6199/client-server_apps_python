import unittest

# Обеспечиваем доступность пути к корню проекта
import sys
import os
sys.path.append(os.path.join(os.getcwd(), '..'))
from server import prepare_response


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

    def test_with_right_message(self):
        """Тестирование функции c правильным сообщением."""
        self.assertEqual(prepare_response(self.right_message)['response'], 200)

    def test_with_wrong_message(self):
        """Тестирование функции с ошибочным сообщением."""
        self.assertEqual(prepare_response(self.wrong_message)['response'], 400)


if __name__ == '__main__':
    unittest.main()
