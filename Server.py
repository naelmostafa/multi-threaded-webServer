import socket
import threading
import Response
import RequestParser


class Server:
    FORMAT = 'utf-8'  # format
    DISCONNECT_MESSAGE = "!DISCONNECT"  # disconnect message
    HOST = socket.gethostbyname(socket.gethostname())  # server ip
    HEADER = 2048  # header size

    def __init__(self, port=80):
        self.port = port
        self.ADDR = (self.HOST, self.port)  # server address
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        self.server.listen()
        self.clients = []
        self.threads = []
        self.running = True

    def start(self):
        print(f'[*] Server started on port {self.port}')
        while self.running:
            print(f'[*] Waiting for clients...')
            client, addr = self.server.accept()
            self.clients.append(client)
            thread = threading.Thread(target=self.handle, args=(client, addr))
            thread.start()
            self.threads.append(thread)

    def handle(self, client, addr):
        print(f'[*] Connected to {addr}')
        while True:
            try:
                # TODO: receive msg from client
                # TODO: parse msg => Extract Method, Path, Headers, Data
                # TODO: create response
                # TODO: send response
                request = client.recv(2048).decode(self.FORMAT)
                if request == self.DISCONNECT_MESSAGE:
                    print(f'[*] {addr} disconnected')
                    self.clients.remove(client)
                    client.close()
                    break
                else:
                    print(f'[*] {addr} > {request}')
                    for client in self.clients:
                        if client != self.server:
                            client.send(request.encode(self.FORMAT))
            except Exception as e:
                print(e)
                break
