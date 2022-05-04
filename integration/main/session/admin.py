class AdminAccount(object):

    def __init__(self, username, password=None, pin=None, secret_key=None, name=None):
        self.__username = 'admin@otp.local' if username is '' or username is None else username
        self.__password = None if password is '' or password is None else password
        self.__pin = None if pin is '' else pin
        self.__secret_key = None if secret_key is '' else secret_key

        self.__password = '111111' if password is None and pin is None and secret_key is None else password
        self.__otp = self.__pin is not None and self.__secret_key is not None and self.__password is None
        self.__name = 'admin' if name is '' or name is None else name

    @property
    def username(self):
        """
        :return: str 
        """
        return self.__username

    @property
    def otp(self):
        """
        :return: boolean 
        """

        return self.__otp

    @property
    def password(self):
        """
        :return: str 
        """

        if self.__otp:
            import pyotp
            otp = pyotp.TOTP(self.__secret_key)
            return '{0}{1}'.format(self.__pin, otp.now())

        return self.__password

    @property
    def name(self):
        """
        Admin name
        :return: Admin name
        :rtype: str
        """
        return self.__name
