import socket

from Client.Request import Request
from Client.ResponseParser import ResponseParser


class Client:
    FORMAT = 'utf-8'  # format
    HEADER = 2048  # header size

    def __init__(self, server, port=80):
        self.port = port
        self.server = server
        self.ADDR = (self.server, self.port)
        self.headers = {'Host': f'{self.server}',
                        'Connection': 'close'}

    def start(self):
        print('Connecting to server...')

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(self.ADDR)

        print("Connected to server")

        method = input("Method: ")
        url = input("path: ")

        # generate request and send it to server
        request = Request(method=method, path=url, headers=self.headers)

        msg_length = len(request.get_request())
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))

        client.send(send_length)
        client.send(request.get_request().encode(self.FORMAT))
        # receive response from server and parse it
        response = client.recv(self.HEADER).decode(self.FORMAT)
        print(f'Received response: \n{response}')
        response_parser = ResponseParser(response)
        client.close()

        # except Exception as e:
        #     print(e)
        #     break

        # print(f"Response: {response}")
