import math
import socket

class Comms(object):
    def __init__(self, host, port):
        self.__BLOCK_SIZE = 1024

        self.__host = host
        self.__port = port
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.bind((host, port))
        self.__conn = None

    def __encode(self, data):
        encoded = base64.b64encode(encoded)
        return encoded

    def __decode(self, data):
        decoded = base64.b64decode(data)
        return decoded

    def listen(self):
        self.__sock.listen(1)
        self.__conn, addr = self.__sock.accept()

    def send(self, data):
        d = data
        # ensuring that d is a bytes-like object
        if hasattr(data, 'encode'):
            d = data.encode()
        
        # determining chunks for sending
        length = len(d)
        iterations = math.ceil(length / self.__BLOCK_SIZE)
        # send the amount of chunks
        iterStr = str(iterations).encode()
        self.__conn.send(iterStr)
        self.__conn.recv(self.__BLOCK_SIZE)

        # send chunks
        for it in range(0, iterations):
            # get offset in array
            offset = it * self.__BLOCK_SIZE
            # get the end of the range which is to send
            distance = min(length - offset + 1, self.__BLOCK_SIZE)
            # send the chunk
            self.__conn.send(d[offset:offset+distance])
            # retrieve confirmation (handshake)
            self.__conn.recv(self.__BLOCK_SIZE)

    def receive(self):
        count = self.__conn.recv(self.__BLOCK_SIZE).decode()
        self.__conn.send('ok')
        frame = bytearray()
        for index in range(0, count):
            data = self.__conn.recv(self.__BLOCK_SIZE)
            self.__conn.send('ok')
            frame.extend(data)
        return frame.decode()
