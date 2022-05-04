from integration.main.helpers import SqlClient
from integration.main.request import RequestBuilder


class Spa(object):
    """
    stub class
    for spa db class
    """

    def __init__(self, url):
        self.__url = url

    @property
    def http(self):
        return SpaHttp(self.__url)


class SpaHttp(object):

    def __init__(self, url):
        self.__base_url = 'http://{}/'.format(url)

    def update_account(self, wgid, update_name, update_value):
        url = '{}spa/accounts/{}/attributes/update/'.format(self.__base_url, wgid)
        return RequestBuilder(url, session=None).headers({
            'Accept': 'application/json',
        }).params({
            'name': update_name,
            'value': update_value
        }).post()

    def delete_account(self, wgid):
        url = '{}spa/accounts/{}/delete/'.format(self.__base_url, wgid)
        return RequestBuilder(url, session=None).headers({
            'Accept': 'application/json',
        }).post()

    def create_external_service_for_account(self, wgid, name, uid, data=None, state=None, _force_create=None):
        url = '{}spa/accounts/{}/externals/create/'.format(self.__base_url, wgid)
        return RequestBuilder(url, session=None).headers({
            'Accept': 'application/json',
        }).params({
            'name': name,
            'uid': uid,
            'data': data,
            'state': state,
            '_force_create': _force_create
        }).post()

    def create_account(self, data):
        url = '{}spa/accounts/create/'.format(self.__base_url)
        return RequestBuilder(url, session=None).headers({
            'Accept': 'application/json',
        }).data(
            data
        ).post()

    def update(self, account_id, name=None, force=None, activated=None, game=None, game_type=None, wot_type=None,
               wowp_type=None, wows_type=None, wotb_type=None, wotg_type=None, autoban_at=None, bigworld=None,
               warplane=None, warship=None, blitz=None, generals=None, in_game=None, delete_from_contact_lists=None):
        url = '{}spa/accounts/{}/update/'.format(self.__base_url, account_id)
        data = dict(name=name,
                    force=force,
                    activated=activated,
                    game=game,
                    game_type=game_type,
                    wot_type=wot_type,
                    wowp_type=wowp_type,
                    wows_type=wows_type,
                    wotb_type=wotb_type,
                    wotg_type=wotg_type,
                    autoban_at=autoban_at,
                    bigworld=bigworld,
                    warplane=warplane,
                    warship=warship,
                    blitz=blitz,
                    generals=generals,
                    in_game=in_game,
                    delete_from_contact_lists=delete_from_contact_lists)
        return RequestBuilder(url, session=None).headers({
            'Accept': 'application/json',
        }).data(
            data
        ).post()

class SpaDatabase(object):

    def __init__(self, db_host, db_port, db_name, db_user, db_password):
        self.__database = SqlClient(db_host, db_port, db_name, db_user, db_password,
                                    db_type=SqlClient.DbType.POSTGRESQL)

    def connect(self):
        if self.__database.connection is not None:
            self.__database.connect()

    def get_tokens(self):
        query = 'select * from spa_token;'
        return self.__database.execute(query)

    def get_account_tokens(self, account_id):
        query = 'select * from spa_token where account_id=%s;' % account_id
        return self.__database.execute(query)

    def get_gamesessions(self):
        query = 'select * from spa_gamesession;'
        return self.__database.execute(query)

    def get_account_gamesessions(self, account_id):
        query = 'select * from spa_gamesession where account_id=%s;' % account_id
        return self.__database.execute(query)
