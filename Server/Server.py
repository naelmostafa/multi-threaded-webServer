import socket
import threading

from Server.RequestParser import RequestParser
from Server.Response import Response


class Server:
    FORMAT = 'utf-8'  # format
    SERVER = socket.gethostbyname(socket.gethostname())  # server ip
    HEADER = 2048  # header size
    IMAGE_EXTENSIONS = ["png", "jpg", "jpeg", "gif"]  # image extensions
    TEXT_EXTENSIONS = ["txt", "html", "css", "js"]  # text extensions

    def __init__(self, port=80):
        self.port = port
        self.ADDR = (self.SERVER, self.port)  # server address
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        self.running = True

    def start(self):
        self.server.listen()
        print(f'[*] Server started on {self.SERVER}:{self.port}')
        while self.running:
            print(f'[*] Waiting for clients...')
            client, addr = self.server.accept()
            thread = threading.Thread(target=self.handle, args=(client, addr))
            thread.start()
            print(f'[*] Active connections: {threading.active_count() - 1}')

    def handle(self, client, addr):
        print(f'[*] Accepted connection from {addr}')
        try:
            msg_len = client.recv(self.HEADER).decode(self.FORMAT)
            if msg_len:
                request = client.recv(int(msg_len)).decode(self.FORMAT)
        except Exception as e:
            print(f'[*] ERROR : {e}')
            client.close()
            print(f'[*] Connection from {addr} closed')
            return
        else:

            request_parser = RequestParser(request)
            if request_parser.headers['connection'] == 'keep-alive':
                self.handle_keep_alive(10, client, addr, request)
            else:
                self.handle_close(client, addr, request)

    def handle_close(self, client, addr, request):
        print(f'[*] Received request: \n{request}')
        request_parser = RequestParser(request)
        code = 404
        response = None
        response_builder = Response()
        headers = {'connection': 'close'}
        if request_parser.method == 'GET':
            response, code = self.get_file(request_parser.path)
            # get file extension
            extension = request_parser.path.split('.')[-1].lower()
            if extension in self.IMAGE_EXTENSIONS:
                headers['content-type'] = 'image/' + extension
            elif extension in self.TEXT_EXTENSIONS:
                headers['content-type'] = 'text/' + extension

        elif request_parser.method == 'POST':
            # TODO: POST request
            pass

        response = response_builder.build_response(status_code=code, headers=headers, data=response)
        client.send(response.encode(self.FORMAT))
        client.close()
        print(f'[*] Connection from {addr} closed')
        exit(0)

    def handle_keep_alive(self, timeout, client, addr, request):
        client.settimeout(timeout)
        while True:
            try:
                # TODO: keep-alive => timeout heuristically
                print(f'[*] Received request: \n{request}')
                request_parser = RequestParser(request)
                code = 404
                response = None
                response_builder = Response()
                headers = {'connection': 'keep-alive'}  # keep-alive
                if request_parser.method == 'GET':
                    response, code = self.get_file(request_parser.path)
                    # get file extension
                    extension = request_parser.path.split('.')[-1].lower()
                    if extension in self.TEXT_EXTENSIONS:
                        headers['content-type'] = 'text/' + extension
                    elif extension in self.IMAGE_EXTENSIONS:
                        headers['content-type'] = 'image/' + extension
                if request_parser.method == 'POST':
                    # TODO: POST request
                    pass
                response = response_builder.build_response(status_code=code, headers=headers, data=response)
                # receive request
                msg_len = client.recv(self.HEADER).decode(self.FORMAT)
                if msg_len:
                    request = client.recv(int(msg_len)).decode(self.FORMAT)
            except socket.timeout:
                print(f'[*] {addr} timed out')
                client.close()
                break
            except Exception as e:
                print(e)
                break

    @staticmethod
    def get_file(path):
        if path == '/':
            path = '/index.html'
        try:
            with open(path[1:], 'r') as file:
                return file.read(), 200
        except FileNotFoundError:
            return f'File {path[1:]} not found', 404
