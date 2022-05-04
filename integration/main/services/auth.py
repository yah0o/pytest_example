from requests import Session

from gateway import Gateway
from integration.main.request import RequestConstants, Response


class AuthGateway(Gateway):
    """
    Auth Gateway
    """

    def __init__(self, base_url, api_key, session):
        """
        Initializes Gateway with base url and session object, defines API key
        :param base_url: Gateway base url from environment file
        :type base_url: str
        :param api_key: Gateway server API key from environment file
        :type api_key: str
        :param session: Session object which manages and persists settings across requests (cookies, auth, proxies)
        :type session: Session
        """
        Gateway.__init__(self, base_url, session)

        self.api_key = api_key

    def __call__(self, api_key):
        """
        Calls Auth Gateway for usage
        :param api_key: Gateway server API key from environment file
        :type api_key: str
        :return: Auth Gateway object
        :rtype: AuthGateway
        """

        self.api_key = api_key
        return self

    def ping(self):
        """
        Ping Auth Gateway
        :return: Ping response from Auth Gateway
        :rtype: Response
        """

        return self.request('auth/api/v1/ping').get()

    def ping_client(self):
        """
        Ping Auth Gateway Client
        :return: Ping response from Auth Gateway Client
        :rtype: Response
        """

        return self.request('auth/api/v1/ping/client').get()

    def login_with_email(
            self,
            email,
            password,
            region=RequestConstants.Parameters.OPTIONAL,
            fingerprint=RequestConstants.Parameters.OPTIONAL,
            create_remember_me=RequestConstants.Parameters.OPTIONAL,
            client_ip=RequestConstants.Parameters.OPTIONAL,
            auth_token_target_application=RequestConstants.Parameters.OPTIONAL,
            content_type=RequestConstants.ContentTypes.JSON,
            tracking_id=RequestConstants.Parameters.OPTIONAL,
            client_language=RequestConstants.Parameters.OPTIONAL):
        """
        Login through Auth Gateway with email
        :param email: Wargaming account email
        :type email: str
        :param password: Wargaming account password
        :type password: str
        :param region: SPA account region
        :type region: str
        :param fingerprint: Device fingerprint to lock session this device. Required if creating a remember me token
        :type fingerprint: str
        :param create_remember_me: Boolean indicating if a RememberMe (Token 2) should be created
        :type create_remember_me: bool
        :param client_ip: Client IP address
        :type client_ip: str
        :param auth_token_target_application: If not null, will create an auth token for specified application
        :type auth_token_target_application: str
        :param tracking_id: x-np-tracking-id
        :type tracking_id: str
        :param content_type: Content type as json or msg-pack
        :type content_type: RequestConstants
        :param client_language: Client language
        :type client_language: Str
        :return: Response to login with email request
        :rtype: Response
        """

        return self.request(
            'auth/api/v1/loginWithEmail'
        ).headers({
            'x-freya-server-api-key': self.api_key,
            'x-np-tracking-id': tracking_id
        }).json({
            'header': {},
            'body': {
                'email': email,
                'password': password,
                'region': region,
                'fingerprint': fingerprint,
                'create_remember_me': create_remember_me,
                'client_ip': client_ip,
                'auth_token_target_application': auth_token_target_application,
                'client_language': client_language
            }
        }).post(content_type)

    def login_with_auth_token(
            self,
            auth_token,
            wgid,
            region=RequestConstants.Parameters.OPTIONAL,
            fingerprint=RequestConstants.Parameters.OPTIONAL,
            create_remember_me=True,
            client_ip=RequestConstants.Parameters.OPTIONAL,
            auth_token_target_application=RequestConstants.Parameters.OPTIONAL,
            content_type=RequestConstants.ContentTypes.JSON,
            client_language=RequestConstants.Parameters.OPTIONAL):
        """
        Logging in through Auth Gateway with authorization token
        :param auth_token: Wargaming Auth Token (Token 1)
        :type auth_token: str
        :param wgid: WGID of account (SPA ID)
        :type wgid: int
        :param region: SPA region of account
        :type region: str
        :param fingerprint: Device fingerprint to lock session this device. Required if creating a remember me token
        :type fingerprint: str
        :param create_remember_me: Boolean indicating if a RememberMe (Token 2) should be created
        :type create_remember_me: bool
        :param client_ip: Client IP address
        :type client_ip: str
        :param auth_token_target_application: If not null, will create an auth token for specified application
        :type auth_token_target_application: str
        :param content_type: Content type as json or msg-pack
        :type content_type: RequestConstants
        :param client_language: Client language
        :type client_language: Str
        :return: Response to login with auth token request
        :rtype: Response
        """

        return self.request(
            'auth/api/v1/loginWithAuthToken'
        ).headers({
            'x-freya-server-api-key': self.api_key,
        }).json({
            'header': {},
            "body": {
                "region": region,
                "auth_token": auth_token,
                "wgid": wgid,
                "fingerprint": fingerprint,
                "create_remember_me": create_remember_me,
                "client_ip": client_ip,
                "auth_token_target_application": auth_token_target_application,
                "client_language": client_language
            }
        }).post(content_type)

    def login_with_remember_me(
            self,
            remember_me,
            region,
            fingerprint=RequestConstants.Parameters.OPTIONAL,
            client_ip=RequestConstants.Parameters.OPTIONAL,
            auth_token_target_application=RequestConstants.Parameters.OPTIONAL,
            content_type=RequestConstants.ContentTypes.JSON,
            client_language=RequestConstants.Parameters.OPTIONAL):
        """
        Logging in through Auth gateway with remember me
        :param remember_me: Remember Me token from createRememberMeToken
        :type remember_me: str
        :param region: SPA Region of where the call is made
        :type region: str
        :param fingerprint: Device fingerprint to lock session this device. Required if creating a remember me token
        :type fingerprint: str
        :param client_ip: IP address of client
        :type client_ip: str
        :param auth_token_target_application: If not null, will create an auth token for specified application
        :type auth_token_target_application: str
        :param content_type: Content type as json or msg-pack
        :type content_type: RequestConstants
        :param client_language: Client language
        :type client_language: Str
        :return: Response to login with remember me request
        :rtype: Response
        """

        return self.request(
            'auth/api/v1/loginWithRememberMe'
        ).headers({
            'x-freya-server-api-key': self.api_key,
        }).json({
            "header": {},
            "body": {
                "fingerprint": fingerprint,
                "region": region,
                "remember_me": remember_me,
                "client_ip": client_ip,
                "auth_token_target_application": auth_token_target_application,
                "client_language": client_language
            }
        }).post(content_type)
