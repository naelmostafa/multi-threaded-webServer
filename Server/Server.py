import socket
import threading

from Server.RequestParser import RequestParser
from Server.Response import Response


def get_file(path):
    if path == '/':
        path = '/index.html'
    try:
        with open(path[1:], 'r') as file:
            return file.read(), 200
    except FileNotFoundError:
        return f'File {path} not found', 404


def store_data(file_name, data):
    print(f'[*] Storing file: {file_name}')
    try:
        with open(file_name, 'w+') as f:
            f.write(data)
    except IOError:
        print("Failed to store file")
        return False


class Server:
    FORMAT = 'utf-8'  # format
    SERVER = socket.gethostbyname(socket.gethostname())  # server ip
    HEADER = 2048  # header size
    IMAGE_EXTENSIONS = ["png", "jpg", "jpeg", "gif"]  # image extensions
    TEXT_EXTENSIONS = ["txt", "html", "css", "js"]  # text extensions
    STORAGE_PATH = 'storage-server/'

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
            thread = threading.Thread(target=self.handle_piped, args=(client, addr))
            thread.start()
            print(f'[*] Active connections: {threading.active_count() - 1}')

    def handle_piped(self, client, addr):
        print(f'[*] Accepted connection from {addr}')
        client.settimeout(10)
        try:
            while True:
                try:
                    request = client.recv(self.HEADER).decode(self.FORMAT)
                except Exception as e:
                    print(f'[*] ERROR : {e}')
                    client.close()
                    print(f'[*] Connection from {addr} closed')
                    return
                else:
                    request_parser = RequestParser(request)
                    try:
                        if request_parser.headers['connection'].lower() == 'keep-alive':
                            # Persistent and Pipeline connection
                            thread = threading.Thread(target=self.persistent, args=(client, addr, request))
                            thread.start()
                        else:
                            # Non-Persistent connection
                            self.persistent(client, addr, request, none_persistent=True)
                            client.close()
                            exit()
                            return
                    except Exception as e:
                        print(f'[*] Connection header ERROR : {e}')
                        self.persistent(client, addr, request, none_persistent=True)
                        client.close()
                        return
        except socket.timeout:
            print(f'[*] ERROR : Timeout')
            client.close()
            print(f'[*] Connection from {addr} closed')
            return

    def persistent(self, client, addr, request, none_persistent=False):
        print(f'[*] Received request: \n{request}')
        request_parser = RequestParser(request)
        code = 404
        response = None
        if none_persistent:
            connection = 'close'
        else:
            connection = 'keep-alive'
        headers = {'connection': f'{connection}'}
        response_builder = Response()
        if request_parser.method == 'GET':
            response, code = get_file(request_parser.path)
            # get file extension
            extension = request_parser.path.split('.')[-1].lower()
            if extension in self.IMAGE_EXTENSIONS:
                headers['content-type'] = 'image/' + extension
            elif extension in self.TEXT_EXTENSIONS:
                headers['content-type'] = 'text/' + extension

        elif request_parser.method == 'POST':
            data = request_parser.data
            code = 200
            print(f'[*] POST data: {data}')
            file_name = f'{self.STORAGE_PATH}{addr[0]}'
            store_data(file_name, data)

        response = response_builder.build_response(status_code=code, headers=headers, data=response)
        client.send(response.encode(self.FORMAT))

        if none_persistent:
            client.close()
            print(f'[*] Connection from {addr} closed')
            exit()
        return
