"""Программа-лаунчер"""

import subprocess

PROCESSES = []

while True:
    ACTION = input('Выберите действие: q - выход, '
                   's - запустить сервер и клиенты, '
                   'x - закрыть все окна: ')

    if ACTION == 'q':
        break
    elif ACTION == 's':
        PROCESSES.append(subprocess.Popen('python start_server_app.py',
                                          creationflags=subprocess.CREATE_NEW_CONSOLE))
        PROCESSES.append(subprocess.Popen('python client.py -n TestUser_1',
                                          creationflags=subprocess.CREATE_NEW_CONSOLE))
        PROCESSES.append(subprocess.Popen('python client.py -n TestUser_2',
                                          creationflags=subprocess.CREATE_NEW_CONSOLE))
        PROCESSES.append(subprocess.Popen('python client.py -n TestUser_3',
                                          creationflags=subprocess.CREATE_NEW_CONSOLE))
    elif ACTION == 'x':
        while PROCESSES:
            VICTIM = PROCESSES.pop()
            VICTIM.kill()
