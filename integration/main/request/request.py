import datetime
import hashlib
import json

import msgpack
import requests
import requests_toolbelt
import urllib3
from constants import RequestConstants
from response import Response


class RequestBuilder(object):

    def __init__(self, url, session=None, timeout=60):
        self.__args = {
            'url': url,
            'headers': {},
            'data': {},
            'cookies': {},
            'json': {},
            'params': {},
            'hooks': {},
            'timeout': timeout
        }

        self.__request = requests if session is None else session
        self.__request_time = None
        self.__method = ''

        # disables warning. When we make unsafe SSL requests for the mock commerce pages
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def __str__(self):
        """
        :return: str 
        """

        return json.dumps(self.details, indent=4, separators=(',', ': '))

    @property
    def details(self):
        """
        details containing argument, 
        unpacks msgpack to print

        :return: dict
        """

        details = self.__args.copy()
        details.pop('hooks')

        if 'Content-Type' in self.__args['headers']:
            if self.__args['headers']['Content-Type'] == RequestConstants.ContentTypes.MSG_PACK:
                details['data'] = msgpack.unpackb(self.__args['data'])
            elif self.__args['headers']['Content-Type'].startswith(RequestConstants.ContentTypes.FORM_DATA):
                details['data'] = str(self.__args['data'])

        details['method'] = self.__method

        try:
            cookies = requests.utils.dict_from_cookiejar(self.__request.cookies)
        except TypeError:
            cookies = requests.utils.dict_from_cookiejar(self.__request.cookies.RequestsCookieJar())
        details['cookies'] = cookies

        if self.__request_time is not None:
            details['REQUEST_TIME'] = self.__request_time.strftime('%y/%m/%d %H:%M:%S:%f').encode('utf-8').strip()

        return details

    @property
    def method(self):
        """
        :return: str 
        """

        return self.__method

    @property
    def time(self):
        """
        the time the request was sent

        :return: :py:class: `datetime`
        """

        return self.__request_time

    @property
    def url(self):
        """
        request url

        :return: str 
        """

        return self.__args['url']

    def __remove_optional_parameters(self, input_object):
        """
        :param input_object:
        :return:
        """

        # object queue is a queue of dicts and lists
        object_queue = [input_object]

        while len(object_queue) > 0:
            item = object_queue.pop()

            if isinstance(item, dict):
                for key, value in list(item.iteritems()):
                    if value is RequestConstants.Parameters.OPTIONAL:
                        # pop removes key and value from dictionary
                        item.pop(key)
                    elif isinstance(value, dict) or isinstance(value, list):
                        object_queue.append(value)

            elif isinstance(item, list):
                index = 0
                while index < len(item):
                    value = item[index]

                    if value is RequestConstants.Parameters.OPTIONAL:
                        del item[index]
                        continue
                    elif isinstance(value, dict) or isinstance(value, list):
                        object_queue.append(value)
                    index += 1

    def data(self, data):
        """
        builder function to add data to the request

        :param data:
        :return: :py:class: `RequestBuilder`
        """

        self.__args['data'].update(data)
        self.__remove_optional_parameters(self.__args['data'])
        return self

    def delete(self):
        """
        executes a delete request

        :return: :py:class: `Response`
        """

        self.__method = 'DELETE'
        self.__request_time = datetime.datetime.now()
        response_wrapped = Response(self)

        self.__args['hooks'] = {
            'response': [response_wrapped.response_hook]
        }

        return response_wrapped.wrap(self.__request.delete(**self.__args))

    def get(self, verify=False):
        """
        executes a get request

        :param verify: SSL verification. False for ignore
        :return: :py:class: `Response`
        """

        self.__method = 'GET'
        self.__request_time = datetime.datetime.now()
        response_wrapped = Response(self)

        self.__args['verify'] = verify
        self.__args['hooks'] = {'response': [response_wrapped.response_hook]}

        return response_wrapped.wrap(self.__request.get(**self.__args))

    def headers(self, headers):
        """
        builder function to add headers to the request

        :param json:
        :return: :py:class: `RequestBuilder`
        """

        self.__args['headers'].update(headers)
        self.__remove_optional_parameters(self.__args['headers'])
        return self

    def json(self, json):
        """
        builder function to add json to the request

        :param json:
        :return: :py:class: `RequestBuilder`
        """

        self.__args['json'].update(json)
        self.__remove_optional_parameters(self.__args['json'])

        return self

    def params(self, params):
        """
        builder function to add params to the request

        :param json:
        :return: :py:class: `RequestBuilder`
        """

        self.__args['params'].update(params)
        self.__remove_optional_parameters(self.__args['params'])
        return self

    def post(self, content_type=RequestConstants.ContentTypes.JSON, file=None):
        """
        executes a post request

        :param file:
        :param content_type:
        :return: :py:class: `Response`
        """

        self.__method = 'POST'
        self.__request_time = datetime.datetime.now()
        response_wrapped = Response(self)

        self.transform(content_type)

        if file is not None:
            multipart_encoder = requests_toolbelt.MultipartEncoder(
                fields={
                    'type': 'formData',
                    'file': (file.name, file, 'application/x-www-form-urlencoded')
                }
            )
            self.__args['headers']['Content-Type'] = multipart_encoder.content_type
            self.__args['data'] = multipart_encoder

        self.__args['hooks'] = {'response': [response_wrapped.response_hook]}

        response = self.__request.post(**self.__args)
        return response_wrapped.wrap(response)

    def put(self, content_type=RequestConstants.ContentTypes.JSON):
        """
        executes a post request

        :param content_type:
        :return: :py:class: `Response`
        """

        self.__method = 'PUT'
        self.__request_time = datetime.datetime.now()
        response_wrapped = Response(self)

        self.transform(content_type)
        self.__args['hooks'] = {'response': [response_wrapped.response_hook]}

        return response_wrapped.wrap(self.__request.put(**self.__args))

    def set_timeout(self, timeout):
        """
        sets the timeout for the request (it defaults to 30 seconds)
        
        :param timeout: 
        :return: 
        """

        self.__args['timeout'] = timeout
        return self

    def sign(self, secret_key):
        """
        signs the data with a secret key
        
        :param secret_key: 
        :return: 
        """

        concated_data = ''.join((k + str(v) for k, v in sorted(self.__args['data'].iteritems()) if k != 'signature'))
        hash_string = u'{0}{1}'.format(concated_data, str(secret_key))

        self.__args['data']['signature'] = hashlib.md5(hash_string.encode('utf-8')).hexdigest().lower()

        return self

    def transform(self, content_type):
        """
        transforms data to be compatible for a specific content_type request
        Currently only handles message pack because that's the only other content_type we support
        
        it changes content-type and accept in header to msgpack
        it moves information from json to data
        
        :param content_type: 
        :return: 
        """

        if content_type == RequestConstants.ContentTypes.MSG_PACK:
            self.__args['headers']['Content-Type'] = RequestConstants.ContentTypes.MSG_PACK
            self.__args['headers']['Accept'] = RequestConstants.ContentTypes.MSG_PACK

            self.__args['data'] = msgpack.packb(self.__args['json'])
            self.__args['json'] = {}
