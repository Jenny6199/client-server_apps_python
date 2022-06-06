import logging
import sys
import traceback


def debug_log(func):
    """Обеспечивает логирование функций используемых в программе"""
    def wrap(*args, **kwargs):
        """Функция-обертка"""
        logger_type = 'server' if 'server.py' in sys.argv[0] else 'client'
        logger = logging.getLogger(logger_type)
        result = func(*args, **kwargs)
        func_name = f'Вызов функции {func.__name__} с параметрами {args}, {kwargs}. \n'
        func_module = f'Вызов осуществлен из модуля {func.__module__}. \n'
        func_caller = f'Вызов осуществлен из функции {traceback.format_stack()[0].strip().split()[-1]}. \n'
        logger.debug('\n %s %s %s' % (func_name, func_module, func_caller))
        return result
    return wrap
