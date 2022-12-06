import logging
import sys
import traceback


def debug_log(func):
    """Обеспечивает логирование функций используемых в программе"""
    def wrap(*args, **kwargs):
        """Функция-обертка"""
        logger_type = 'server' if 'start_server_app.py' in sys.argv[0] else 'client'
        logger = logging.getLogger(logger_type)
        func_name = f'Вызов функции {func.__name__}.'
        func_module = f'Из модуля {func.__module__}.'
        func_caller = f'Из из функции {traceback.format_stack()[0].strip().split()[-1]}.'
        func_params = f'Параметры: {args}, {kwargs}'
        logger.debug('%s %s %s %s' % (func_name, func_module, func_caller, func_params))
        result = func(*args, **kwargs)
        return result
    return wrap
