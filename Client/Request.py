class Request:
    """
    Request class
    request_method: GET, POST, PUT, DELETE
    request_path: /path/to/resource
    request: {Method} + {Path} + HTTP/1.X\r\n + {Headers} + \r\n + {Data}
    """

    def __init__(self, method: str, path: str, headers: dict = None, data: str = None):
        self.method = method.upper()
        self.path = path
        self.request = f'{self.method} {self.path} HTTP/1.1\r\n'
        if headers:
            self.headers = headers
            self.__set_headers(headers)
        if data:
            self.data = data
            self.request += data

    def __set_headers(self, headers):
        for key, value in headers.items():
            self.request += f'{key}: {value}\r\n'
        self.request += '\r\n'

    def set_data(self, data):
        if data:
            self.data = data
            self.request += data

    def build_request(self):
        return self.request

    def __str__(self):
        return self.request
