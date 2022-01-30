# python3

import socket
import shutil
import os

serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
IP = socket.gethostbyname(socket.gethostname())
serv_sock.bind((IP, 53210))
serv_sock.listen(10)
print(IP)

while True:
    # Бесконечно обрабатываем входящие подключения
    client_sock, client_addr = serv_sock.accept()
    print('Connected by', client_addr)

    while True:
        # Пока клиент не отключился, читаем передаваемые
        # им данные и отправляем их обратно
        data = client_sock.recv(1024)
        read = data.decode("utf8")
        get_inf = read.split(' ')
        for users in range(0, 100):
            user = ('user%s' % users)
            if get_inf[0] == user:
                print('user be')
                file_password = 'users/%s/password.txt' % get_inf[0]
                read_password = open(file_password, 'r').read()
                if get_inf[1] == read_password:
                    print('password corectly')
                    file_hwid = 'users/%s/hwid.txt' % get_inf[0]
                    read_hwid = open(file_hwid, 'r').read()
                    if get_inf[2] == read_hwid:
                        print('hwid corectly')
                        client_sock.sendall('True'.encode('utf8'))
                    elif read_hwid == "":
                        print('has not hwid')
                        hwid = 'users/%s/hwid.txt' % get_inf[0]
                        wr = open(hwid, 'w')
                        wr.write(get_inf[2])
                        wr.close()
                        client_sock.sendall('Hwid reserved'.encode('utf8'))
                    else:
                        print('incorectly hwid')
                        hwid = 'users/%s/hwid.txt' % get_inf[0]
                        hwid_cound = 'users/%s/hwid_cound.txt' % get_inf[0]
                        wr = open(hwid, 'w')
                        wr.write(get_inf[2])
                        wr.close()
                        wrcr = open(hwid_cound).read()

                        if wrcr > '7':
                            shutil.rmtree('users/%s' % get_inf[0], ignore_errors=True)
                            client_sock.sendall('user was deleted'.encode('utf8'))
                        elif wrcr == '':
                            wrc = open(hwid_cound, 'w')
                            wrcr = 0
                            cound = str(int(wrcr) + 1)
                            p = wrc.write(cound)
                            wrc.close()
                            client_sock.sendall('Hwid reload'.encode('utf8'))
                        else:
                            wrc = open(hwid_cound, 'w')
                            cound = str(int(wrcr) + 1)
                            p = wrc.write(cound)
                            wrc.close()
                            client_sock.sendall('Hwid reload'.encode('utf8'))

                else:
                    print('password incorectly')
                    client_sock.sendall('пароль введен не правильно'.encode('utf8'))
            else:
                if users >= 99:
                    print('login incorectly')
                    client_sock.sendall('логин введен не правильно'.encode('utf8'))

        if not data:
            # Клиент отключился
            break

        break
    client_sock.close()