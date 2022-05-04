from integration.main.request import RequestBuilder


class Banw(object):
    """
    Banw Service
    """

    def __init__(self, url):
        """
        Initialized with Banw base url from the environment YAML file
        :param url: Base url for Banw
        :type url: str
        """
        self.__url = url

    @property
    def service(self):
        return BanwService(self.__url)

    def request(self, path):
        """
        :param path: Path of the http request
        :type path: str
        :return: Request formatted as http
        :rtype: RequestBuilder
        """
        url = 'http://{0}/{1}'.format(self.__url, path)
        return RequestBuilder(url, session=None)


class BanwService(Banw):

    def __init__(self, base_url):
        """
        Initialized with Banw base url passed in from Banw
        :param base_url: Base URL
        :type base_url: str
        """
        Banw.__init__(self, base_url)

    def create_ban(self, account_id, game, project, bantype, author_id, srcapp_id, component=None, started_at=None,
                   comment=None, request_id=None, reason=None, tag=None, expired_at=None, curfew_from=None,
                   action_time=None):
        params = dict(account_id=account_id,
                      author_id=author_id,
                      bantype=bantype,
                      component=component,
                      game=game,
                      srcapp_id=srcapp_id,
                      comment=comment,
                      reason=reason,
                      project=project,
                      request_id=request_id,
                      started_at=started_at,
                      tag=tag,
                      expired_at=expired_at,
                      curfew_from=curfew_from,
                      action_time=action_time)
        params = {k: v for k, v in params.items() if v is not None}
        url = 'bans'
        return self.request(url).data(params).post()

    def get_ban(self, account_id=None, ban_id=None, bantype=None, component=None, game=None, last_id=None, limit=None,
                permanent=None, project=None, request_id=None, started_at=None, status=None):
        params = dict(account_id=account_id,
                      ban_id=ban_id,
                      bantype=bantype,
                      component=component,
                      game=game,
                      last_id=last_id,
                      limit=limit,
                      permanent=permanent,
                      project=project,
                      request_id=request_id,
                      started_at=started_at,
                      status=status)
        params = {k: v for k, v in params.items() if v is not None}
        url = 'bans'
        return self.request(url).params(params).get()
