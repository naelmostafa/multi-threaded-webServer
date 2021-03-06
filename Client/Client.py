import shelve
import socket

from Client.Request import Request
from Client.ResponseParser import ResponseParser

"""
Client class for sending requests to the server.
METHOD - GET, POST
file-name - the file name to be sent to the server
data - content of file to be sent to the server
server - the host name of the server
port - the port number of the server <default: 80>

"""


def store_file(file_name, data):
    print(f'[*] Storing file: {file_name}')
    try:
        with open(file_name, 'w+') as f:
            f.write(data)
    except IOError:
        print("File not found")
        return False


class Client:
    FORMAT = 'utf-8'  # format
    HEADER = 2048  # header size
    CACHE_PATH = 'cache-client/'
    STORAGE_PATH = 'storage-client/'

    def __init__(self, server, port=80):
        self.port = port
        self.server = server
        self.ADDR = (self.server, self.port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.headers = {'Host': f'{self.server}',
                        'connection': 'close'}
        self.cache = shelve

    def start(self, method, file_name):
        print('[*] Connecting to server...')

        try:
            self.client.connect(self.ADDR)
            print("[*] Connected to server")
            # generate request and send it to server
            method = method.upper()
            if method == 'GET':
                response = self.do_GET(file_name)
            elif method == 'POST':
                response = self.do_POST(file_name)
            else:
                print("[*] ERROR: Invalid method")
                return False

            print(f'Received response: \n{response}')
            response_parser = ResponseParser(response)
            file = file_name.split('/')[-1]
            if file == '':
                file = 'index.html'
            response_file = f'{self.STORAGE_PATH}{self.server}.{file}'
            store_file(response_file, response_parser.data)
            print('[*] Closing connection...')  # close connection
        except Exception as e:
            print(f'Error: {e}')
        finally:
            self.client.close()
            print('Disconnected from server')

    def send_request(self, request):
        self.client.send(request.build_request().encode(self.FORMAT))
        response = self.client.recv(self.HEADER).decode(self.FORMAT)
        return response

    def do_GET(self, file_name):
        request = Request(method='GET', path=file_name, headers=self.headers)
        cache_key = f'{self.server}:{self.port}:{file_name}'
        response = None
        try:
            with self.cache.open(self.CACHE_PATH) as cache:
                if cache_key in cache:
                    print('[*] Cache hit')
                    response = cache.get(cache_key)
                else:
                    print('[*] Cache miss')
                    response = self.send_request(request)
                    cache[cache_key] = response
        except Exception as e:
            print(f'[*] ERROR: {e}')
        return response

    def do_POST(self, file_name):
        request = Request(method='POST', path=file_name, headers=self.headers)
        try:
            with open(file_name, 'r') as f:
                data = f.read()
        except Exception as e:
            print(f'[*] ERROR: {e}')
        request.set_data(data=data)
        response = self.send_request(request)
        return response
