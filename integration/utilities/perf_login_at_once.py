import json
import os
import sys
import threading

import requests

from integration.main.helpers import AccountUtilities, Account
from integration.main.services import Freya

title = 'qa.perftest'


class AnAccount(object):

    def __init__(self, freya, name=None, email=None, password=None):
        self.__account = AccountUtilities.create_account() \
            if name is None and email is None and password is None \
            else Account(name, email, password)
        self.__freya = freya
        self.__exc_info = None
        self.__thread = None

    @property
    def as_json(self):
        return {
            'email': self.__account.email,
            'password': self.__account.password,
            'name': self.__account.name
        }

    @property
    def exception(self):
        return self.__exc_info

    @property
    def account(self):
        return self.__account

    def create(self):
        response = self.__freya.tools_gateway.player.new(self.__account.email, self.__account.name,
                                                         self.__account.password, title)
        response.assert_is_success()

    def try_login(self):
        try:
            response = self.__freya.auth_gateway.login_with_email(self.__account.email, self.__account.password)
            response.assert_is_success()
        except Exception, e:
            self.__exc_info = sys.exc_info()

    def threaded_login(self):
        self.__thread = threading.Thread(target=account.try_login)
        self.__thread.setDaemon(True)
        self.__thread.start()

    def login_wait(self):
        self.__thread.join()


freya = Freya(
    'http://platform.sgrd.ix.wgcrowd.io/',
    'ead79acd-d282-49ea-b9d3-2739eabdd00e',
    session=requests.Session(),
    test_domains={}
)
freya.tools_gateway.login.auth_login('admin', '111111')
COUNT = 300
accounts = []

if not os.path.isfile('test_accounts.json'):

    for x in range(0, COUNT):
        account = AnAccount(freya)
        account.create()
        accounts.append(account)
    with open('test_accounts.json', 'w+') as f:

        f.write(json.dumps([account.as_json for account in accounts], indent=4, separators=(',', ': ')))

else:
    with open('test_accounts.json', 'r') as f:
        data = json.load(f)
        for account in data:
            accounts.append(AnAccount(freya, account['name'], account['email'], account['password']))

for account in accounts:
    account.threaded_login()

for account in accounts:
    account.login_wait()

for account in accounts:
    if account.exception is not None:
        print '------'
        print account.account.email
        print account.account.password
        print account.exception
