class RequestParser:
    def __init__(self, request):
        self.request = request

    @property
    def method(self):
        return self.request.split(' ')[0]

    @property
    def path(self):
        return self.request.split(' ')[1]

    @property
    def version(self):
        return self.request.split(' ')[2]

    @property
    def headers(self):
        headers = {}
        for line in self.request.split('\r\n')[1:]:
            key, value = line.split(': ')
            headers[key] = value
        return headers

    @property
    def data(self):
        return self.request.split('\r\n\r\n')[1]

    @property
    def data_post(self):
        data_post = {}
        try:
            for line in self.data.split('&'):
                key, value = line.split('=')
                data_post[key] = value
        except Exception as e:
            return data_post

    @property
    def data_get(self):
        data_get = {}
        try:
            for line in self.path.split('?')[1].split('&'):
                key, value = line.split('=')
                data_get[key] = value
        except Exception as e:
            return data_get
