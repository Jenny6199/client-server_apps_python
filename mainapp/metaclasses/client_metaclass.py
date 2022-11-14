import dis


class ClientChecker(type):
    """
    Класс осуществляет проверку клиентской части программы
    при инициализации на предмет наличия блокирующих методов.
    """
    def __init__(cls, clsname, bases, clsdict):
        methods = []
        for func in clsdict:
            try:
                ret = dis.get_instructions(clsdict[func])
            except TypeError:
                pass
            else:
                for i in ret:
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods:
                            methods.append(i.argval)
        for command in ('accept', 'listen', 'socket'):
            if command in methods:
                raise TypeError('Класс использует запрещенные методы!')
        if 'get_response' in methods or 'send_response' in methods:
            pass
        else:
            raise TypeError('Отсутствуют функции работающие с сокетом!')
        super().__init__(clsname, bases, clsdict)
