import math
import socket

class Server(object):
    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__conn = None
        self.__transmit = Transmit()
    
    def bind_and_listen(self):
        self.__sock.bind((self.__host, self.__port))
        self.__sock.listen()

    def accept(self):
        self.__conn, addr = self.__sock.accept()
        return addr

    def send(self, msg):
        self.__transmit.send(self.__conn, msg)

    def recv(self):
        return self.__transmit.receive(self.__conn)

class Client(object):
    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__transmit = Transmit()

    def connect(self):
        self.__sock.connect((self.__host, self.__port))

    def send(self, msg):
        self.__transmit.send(self.__sock, msg)

    def recv(self):
        return self.__transmit.receive(self.__sock)

class Transmit(object):
    def __init__(self):
        self.__BLOCK_SIZE = 1024

    # send method
    def send(self, channel, data):
        d = data
        # ensuring that d is a bytes-like object
        if hasattr(data, 'encode'):
            d = data.encode()
        
        # determining chunks for sending
        length = len(d)
        iterations = math.ceil(length / self.__BLOCK_SIZE)
        # send the amount of chunks
        iterStr = str(iterations).encode()
        channel.send(iterStr)
        channel.recv(self.__BLOCK_SIZE)

        # send chunks
        for it in range(0, iterations):
            # get offset in array
            offset = it * self.__BLOCK_SIZE
            # get the end of the range which is to send
            distance = min(length - offset + 1, self.__BLOCK_SIZE)
            # send the chunk
            channel.send(d[offset:offset+distance])
            # retrieve confirmation (handshake)
            channel.recv(self.__BLOCK_SIZE)

    # receive method
    def receive(self, channel):
        # retrieve length of coms
        count = int(channel.recv(self.__BLOCK_SIZE).decode())
        channel.send(str(count).encode())
        # retrieve chunk after chunk and append them to frame
        frame = bytearray()
        for index in range(0, count):
            data = channel.recv(self.__BLOCK_SIZE)
            channel.send(str(len(data)).encode())
            frame.extend(data)
        # return frame
        return frame
