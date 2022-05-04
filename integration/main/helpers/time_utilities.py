from datetime import datetime


class TimeUtilities(object):
    @staticmethod
    def get_current_time():
        """
        Get the current time in ISO-8601 format
        :return: Current time in ISO-8601
        :rtype: str
        """
        return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    @staticmethod
    def get_time_at_timestamp(sec):
        """
        Get the time in ISO-8601 format at passed in UNIX timestamp
        :param sec: UNIX timestamp
        :type sec: float
        :return: Time at UNIX timestamp in ISO-8601 format
        :rtype: str
        """
        return datetime.utcfromtimestamp(sec).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
