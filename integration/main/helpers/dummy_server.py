import os

from integration.main.request import RequestBuilder, Url


class DummyServer(object):
    IP = 'http://34.217.73.245:8080/'

    def __init__(self, ip=None):

        # if ip is not provided, it will default to environment variables
        # if there not provided environment variables, it will default to a hard coded value
        if ip is None:
            ip = os.environ['dummy_server'] if 'dummy_server' in os.environ else DummyServer.IP
        self.__ip = ip

    @property
    def ip(self):

        return self.__ip

    @staticmethod
    def get_webhook_url(environment_name):
        return '{}{}/test_webhook/'.format(DummyServer.IP, environment_name)

    def get_call(self, method, path):

        url = Url.build_url(self.__ip, path='/registry')
        registry_response = RequestBuilder(url).get()
        registry_response.assert_is_success()

        for key, data in registry_response.content.iteritems():
            if data['method'] == method and data['path'] == path:
                return DummyServerCall(self.__ip, key, method, path)
        return None

    def register(self, method, path, content=None, headers=None, status=None):

        content = {} if content is None else content
        headers = {} if headers is None else headers
        status = 200 if status is None else status

        url = Url.build_url(self.__ip, path='/register')
        register = RequestBuilder(url).json({
            'method': method,
            'path': path,
            'content': content,
            'headers': headers,
            'status_code': status
        }).post()
        register.assert_is_success()

        key = register.content['registry_key']
        return DummyServerCall(self.__ip, key, method, path)


class DummyServerCall(object):

    def __init__(self, ip, key, method, path):

        self.__ip = ip
        self.__registry_key = key
        self.__method = method
        self.__path = path

    @property
    def path(self):

        return self.__path

    @property
    def url(self):

        url = Url.build_url(self.__ip, path=self.__path)
        return url

    def call(self, json=None):

        if self.__method.upper() == 'GET':
            return RequestBuilder(self.url).get()

        if self.__method.upper() == 'POST':
            return RequestBuilder(self.url).json(json).post()

        return None

    def attach(self, absolute_file_path):

        with open(absolute_file_path, 'rb') as attachment:
            url = Url.build_url(self.__ip, path='/attach/{}'.format(self.__registry_key))
            attach = RequestBuilder(url).post(file=attachment)
            attach.assert_is_success()

    def logs(self):

        url = Url.build_url(self.__ip, path='/logs/{}'.format(self.__registry_key))
        logs = RequestBuilder(url).get()
        logs.assert_is_success()
        return logs.content['logs']

    def unregister(self):

        url = Url.build_url(self.__ip, path='/unregister')
        unregister = RequestBuilder(url).json({
            'method': self.__method,
            'path': self.__path,
        }).post()
        unregister.assert_is_success()
