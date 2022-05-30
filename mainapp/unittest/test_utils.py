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

from common.utils import send_response, get_response, get_port_and_address_for_use
from common.variables import ENCODING_METHOD, RESPONSE, ERROR


class TestSocket:
    """Имитация работы сокета"""
    def __init__(self, test_message):
        self.test_message = test_message
        self.encoded_message = None
        self.received_message = None

    def send(self, message):
        """
        Тестовая функция, аналог для проверки работы send_response.
        в отличии от send_response не отправляет данные в сокет
        сохраняет данные в переменную для последующей проверки.
        """
        json_test_message = json.dumps(self.test_message)
        self.encoded_message = json_test_message.encode(ENCODING_METHOD)
        self.received_message = message

    def recv(self):
        """
        Тестовая функция, имитирующая получение значений
        из сокета.
        """
        json_test_message = json.dumps(self.test_message)
        return json_test_message.encode(ENCODING_METHOD)


class TestSendResponse(unittest.TestCase):
    """
    Тестирование функции send_response
    """

    right_message = {
        'action': 'presence',
        'time': 'Mon May 30 01:10:47 2022',
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
        send_response(test_socket, self.right_message)
        self.assertEqual(
            test_socket.encoded_message, 
            test_socket.received_message
        )

    def test_send_response_with_empty_message(self):
        """Тестирование функции с некорректным (пустым) сообщением"""
        test_socket = TestSocket(self.right_message)
        with self.assertRaises(TypeError):
            send_response(test_socket, '')


if __name__ == '__main__':
    unittest.main()
