"""
Тестирование функций используемых как клиентской так и серверной
частями программы.
"""

import unittest

# Обеспечиваем доступность пути к корню проекта
import sys
import os
sys.path.append(os.path.join(os.getcwd(), '..'))

from common.utils import send_response
from common.variables import ENCODING_METHOD, RESPONSE,

class TestSocket:
    """Тестовый сокет"""
    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.encoded_message = None
        self.received_message = None

    def send(self, message):
        """
        Тестовая функция, аналог для проверки работы send_response.
        сохраняет данные в переменную для последующей проверки.
        """
        if not isinstance(message, dict):
            raise TypeError
        json_message = json.dumps(message)
        self.encoded_message = json_message.encode(ENCODING_METHOD)
        self.received_message = message


    def recv(self, max_len):
        """Получаем данные из сокета"""
        json_test_message = json.dumps(self.test_dict)
        return json_test_message.encode(ENCODING)


class TestSendResponse(unittest.TestCase):
    """
    Тестирование функции send_response
    """

    right_message = {
        'action': 'presence',
        'time': 'Mon May 30 01:10:47 2022',
        'user': {'account_name': 'Guest'}
    }


if __name__ == '__main__':
    unittest.main()
