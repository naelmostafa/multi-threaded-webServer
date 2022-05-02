import socket
from Request import *


class Client:
    FORMAT = 'utf-8'  # format
    DISCONNECT_MESSAGE = "!DISCONNECT"  # disconnect message
    HEADER = 2048  # header size

    def __init__(self, server, port=80):
        self.port = port
        self.server = server
        self.ADDR = (self.server, self.port)

    def start(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(self.ADDR)

        while True:
            data = input("> ")

            if data == self.DISCONNECT_MESSAGE:
                client.close()
                break

            # TODO: create request => request = Request(method, path)
            # TODO: send request to server

            client.send(bytes(data, self.FORMAT))
            response = client.recv(self.HEADER).decode(self.FORMAT)

            print(f"Response: {response}")
