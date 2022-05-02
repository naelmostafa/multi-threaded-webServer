class Response:
    """
    This class is used to store the response from the server.
    response_code: The response code from the server
    response_message: The response message from the server
    response_data: The response data from the server

    Response codes: 200:OK, 404:Forbidden, 500:Internal Server Error
    Response messages: OK, Forbidden, Internal Server Error
    Response: HTTP/1.1 {Code} {Message} \r\n {Headers} \r\n \r\n {Data}
    """

    def __init__(self, status_code, message, headers):
        self.status_code = status_code
        self.message = message
        self.response = f'HTTP/1.1 {self.status_code} {self.message} \r\n'
        if headers:
            self.headers = headers
            self.__set_headers(self.headers)

    def __set_headers(self, headers):
        for key, value in headers.items():
            self.response += f'{key}: {value}\r\n'
        self.response += '\r\n'
