import socket

from Client.Request import Request
from Client.ResponseParser import ResponseParser

"""
Client class for sending requests to the server.
METHOD - GET, POST, PUT, DELETE
file-name - the file name to be sent to the server
server - the host name of the server
port - the port number of the server <default: 80>

"""


class Client:
    FORMAT = 'utf-8'  # format
    HEADER = 2048  # header size

    def __init__(self, server, port=80):
        self.port = port
        self.server = server
        self.ADDR = (self.server, self.port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.headers = {'Host': f'{self.server}',
                        'connection': 'close'}

    # TODO: POST

    def start(self, method, file_name):
        print('[*] Connecting to server...')

        try:
            self.client.connect(self.ADDR)
            print("[*] Connected to server")

            # generate request and send it to server
            request = Request(method=method, path=file_name, headers=self.headers)
            self.client.send(request.get_request().encode(self.FORMAT))
            print("[*] Request sent\n")

            # receive response from server and parse it
            response = self.client.recv(self.HEADER).decode(self.FORMAT)
            print(f'Received response: \n{response}')

        except Exception as e:
            print(f'Error: {e}')
        finally:
            self.client.close()
            print('Disconnected from server')
