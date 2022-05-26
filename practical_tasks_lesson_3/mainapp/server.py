"""Серверная часть программы."""

import json
from socket import *
from common.utils import get_response, send_response, get_port_and_address_for_use
from common.variables import CONNECTION_LIMIT, \
    ACTION, ACCOUNT_NAME, USER, TIME, PRESENCE, RESPONSE, ERROR


def prepare_response(message):
    """
    Подготавливает ответное сообщение
    :param message: сообщение от клиента.
    :return: response: dict
    """
    if ACTION in message \
            and message[ACTION] == PRESENCE \
            and TIME in message \
            and USER in message \
            and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def main():
    """
    Агрегация работы функций и запуск программы-сервера.
    :return:
    """
    # Получаем значения адреса и порта
    server_options = get_port_and_address_for_use()
    # Готовим сокет
    transport = socket(AF_INET, SOCK_STREAM)
    transport.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    transport.bind(server_options)
    # Слушаем порт
    print(f'Ожидание сообщения от {server_options[0]}:{server_options[1]}')
    transport.listen(CONNECTION_LIMIT)

    while True:
        client, client_address = transport.accept()
        try:
            message_from_client = get_response(client)
            print(message_from_client)
            response = prepare_response(message_from_client)
            send_response(client, response)
            client.close()
        except (ValueError, json.JSONDecodeError):
            print('Получено некорректное сообщение от клиента')
            client.close()


if __name__ == '__main__':
    main()
