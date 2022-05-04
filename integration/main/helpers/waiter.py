import time

from integration.main.logger import log


class WaitOn(object):
    SLEEP_TIME = 1

    def __init__(self, method, *args, **kwargs):

        self.__method = method
        self.__args = args
        self.__kwargs = kwargs

        self.__comparison = None
        self.__timeout = None

        self.__return = None

    def until(self, comparison, timeout):

        self.__comparison = comparison
        self.__timeout = timeout
        return self

    def wait(self, message=None):
        timeout_time = time.time() + self.__timeout

        while True:
            self.__return = self.__method(*self.__args, **self.__kwargs)
            if self.__comparison.compare(self.__return):
                return self.__return

            assert time.time() <= timeout_time, '{}:Timeout {} seconds'.format(message, self.__timeout)

            time.sleep(WaitOn.SLEEP_TIME)

    def wait_and_continue(self):
        timeout_time = time.time() + self.__timeout
        while True:
            self.__return = self.__method(*self.__args, **self.__kwargs)
            if self.__comparison.compare(self.__return):
                return self.__return

            if time.time() <= timeout_time:
                return self.__return

            time.sleep(WaitOn.SLEEP_TIME)


class ReturnValue(object):

    def __init__(self, comparison, control, name):
        self.__name = name
        self.__comparison = comparison
        self.__control = control

    @staticmethod
    def IN(control_value):
        return ReturnValue(lambda x, y: x in y, control_value, ReturnValue.IN.__name__)

    @staticmethod
    def NOT_IN(control_value):
        return ReturnValue(lambda x, y: x not in y, control_value, 'NOT IN')

    @staticmethod
    def NOT_EQUAL_TO(control_value):
        return ReturnValue(lambda x, y: x != y, control_value, 'NOT EQUAL TO')

    @staticmethod
    def EQUAL_TO(control_value):
        return ReturnValue(lambda x, y: x == y, control_value, 'EQUAL TO')

    @staticmethod
    def GREATER_THAN(control_value):
        return ReturnValue(lambda x, y: x > y, control_value, 'GREATER THAN')

    @staticmethod
    def LESS_THAN(control_value):
        return ReturnValue(lambda x, y: x < y, control_value, 'LESS THAN')

    @staticmethod
    def LESS_THAN_OR_EQUAL_TO(control_value):
        return ReturnValue(lambda x, y: x <= y, control_value, 'LESS THAN OR EQUAL TO')

    @staticmethod
    def GREATER_THAN_OR_EQUAL_TO(control_value):
        return ReturnValue(lambda x, y: x >= y, control_value, 'GREATER THAN OR EQUAL TO')

    @staticmethod
    def HAS_LENGTH_GREATER_THAN_OR_EQUAL_TO(control_value):
        return ReturnValue(lambda x, y: len(x) >= y, control_value, 'HAS LENGTH GREATER THAN OR EQUAL TO')

    @staticmethod
    def HAS_LENGTH_GREATER_THAN(control_value):
        return ReturnValue(lambda x, y: len(x) > y, control_value, 'HAS LENGTH GREATER THAN')

    @staticmethod
    def HAS_LENGTH(control_value):
        return ReturnValue(lambda x, y: len(x) == y, control_value, 'HAS LENGTH')

    @staticmethod
    def IS_NOT(control_value):
        return ReturnValue(lambda x, y: x is not y, control_value, 'IS NOT')

    def compare(self, value):
        if log is not None:
            log.debug('(value:{0}) {1} (control:{2})'.format(value, self.__name, self.__control))
        return self.__comparison(value, self.__control)
