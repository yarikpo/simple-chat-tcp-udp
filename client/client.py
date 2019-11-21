import socket
from threading import Thread
import sys
from colorama import init
from termcolor import colored

init()

host = '127.0.0.1'
host = input('ip: ')
tcp_port = 19092

udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_sock.connect((host, tcp_port))


runProgram = True
addr = (host, 19090)

dontuse = ['?', '&']

def encrypt(message):                                        # TODO this function will encrypt messages
    return message

def decrypt(message):                                        # TODO this function will decrypt messages
    return message

def receive():                                               # TODO receiving messages from the server
    global udp_sock, runProgram
    while runProgram:
        try:
            data, server = udp_sock.recvfrom(1024)
            data = data.decode()
            data = decrypt(data)
            print(data + '\n=> ', end='')
        except KeyboardInterrupt:
            print(colored('[REC ERR...]', 'red'))
            break
        except:
            pass


receiving = Thread(target=receive, args=())
receiving.start()

name = input('Type your nickname: ')

def createOrJoinGroup(groupKey):
    if groupKey == '?open':                               # to create group -> ?open
        groupName = '?' + input('Choose group name: ')    # print name of your group
        groupName = str(groupName).encode()               # decoding str to bytes
        # udp_sock.sendto(groupName, addr)                  # sending name of the group to server
        # conn, addr = tcp_sock.accept()
        print(colored('Sending info...', 'blue'))
        tcp_sock.send(groupName)
        groupName = groupName.decode()
        try:
            print(colored('Receiving info...', 'blue'))
            data = tcp_sock.recv(1024)                    # waiting for answer from the server
            data = data.decode()                          # decoding data from byte to utf-8
            data = decrypt(data)                          # uncoding data

            # print("\n\n\n\n" + f'[GROUP {groupName[1:]} HAS BEEN CREATED]' + "\n\n\n")

            if data == f'[GROUP {groupName[1:]} HAS BEEN CREATED]':     # checking for errors
                print (colored(data, 'yellow'))
            else:
                print (colored(f'SOMETHING WRONG(try to rename group!)', 'red'))
                print(data)
        except:
            print(colored('ERR.. Something wrong!', 'red'))


while runProgram:
    try:
        groupKey = input('Enter group\'s secret key: ')       # reading group key
        if groupKey == '?open':
            createOrJoinGroup(groupKey)

        exit = True
        while exit:                                           # checking for symbols which you can't use
            exit = False
            for use in dontuse:
                if groupKey.find(use) != -1:
                    exit = True
            if exit == False:
                break
            groupKey = input('Enter group\'s secret key: ')


        print(colored(f'[TRYING TO ENTER GROUP: {groupKey}]', 'yellow'))

        ##################
        #    ENTERING    # TODO
        ##################

        receiving = Thread(target=receive, args=())
        receiving.start()

        message = f'[{groupKey}]=>[{name}]=> has joined the chat.'
        message = encrypt(message)
        message = message.encode()
        udp_sock.sendto(message, addr)
        del message

        while True:
            try:
                message = input('=> ')
                message = f'[{groupKey}]=>[{name}]=> ' + message
                message = encrypt(message)
                message = message.encode()
                udp_sock.sendto(message, addr)
            except KeyboardInterrupt:
                # receiving.join()
                print(colored('[EXITTING FROM THE CHAT...]', 'blue'))
                message = f'{name} disconnected the server.'
                message = encrypt(message)
                message = message.encode()
                udp_sock.sendto(message, addr)
                del message
                break

    except:
        print(colored('\n[PROGRAM HAS BEEN FINISHED]', 'yellow'))
        # print(er)
        runProgram = False
        udp_sock.close()
        sys.exit
        receiving.join()
