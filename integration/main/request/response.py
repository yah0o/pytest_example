import datetime
import json

from allure import attach, attachment_type
import msgpack
from bs4 import BeautifulSoup
from hamcrest import *

from constants import *
from integration.main.logger import log


class Response(object):
    """
    A wrapper around requests responses that kind of adheres it to patterns that our teams generally use
    """

    SUCCESS_CODES = range(200, 300)

    DECODE_FUNCTIONS = {
        RequestConstants.ContentTypes.MSG_PACK: msgpack.unpackb,
        RequestConstants.ContentTypes.MSG_PACK_UTF8: msgpack.unpackb,
        RequestConstants.ContentTypes.JSON: json.loads,
        RequestConstants.ContentTypes.JSON_UTF8: json.loads,
    }

    def __init__(self, request):

        self.__response = None
        self.__request = request
        self.__response_time = None

    def __str__(self):

        try:
            as_string = json.dumps(self.details, indent=4, separators=(',', ': '))
        except Exception:
            as_string = str(self.details)
        return as_string

    @property
    def content(self):
        """
        response content decoded
        :return:
        """

        content_type = self.headers['Content-Type'] if 'Content-Type' in self.headers else None
        if content_type and content_type in Response.DECODE_FUNCTIONS:
            return Response.DECODE_FUNCTIONS[content_type](self.__response.content)

        try:
            return json.loads(self.__response.content)
        except ValueError:
            return self.__response.content

    @property
    def details(self):
        """
        returns a json summary of the request and response and their details
        :return: dict 
        """

        return {
            'REQUEST_DETAILS': self.__request.details,
            'RESPONSE_DETAILS': {
                'STATUS': self.status,
                'RESPONSE': self.content,
                'RESPONSE_TIME': self.__response_time.strftime('%y/%m/%d %H:%M:%S:%f'),
            }
        }

    @property
    def is_html(self):
        """
        checks if the content responded with a html web page
        :return: 
        """

        if isinstance(self.__response.content, str):
            soup = BeautifulSoup(self.__response.content, 'html.parser')
            return bool(soup.find())

        return False

    @property
    def headers(self):
        """
        :return: 
        """

        return self.__response.headers

    @property
    def request(self):
        """
        :return: :py:charm: `RequestBuilder`
        """

        return self.__request

    @property
    def status(self):
        """
        :return: 
        """

        return self.__response.status_code

    @property
    def success(self):
        """
        returns true if success and false if there was not a 200 response or if there was a "successful failure"

        :return: bool
        """

        # some errors return success status but with an embedded 'success': false for failure
        # for server calls it tends to be self.content['body']['success']
        # for tools calls it tends to be self.content['success']
        if isinstance(self.content, dict):
            success = Response.__contains(self.content, 'success')
            if success is not None:
                return success

        return self.status in Response.SUCCESS_CODES

    @property
    def time(self):
        """
        the time the response is received

        :return: :py:class: `datetime`
        """

        return self.__response_time

    @staticmethod
    def __contains(an_object, key_name):

        object_queue = [an_object]
        while len(object_queue) > 0:
            obj = object_queue.pop()

            if isinstance(obj, list):
                for item in obj:
                    object_queue.append(item)
                    continue

            if isinstance(obj, dict):
                for key, value in obj.iteritems():
                    if key == key_name:
                        return value
                    elif isinstance(value, dict):
                        object_queue.append(value)
        return None

    def assert_is_success(self):
        """
        checks that a call was successful. This outputs a consistent messaging
        
        :return: 
        """

        message = None if self.success else 'Response was not successful. Status: {0}'.format(self.status)
        results_code = None

        if isinstance(self.content, dict):
            message = Response.__contains(self.content, 'result_message')
            results_code = Response.__contains(self.content, 'result_code')

        assert_that(self.success, 'RESPONSE ASSERT: {0}({1}) - {2}\n{3}'.format(
            results_code,
            self.status,
            message,
            self
        ))

    def assert_success(self):
        """
        checks that a V2 call was successful. This outputs a consistent messaging

        :return:
        """

        result_code = Response.__contains(self.content, 'result_code')
        code = self.status
        message = None if self.success else 'Response was not successful. Status: {0}'.format(self.status)

        if isinstance(self.content, dict):
            message = Response.__contains(self.content, 'result_message')

        assert_that(
            (self.success, code, result_code),
            contains(True, 200, 'OK'),
            'RESPONSE ASSERT: {0}({1}) - {2}\n{3}'.format(
                result_code,
                self.status,
                message,
                self
            )
        )

    def expect_failure(self, result_code=None, result_message=None, message=None, code=None):
        """
        checks that a failure happened and was the failure can have specified code, message, or result_code.

        :param result_code:
        :param result_message:
        :param message:
        :param code:
        :return:
        """

        assert_that(not self.success, 'Call was successful. Expected failure. {0}'.format(self))

        if code is not None:
            assert_that(self.status, equal_to(code), 'Unexpected Status {0}'.format(self))

        if not (result_code or result_message or message):
            return

        assert_that(
            isinstance(self.content, str),
            equal_to(False),
            'content was not expected to be string: {}'.format(self.content)
        )

        if result_code is not None:
            actual_results_code = Response.__contains(self.content, 'result_code') \
                if isinstance(self.content, dict) else None
            assert_that(actual_results_code, equal_to(result_code), 'Unexpected Result Code {0}'.format(self))

        if result_message is not None:
            actual_result_message = Response.__contains(self.content, 'result_message')
            assert_that(actual_result_message, equal_to(result_message), 'Unexpected result_message {0}'.format(self))

        if message is not None:
            actual_message = Response.__contains(self.content, 'message')
            assert_that(actual_message, equal_to(message), 'Unexpected Message {0}'.format(self))

    def response_hook(self, raw_response, *args, **kwargs):
        """
        :param raw_response: 
        :param args: 
        :param kwargs: 
        :return: 
        """
        log.info('Request: {} {}'.format(self.request.method, self.request.url))
        log.info('Response: {} {}'.format(self.request.method, self.request.url))

        try:
            attach(
                'REQUEST:\n{}\nRESPONSE:\n{}'.format(
                    json.dumps(self.request.details, indent=4, separators=(',', ': ')),
                    raw_response.content
                ),
                '{} {}'.format(self.request.method, self.request.url),
                attachment_type.JSON
            )
        except AttributeError as e:
            log.warn(e)
        except KeyError as e:
            log.warn(e)

    def wrap(self, response):
        """
        :param response:z
        :return: :py:class: `Response`
        """

        assert self.__response is None
        assert self.__response_time is None

        self.__response = response
        self.__response_time = datetime.datetime.now()

        return self
