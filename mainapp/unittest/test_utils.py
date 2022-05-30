"""
Тестирование функций используемых как клиентской так и серверной
частями программы.
"""

import unittest

# Обеспечиваем доступность пути к корню проекта
import sys
import os
import json
sys.path.append(os.path.join(os.getcwd(), '..'))

from common.utils import send_response, get_port_and_address_for_use
from common.variables import ENCODING_METHOD, RESPONSE, ERROR


class TestSocket:
    """Имитация работы сокета"""
    def __init__(self, message):
        self.message = message
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

    def recv(self):
        """
        Тестовая функция, имитирующая получение значений
        из сокета.
        """
        json_test_message = json.dumps(self.message)
        return json_test_message.encode(ENCODING_METHOD)


class TestSendResponse(unittest.TestCase):
    """
    Тестирование функции send_response
    """

    right_message = {
        'action': 'presence',
        # 'time': 'Mon May 30 01:10:47 2022',
        'user': {'account_name': 'Guest'}
    }

    response_ok = {
        RESPONSE: 200
    }

    response_error = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }

    def test_send_response_right_message(self):
        """Тестирование функции с корректным сообщением"""
        test_socket = TestSocket(self.right_message)
        test_socket.send(self.right_message)
        test_socket.encoded_message = test_socket
        self.assertEqual(test_socket.encoded_message,
                         test_socket.received_message)


class TestGetPortAndAddressForUse(unittest.TestCase):
    """
    Тестирование функции get_port_and_address_for_use
    """
    DEFAULT_IP = 1000

    def test_port_exception(self):
        with self.assertRaises(ValueError):
            get_port_and_address_for_use('server')

    def test_return_is_tuple(self):
        self.assertIsInstance(
            get_port_and_address_for_use('server'),
            tuple
        )


if __name__ == '__main__':
    unittest.main()
