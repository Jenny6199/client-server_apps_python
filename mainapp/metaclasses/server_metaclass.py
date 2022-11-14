import dis


class ServerChecker(type):
    """
    Класс осуществляет проверку серверной части программы
    на предмет наличия блокирующих методов.
    """
    def __init__(cls, clsname, bases, clsdict):
        methods = []
        methods_2 = []
        attrs = []

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
                    elif i.opname == 'LOAD_METHOD':
                        if i.argval not in methods_2:
                            methods_2.append(i.argval)
                    elif i.opname == 'LOAD_ATTR':
                        if i.argval not in attrs:
                            attrs.append(i.argval)
        # Check server problem
        if 'connect' in methods:
            raise TypeError('Использование метода connect - запрещено!')
        if not ('SOCK_STREAM' in methods and 'AF_INET' in methods):
            raise TypeError('Ошибка в настройках сокета!')

        # Call parent init (type)
        super().__init__(clsname, bases, clsdict)
