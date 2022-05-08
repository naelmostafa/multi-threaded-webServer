import socket
import threading

from Server.RequestParser import RequestParser
from Server.Response import Response


class Server:
    FORMAT = 'utf-8'  # format
    DISCONNECT_MESSAGE = "!DISCONNECT"  # disconnect message
    SERVER = socket.gethostbyname(socket.gethostname())  # server ip
    HEADER = 2048  # header size

    def __init__(self, port=80):
        self.port = port
        self.ADDR = (self.SERVER, self.port)  # server address
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        self.clients = []
        self.threads = []
        self.running = True

    def start(self):
        self.server.listen()
        print(f'[*] Server started on {self.SERVER}:{self.port}')
        while self.running:
            print(f'[*] Waiting for clients...')
            client, addr = self.server.accept()
            self.clients.append(client)
            thread = threading.Thread(target=self.handle, args=(client, addr))
            thread.start()
            self.threads.append(thread)
            print(f'[*] Active connections: {threading.active_count() - 1}')

    def handle(self, client, addr):
        print(f'[*] Accepted connection from {addr}')
        client.settimeout(5)
        while True:
            try:
                request = client.recv(self.HEADER).decode(self.FORMAT)

                request_parser = RequestParser(request)

                response = None
                response_builder = Response()

                if request_parser.method == 'GET':
                    # GET request
                    if request_parser.path == '/':
                        response = self.get_index()
                    else:
                        response = self.get_file(request_parser.path)

                elif request_parser.method == 'POST':
                    # TODO: POST request
                    pass

                if response is None:
                    response = response_builder.forbidden_status()
                else:
                    response = response_builder.ok_status(data=response)

                if request_parser.data == self.DISCONNECT_MESSAGE:
                    print(f'[*] {addr} disconnected')
                    self.clients.remove(client)
                    client.close()
                    break
                else:
                    print(f'[*] {addr} > {request}')
                    client.send(response.encode(self.FORMAT))

            except socket.timeout:
                print(f'[*] {addr} timed out')
                self.clients.remove(client)
                client.close()
                break

            except Exception as e:
                print(e)
                break

    @staticmethod
    def get_index():
        try:
            with open('index.html', 'r') as file:
                return file.read()
        except FileNotFoundError:
            return f'File index.html not found'

    @staticmethod
    def get_file(path):
        try:
            with open(path[1:], 'r') as file:
                return file.read()
        except FileNotFoundError:
            return f'File {path[1:]} not found'
