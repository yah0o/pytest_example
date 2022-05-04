import Queue
import threading


class ThreadQueue(object):

    def __init__(self):

        self.__queue = Queue.Queue()
        self.__results = []
        self.__callback = None
        self.__args = []
        self.__kwargs = {}

    def put(self, data):

        self.__queue.put(data)

    def __run(self):

        assert self.__callback is not None

        while True:
            data = self.__queue.get()
            self.__results.append(self.__callback(data, *self.__args, **self.__kwargs))
            self.__queue.task_done()

    def run(self, thread_count, callback, *args, **kwargs):

        assert callable(callback)

        self.__callback = callback
        self.__args = args
        self.__kwargs = kwargs

        for _ in range(thread_count):
            thread = threading.Thread(target=self.__run)
            thread.daemon = True
            thread.start()

    def wait(self):

        self.__queue.join()
        return self.__results
