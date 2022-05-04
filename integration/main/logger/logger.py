import logging
import sys
import time


class UTCFormatter(logging.Formatter):
    converter = time.gmtime


class Logger(object):

    def __init__(self):
        self.__logs = {}

    def log(self, name):
        if name in self.__logs:
            return self.__logs[name]

        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        formatter = UTCFormatter(
            '%(asctime)s.%(msecs)03d [%(threadName)s] %(levelname)s %(name)s.%(module)s - %(message)s',
            '%H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        self.__logs[name] = logger
        return logger

    def get_test_logger(self):
        return self.log('test')


log = Logger().get_test_logger()
