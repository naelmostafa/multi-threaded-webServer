import socket
import Request
import ResponseParser


class Client:
    FORMAT = 'utf-8'  # format
    DISCONNECT_MESSAGE = "!DISCONNECT"  # disconnect message
    HEADER = 2048  # header size

    def __init__(self, server, port=4545):
        self.port = port
        self.server = server
        self.ADDR = (self.server, self.port)
        self.headers = {'Host': f'{self.server} : {self.port}'}

    def start(self):
        print('Connecting to server...')
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(self.ADDR)

        print("Connected to server")
        while True:
            try:
                method = input("Method: ")
                url = input("URL: ")
                data = input("Data: ")
                # generate request and send it to server
                request = Request.Request(method, url, self.headers, data)
                client.send(bytes(request.get_request(), self.FORMAT))
                # receive response from server and parse it
                response = client.recv(self.HEADER).decode(self.FORMAT)
                response_parser = ResponseParser.ResponseParser(response)

                if response_parser.data() == self.DISCONNECT_MESSAGE:
                    client.close()
                    break
            except Exception as e:
                print(e)
                break

            print(f"Response: {response}")
