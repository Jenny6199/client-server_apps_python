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
from common.variables import DEFAULT_IP, ENCODING_METHOD, RESPONSE, ERROR, PORT_LISTEN


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

    def recv(self, lenght):
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
    def setUp(self):
        """Настройка тестов"""
        pass

    def tearDown(self):
        """Выполнить завершающие действия"""
        print(f'log: Успешное завершение теста: {self.__str__()}')
    
    def test_send_response_right_message(self):
        """Тестирование функции с корректным сообщением"""
        test_socket = TestSocket(right_message)
        send_response(test_socket, right_message)
        self.assertEqual(
            test_socket.encoded_message, 
            test_socket.received_message
        )

    def test_send_response_with_empty_message(self):
        """Тестирование функции с некорректным (пустым) сообщением"""
        test_socket = TestSocket(right_message)
        with self.assertRaises(TypeError):
            send_response(test_socket, '')


class TestGetResponse(unittest.TestCase):
    """Тестирование функции get_response"""
    def setUp(self):
        """Настройка тестов"""
        pass

    def tearDown(self):
        """Выполнить завершающие действия"""
        print(f'log: Успешное завершение теста: {self.__str__()}')
    
    def test_get_response_correct_message(self):
        """
        Тестирование функции get_response с корректным сообщением
        """
        test_socket = TestSocket(response_ok)
        self.assertEqual(get_response(test_socket), response_ok)

    
    def test_get_response_wrong_message(self):
        """
        Тестирование функции get_response c ошибочным сообщением
        """
        test_soket = TestSocket(response_error)
        self.assertEqual(get_response(test_soket), response_error)


class TestGetPortAndAddressForUse(unittest.TestCase):
    """Тестирование функции get_port_and_address_for_use"""
    def setUp(self):
        """Настройка тестов"""
        pass

    def tearDown(self):
        """Выполнить завершающие действия"""
        print(f'log: Успешное завершение теста: {self.__str__()}')
    
    def test_result_is_tuple(self):
        """Проверка типа возвращаемых данных"""
        self.assertIsInstance(get_port_and_address_for_use('server'), tuple)
        
    def test_default_port(self):
        """Проверка возвращаемого значения по умолчанию"""
        self.assertEqual(get_port_and_address_for_use('client')[1], int(PORT_LISTEN))
    
    def test_check_result(self):
        """
        Проверяет совпадение значений при вызове функции 
        без указания параметров в комманой строке
        """
        self.assertEqual(get_port_and_address_for_use('client'), (DEFAULT_IP, int(PORT_LISTEN)))


if __name__ == '__main__':
    unittest.main()
