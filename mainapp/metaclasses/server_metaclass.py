import dis
from pprint import pprint


class ServerChecker(type):
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
                    print(i)
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods:
                            methods.append(i.argval)
                    elif i.opname == 'LOAD_METHOD':
                        if i.argval not in methods_2:
                            methods_2.append(i.argval)
                    elif i.opname == 'LOAD_ATTR':
                        if i.argval not in attrs:
                            attrs.append(i.argval)

        # Show creating lists:
        print(20*'-', 'methods', 20*'-')
        pprint(methods)
        print(20*'-', 'methods_2', 20*'-')
        pprint(methods_2)
        print(20*'-', 'attrs', 20*'-')
        pprint(attrs)
        print(50*'-')

        # Check server problem
        if 'connect' in methods:
            raise TypeError('Использование метода connect - запрещено!')
        if not ('SOCK_STREAM' in attrs and 'AF_INET' in attrs):
            raise TypeError('Ошибка в настройках сокета!')

        # Call parent init (type)
        super().__init__(clsname, bases, clsdict)
