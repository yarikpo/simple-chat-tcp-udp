import socket
from threading import Thread
from colorama import init
from termcolor import colored

init()


host = '127.0.0.1'
host = input(colored('ip: ', 'blue'))
port = 19090

udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_sock.bind((host, port))

tcp_port = 19092
tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # tcp server for creating groups
tcp_sock.bind((host, tcp_port))
tcp_sock.listen(6)

print(colored('[SERVER STARTED]', 'green'))

# udp_sock.listen(6)

groups = ['mainGroup']
clients = {'0.0.0.0':['host', 'mainGroup']}                  # name & name of group

def encrypt(message):                                        # TODO this function will encrypt messages
    return message

def decrypt(message):                                        # TODO this function will decrypt messages
    return message

def groupCreate():
    try:
        global tcp_sock
        while True:
            try:
                conn, addr = tcp_sock.accept()
                data = conn.recv(1024)
                data = data.decode()
                data = decrypt(data)
                exist = False

                data = data[1:]

                print(f'Trying to create group named {data}')
                for gr in groups:
                    if gr == data[1:]:
                        exist = True

                if exist == True:
                    conn.send(colored(b'Rename group, please!!!', 'red'))
                else:
                    groups.append(data)
                    mes = f'[GROUP {data} HAS BEEN CREATED]'
                    mes = encrypt(mes)
                    mes = mes.encode()
                    conn.send(mes)
            except:
                pass
            finally:
                conn.close()
                print(colored('.', 'yellow'))
                for group in groups:
                    print(colored(f'|--> {group}', 'yellow'))
    except:
        try:
            conn.close()
        except:
            pass
        # tcp_sock.close()
        # return

create = Thread(target=groupCreate, args=())
create.start()

while True:
    try:
        message, addr = udp_sock.recvfrom(1024)
        message = message.decode()
        message = decrypt(message)
        #######################################
        #        checking group name          #
        #######################################

        if message.find('[') != -1 and message.find(']') != -1:
            clients[addr] = [None, None]

            clients[addr][1] = message[message.find('[') + 1:message.find(']')]

            if message.find('>[') != -1 and message.find(']=> ') != -1:
                clients[addr][0] = message[message.find('>[') + 1:message.find(']=> ')]

                exist = False
                for group in groups:
                    if group == clients[addr][1]:
                        exist = True
                        break

                if exist == False:
                    print(colored(f'There is no group like {clients[addr][1]}', 'red'))             # TODO sending info about this to client
                    # udp_sock.sendto(b'Change the group please!', addr)
                    continue

        #######################################
        # clients[addr] = clients[addr]
        # print('\n\n\n')
        if message.find('disconnected the server.') != -1:
            message = colored(message, 'red')
            print(colored(message, 'red'))
        elif message.find('has joined the chat.') != -1:
            message = colored(message, 'green')
            print(colored(message, 'green'))
        else:
            print(message)
        # message += '\n=> '
        # print('\n\n')
        #######################################
        # try:
        #     clients[addr] = clients[addr]                               # could be deleted
        #     print(message)
        # except:
        #     clients[addr][1] = message[message.find('[') + 1:message.find(']')]
        #     clients[addr][0] = message[message.find('>[') + 1:message.find(']=> ')]
        #     print(f'[{clients[addr][1]}]=>[{clients[addr][0]}]=> Joined chat')          # TODO add sending empty pocket in client
    # except TypeError:
    #     clients[addr][1] = message[message.find('[') + 1:message.find(']')]
    #     clients[addr][0] = message[message.find('>[') + 1:message.find(']=> ')]
    #     print(f'[{clients[addr][1]}]=>[{clients[addr][0]}]=> Joined chat')          # TODO add sending empty pocket in client

    #################################
    #         SENDING INFO          #                                                   # TODO send info to other users in group
    #################################

        message = encrypt(message)
        message = message.encode()

        for adr in clients:
            to = adr
            name = clients[adr][0][1:]
            group = clients[adr][1]

            if group == clients[addr][1] and adr != addr:
                print(colored(f'message has been sent to {to}-{name}-{group}', 'green'))
                # message = encrypt(message)
                # message = message.encode()
                # print(type(message))
                udp_sock.sendto(message, adr)

    except Exception as er:
        # print(er)
        pass


create.join()
tcp_sock.close()
udp_sock.close()
