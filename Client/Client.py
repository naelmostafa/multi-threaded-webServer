import socket

from Client.Request import Request
from Client.ResponseParser import ResponseParser
from Client.Cache import Cache

"""
Client class for sending requests to the server.
METHOD - GET, POST
file-name - the file name to be sent to the server
data - content of file to be sent to the server
server - the host name of the server
port - the port number of the server <default: 80>

"""


def store_file(file_name, data):
    try:
        with open(file_name, 'w') as f:
            f.write(data)
    except IOError:
        print("File not found")
        return False


class Client:
    FORMAT = 'utf-8'  # format
    HEADER = 2048  # header size
    CACHE_PATH = 'cache/'

    def __init__(self, server, port=80):
        self.port = port
        self.server = server
        self.ADDR = (self.server, self.port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.headers = {'Host': f'{self.server}',
                        'connection': 'close'}
        self.cache = Cache(self.CACHE_PATH)

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
            store_file('response.html', response_parser.data)
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
        try:
            if self.cache.is_cached(cache_key):
                print('[*] File is cached')
                response = self.cache.get(cache_key)
            else:
                print('[*] File is not cached')
                response = self.send_request(request)
                self.cache.set(cache_key, response)
        except Exception as e:
            print(f'[*] ERROR: {e}')
            self.cache.close()
            return False
        else:
            self.cache.close()
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
