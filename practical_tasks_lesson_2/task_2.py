"""
Практическое задание к уроку №2 'Клиент-серверные приложения на Python
Студент: Максим Сапунов Jenny6199@yandex.ru
Преподаватель: Илья Барбылев

Задание: Есть файл orders в формате JSON с информацией о заказах.
Написать скрипт, автоматизирующий его заполнение данными.
Для этого:
Создать функцию write_order_to_json(), в которую передается 5 параметров
— товар (item), количество (quantity), цена (price), покупатель (buyer), дата (date).
Функция должна предусматривать запись данных в виде словаря в файл orders.json.
При записи данных указать величину отступа в 4 пробельных символа;
Проверить работу программы через вызов функции write_order_to_json() с передачей в нее
значений каждого параметра.
"""
import json


def write_order_to_json(item, quantity, price, buyer, date):
    """
    :param item: str - наименование товара
    :param quantity: int - количество товара
    :param price:  float - цена товара
    :param buyer: str - покупатель
    :param date: str - дата покупки
    :return: None
    """
    order = {
        'item': item,
        'quantity': quantity,
        'price': price,
        'buyer': buyer,
        'date': date
    }

    try:
        # Файл открыт режиме "а" что позволяет добавлять записи.
        with open('./results/task_2_order.csv', 'a', encoding='utf-8') as orders_f:
            json.dump(order, orders_f, sort_keys=True, indent=4)
        print('Данные о заказе успешно сохранены в файл!')
    except FileNotFoundError:
        print('Данные не сохранены!')
    return


if __name__ == '__main__':
    ord_item = input('Введите наименование товара: ')
    ord_quantity = input('Введите количество товара: ')
    ord_price = input('Введите стоимость товара: ')
    ord_buyer = input('Введите покупателя: ')
    ord_date = input('Введите дату покупки: ')

    write_order_to_json(ord_item, ord_quantity, ord_price, ord_buyer, ord_date)
