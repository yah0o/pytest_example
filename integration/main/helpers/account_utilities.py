from random_utilities import RandomUtilities


class AccountUtilities(object):

    @staticmethod
    def create_account(name=None, email_domain='qa.wargaming.net', password='111111', ip='127.0.0.1', activated=1,
                       attrs='user_stated_country=US'):
        if name is None:
            name = 'test_plat_{}'.format(RandomUtilities.create_unique_id())

        email = '{}@{}'.format(name, email_domain)
        return Account(name, password, ip, email, activated, attrs)


class Account(object):

    def __init__(self, name, password, ip, email, activated, attrs):
        self.name = name
        self.email = email
        self.password = password
        self.ip = ip
        self.login = email
        self.activated = activated
        self.attrs = attrs

    def __str__(self):
        return '{} {} {}'.format(self.name, self.login, self.password)
