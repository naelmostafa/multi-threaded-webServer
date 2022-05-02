class ResponseParser:
    def __init__(self, response):
        self.response = response

    @property
    def version(self):
        return self.response.split(' ')[0]

    @property
    def status_code(self):
        return self.response.split(' ')[1]

    @property
    def status_message(self):
        return self.response.split(' ')[2]

    @property
    def headers(self):
        headers = {}
        for line in self.response.split('\r\n')[1:]:
            key, value = line.split(': ')
            headers[key] = value
        return headers

    def data(self):
        return self.response.split('\r\n\r\n')[1]
