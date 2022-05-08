class Response:
    """
    This class is used to store the response from the server.
    response_code: The response code from the server
    response_message: The response message from the server
    response_data: The response data from the server

    Response codes: 200:OK, 404:Not Found, 500:Internal Server Error
    Response messages: OK, Not Found, Internal Server Error
    Response: HTTP/1.X {Code} {Message} \r\n {Headers} \r\n \r\n {Data}
    """
    message_codes = {200: "OK",
                     404: "Not Found",
                     500: "Internal Server Error"}

    def __init__(self, version=0, headers: dict = None, data=None):
        self.version = version
        self.status_code = None
        self.status_message = None
        self.headers = None
        self.response = None

    def build_response(self, status_code, headers: dict = None, data=None):
        self.response = f'HTTP/1.{self.version} {status_code} {self.message_codes[status_code]} \r\n'
        if headers:
            self.__set_headers(headers)
        if data:
            self.response += data
        return self.response

    def ok_status(self, headers: dict = None, data=None):
        self.status_code = 200
        self.status_message = 'OK'
        self.response = f'HTTP/1.{self.version} {self.status_code} {self.status_message} \r\n'
        if headers:
            self.__set_headers(headers)
        if data:
            self.response += data
        return self.response

    def forbidden_status(self, headers: dict = None):
        self.status_code = 404
        self.status_message = 'Not Found'
        self.response = f'HTTP/1.{self.version} {self.status_code} {self.status_message} \r\n'
        if headers:
            self.__set_headers(headers)
        return self.response

    def __set_headers(self, headers):
        for key, value in headers.items():
            self.response += f'{key}: {value}\r\n'
        self.response += '\r\n'
