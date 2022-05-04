import time

from gateway import Gateway
from integration.main.patterns import Singleton
from integration.main.request import RequestConstants, Response
from integration.main.services.items import LegacyProductItem
from requests import Session


class ToolsGateway(Gateway):
    """
    Tools V1 Gateway
    """

    def __init__(self, base_url, session):
        """
        Initializes Gateway with base url and session object
        :param base_url: Gateway base url from environment file
        :type base_url: str
        :param session: Session object which manages and persists settings across requests (cookies, auth, proxies)
        :type session: Session
        """
        Gateway.__init__(self, base_url, session)

    @property
    def player(self):
        """
        Retrieves Tools V1 Gateway Player Object
        :return: ToolsPlayer object
        :rtype: ToolsPlayer
        """

        return ToolsPlayer(self.url, self.session)

    @property
    def login(self):
        """
        Retrieves Tools V1 Gateway Login Object
        :return: ToolsLogin object
        :rtype: ToolsLogin
        """

        return ToolsLogin(self.url, self.session)

    @property
    def gg(self):
        """
        Retrieves Tools V1 Gateway GG Object
        :return: ToolsGG object
        :rtype: ToolsGG
        """

        return ToolsGG(self.url, self.session)

    @property
    def catalog(self):
        """
        Retrieves Tools V1 Gateway Catalog Object
        :return: ToolsCatalog object
        :rtype: ToolsCatalog
        """

        return ToolsCatalog(self.url, self.session)

    @property
    def title(self):
        """
        Retrieves Tools V1 Gateway Title Object
        :return: ToolsTitle object
        :rtype: ToolsTitle
        """

        return ToolsTitle(self.url, self.session)

    @property
    def operations(self):
        """
        Retrieves Tools V1 Gateway Operations Object
        :return: ToolsOperations object
        :rtype: ToolsOperations
        """

        return ToolsOperations(self.url, self.session)

    @property
    def extension(self):
        """
        Retrieves Tools V1 Gateway Extension Object
        :return: ToolsExtension object
        :rtype: ToolsExtension
        """

        return ToolsExtension(self.url, self.session)

    @property
    def working_catalog(self):
        """
        Retrieves Tools V1 Gateway Working Catalog Object
        :return: ToolsWorkingCatalog object
        :rtype: ToolsWorkingCatalog
        """

        return ToolsWorkingCatalog(self.url, self.session)

    @property
    def publish_catalog(self):
        """
        Retrieves Tools V1 Gateway Publish Catalog Object
        :return: ToolsPublishCatalog object
        :rtype: ToolsPublishCatalog
        """

        return ToolsPublishCatalog(self.url, self.session)

    @property
    def published_catalog(self):
        """
        Retrieves Tools V1 Gateway Published Catalog Object
        :return: ToolsPublishedCatalog object
        :rtype: ToolsPublishedCatalog
        """

        return ToolsPublishedCatalog(self.url, self.session)

    @property
    def working_catalog_entities(self):
        """
        Retrieves Tools V1 Gateway Working Catalog Entities Object
        :return: ToolsWorkingCatalogEntities object
        :rtype: ToolsWorkingCatalogEntities
        """

        return ToolsWorkingCatalogEntities(self.url, self.session)

    def ping(self):
        """
        Ping Tools V1 Gateway
        :return: Ping response from Tools V1 Gateway
        :rtype: Response
        """

        return self.request("tools/api/v1/ping").get()


class ToolsPlayer(Gateway):

    def new(self, email, name, password, title_code, region=RequestConstants.Parameters.OPTIONAL,
            country=RequestConstants.Parameters.OPTIONAL):
        """
        Create a player in SPA
        :param email: Email to register to the SPA player account
        :type email: str
        :param name: Name to register to the SPA player account
        :type name: str
        :param password: Password set to protect the SPA player account
        :type password: str
        :param title_code: Title to register to the SPA player account
        :type title_code: str
        :param region: Region to register to the SPA player account
        :type region: str
        :param country: Country to register to the SPA player account
        :type country: str
        :return: Response to player creation request
        :rtype: Response
        """

        return self.request('tools/api/v1/player/').headers({
            'Content-Type': RequestConstants.ContentTypes.URL_ENCODED,
            'Accept': RequestConstants.ContentTypes.JSON,
        }).data({
            'login': email,
            'nickname': name,
            'password': password,
            'region': region,
            'title_code': title_code,
            'country': country
        }).post()

    def wipe_profile(self, title_code, profile_id):
        """
        Delete a specific profile, including entitlements and currencies
        :param title_code: Code of title
        :type title_code: str
        :param profile_id: Profile ID to wipe
        :type profile_id: int
        :return: Response to wipe profile request
        :rtype: Response
        """

        return self.request(
            'tools/api/v1/player/wipeProfile/{0}/{1}'.format(title_code, profile_id)
        ).post()

    def regions(self):
        """
        Retrieve a list of regions
        :return: Response to Tools V1 Service regions request
        :rtype: Response
        """

        return self.request('tools/api/v1/player/regions').headers({
            'Accept': RequestConstants.ContentTypes.JSON,
        }).get()

    def get_full_inventory(self, title_code, profile_id):
        """
        Retrieves the full inventory of the profile
        :param title_code: Code of title
        :type title_code: str
        :param profile_id: Profile ID to retrieve inventory
        :type profile_id: int
        :return: Response to Tools V1 Service get full inventory request
        :rtype: Response
        """

        return self.request('tools/api/v1/player/{0}/getFullInventory'.format(title_code)).json({
            "header": {},
            "body": {
                "profile_id": profile_id
            }
        }).post()

    def consume_currency(
            self,
            title_code,
            profile_id,
            currency_code,
            amount,
            transaction_id,
            meta=RequestConstants.Parameters.OPTIONAL):
        """
        Consumes currency of the specified profile
        :param title_code: Code of title
        :type title_code: str
        :param profile_id: Profile ID to consume the currency(ies)
        :type profile_id: int
        :param currency_code: Currency code to consume
        :type currency_code: str
        :param amount: Amount of currency to consume
        :type amount: str
        :param transaction_id: UUID supplied for the consume request
        :type transaction_id: str
        :param meta: Map of metadata attached to the consume currency request
        :type meta: dict of (str, object)
        :return: Response to Tools V1 Service consume currency request
        :rtype: Response
        """

        return self.request('tools/api/v1/player/{0}/consumeCurrency'.format(title_code)).json({
            "header": {},
            "body": {
                "transaction_id": transaction_id,
                "profile_id": profile_id,
                "currency_code": currency_code,
                "amount": amount,
                "meta": meta,
            }
        }).post()

    def consume_entitlement(
            self,
            title_code,
            profile_id,
            entitlement_code,
            amount,
            transaction_id=RequestConstants.Parameters.OPTIONAL,
            meta=RequestConstants.Parameters.OPTIONAL):
        """
        Consume entitlement of the specified profile
        :param title_code: Code of title
        :type title_code: str
        :param profile_id: Profile ID to consume the entitlement(s)
        :type profile_id: int
        :param entitlement_code: Entitlement code to consume
        :type entitlement_code: str
        :param amount: Amount of entitlement to consume
        :type amount: str
        :param transaction_id: UUID supplied for the consume request
        :type transaction_id: str
        :param meta: Map of metadata attached to the consume entitlement request
        :type meta: dict of (str, object)
        :return: Response to Tools V1 Service consume entitlement request
        :rtype: Response
        """

        return self.request('tools/api/v1/player/{0}/consumeEntitlement'.format(title_code)).json({
            "header": {},
            "body": {
                "transaction_id": transaction_id,
                "profile_id": profile_id,
                "entitlement_code": entitlement_code,
                "amount": amount,
                "meta": meta,
            }
        }).post()

    def purchase_product(
            self,
            title_code,
            destination_profile_id,
            source_profile_id,
            product_code,
            amount,
            expected_prices,
            transaction_id,
            storefront,
            coupons=RequestConstants.Parameters.OPTIONAL,
            meta=RequestConstants.Parameters.OPTIONAL):
        """
        Purchase specified product using Tools V1 Service
        :param title_code: Code of title
        :type title_code: str
        :param destination_profile_id: Profile ID where purchased product(s) are going
        :type destination_profile_id: int
        :param source_profile_id: Profile ID making the purchase
        :type source_profile_id: int
        :param product_code: Code of product to purchase
        :type product_code: str
        :param amount: Amount of product to purchase
        :type amount: int
        :param expected_prices: Expected price(s) of product
        :type expected_prices: list of LegacyProductItem
        :param transaction_id: UUID supplied for the purchase product request
        :type transaction_id: str
        :param storefront: Code of storefront
        :type storefront: str
        :param coupons: Coupons used for purchase product request
        :type coupons: list of str
        :param meta: Map of metadata attached to the purchase
        :type meta: dict of (str, object)
        :return: Response to Tools V1 Service purchase product request
        :rtype: Response
        """

        return self.request('tools/api/v1/player/{0}/purchaseProduct'.format(title_code)).json({
            "header": {},
            "body": {
                "transaction_id": transaction_id,
                "destination_profile_id": destination_profile_id,
                "source_profile_id": source_profile_id,
                "product": {
                    "product_code": product_code,
                    "amount": str(amount),
                    "coupons": coupons
                },
                "storefront": storefront,
                "expected_prices": expected_prices,
                "meta": meta,
            }
        }).post()

    def grant_entitlement(
            self,
            title_code,
            profile_id,
            entitlement_code,
            amount,
            transaction_id=RequestConstants.Parameters.OPTIONAL,
            meta=RequestConstants.Parameters.OPTIONAL):
        """
        Grant entitlement(s) to a profile using Tools V1 Service
        :param title_code: Code of title
        :type title_code: str
        :param profile_id: Profile ID of where the granted entitlement(s) are going
        :type profile_id: int
        :param entitlement_code: Code of entitlement to grant
        :type entitlement_code: str
        :param amount: Amount of entitlement to grant
        :type amount: int
        :param transaction_id: UUID supplied for the grant entitlement request
        :type transaction_id: str
        :param meta: Map of metadata attached to the grant entitlement request
        :type meta: dict of (str, object)
        :return: Response to Tools V1 Service grant entitlement request
        :rtype: Response
        """

        return self.request('tools/api/v1/player/{0}/grantEntitlement'.format(title_code)).json({
            "header": {},
            "body": {
                "transaction_id": transaction_id,
                "profile_id": profile_id,
                "entitlement_code": entitlement_code,
                "amount": amount,
                "meta": meta,
            }
        }).post()

    def grant_currency(
            self,
            title,
            profile_id,
            currency_code,
            amount,
            transaction_id,
            meta=RequestConstants.Parameters.OPTIONAL):
        """
        Grant currency(s) to a profile using Tools V1 Service
        :param title: Code of title
        :type title: str
        :param profile_id: Profile ID of where the granted currency(ies) are going
        :type profile_id: int
        :param currency_code: Code of currency to grant
        :type currency_code: str
        :param amount: Amount of currency to grant
        :type amount: str
        :param transaction_id: UUID supplied for the grant currency request
        :type transaction_id: str
        :param meta: Map of metadata attached to the grant currency request
        :type meta: dict of (str, object)
        :return: Response to Tools V1 Service grant currency request
        :rtype: Response
        """

        return self.request('tools/api/v1/player/{0}/grantCurrency'.format(title)).json({
            "header": {},
            "body": {
                "transaction_id": transaction_id,
                "profile_id": profile_id,
                "currency_code": currency_code,
                "amount": amount,
                "meta": meta,
            }
        }).post()

    def get_player_list(
            self,
            region=RequestConstants.Parameters.OPTIONAL,
            start_id=RequestConstants.Parameters.OPTIONAL,
            name_prefix=RequestConstants.Parameters.OPTIONAL,
            limit=RequestConstants.Parameters.OPTIONAL,
            state_mask=RequestConstants.Parameters.OPTIONAL):
        """
        Retrieve a list of players using Tools V1 Service
        :param region: Region of player
        :type region: str
        :param start_id: Numbers which the Profile IDs start with in query
        :type start_id: long
        :param name_prefix: Name prefix to include in query
        :type name_prefix: str
        :param limit: Limit of search request
        :type limit: int
        :param state_mask: Mask state
        :type state_mask: str
        :return: Response to Tools V1 Service get player list request
        :rtype: Response
        """

        return self.request('tools/api/v1/player/name').headers({
            'Accept': RequestConstants.ContentTypes.JSON,
        }).params({
            'region': region,
            'start_id': start_id,
            'name_prefix': name_prefix,
            'limit': limit,
            'state_mask': state_mask,
        }).get()

    def get_player_by_id(
            self,
            wgid,
            region=RequestConstants.Parameters.OPTIONAL,
            game_state=RequestConstants.Parameters.OPTIONAL):
        """
        Retrieves a player by ID using Tools V1 Service
        :param wgid: WGID of player profile to retrieve
        :type wgid: str
        :param region: Region code of player profile
        :type region: str
        :param game_state: Game state
        :type game_state: str
        :return: Response to Tools V1 Service get player by id request
        :rtype: Response
        """

        return self.request('tools/api/v1/player/id/{0}'.format(wgid)).params({
            'region': region,
            'game_state': game_state,
        }).get()

    def get_player_by_name(self, name, region=RequestConstants.Parameters.OPTIONAL):
        """
        Retrieves a player by name using Tools V1 Service
        :param name: Name of profile to retrieve
        :type name: str
        :param region: Region code of player profile
        :type region: str
        :return: Response to Tools V1 Service get player by name request
        :rtype: Response
        """

        return self.request('tools/api/v1/player/name/{0}'.format(name)).headers({
            'Accept': RequestConstants.ContentTypes.JSON
        }).params({
            'region': region
        }).get()

    def get_player_by_login(self, email, region=RequestConstants.Parameters.OPTIONAL):
        """
        Retrieves a player by login using Tools V1 Service
        :param email: Email of login to retrieve
        :type email: str
        :param region: Region code of player profile
        :type region: str
        :return: Response to Tools V1 Service get player by login request
        :rtype: Response
        """

        return self.request('tools/api/v1/player/login/{0}'.format(email)).params({
            'region': region
        }).get()

    def get_bans(self, wgid, only_active=True):
        """
        Retrieve ban(s) associated with WGID using Tools V1 Service
        :param wgid: WGID of profile
        :type wgid: long
        :param only_active: Active flag for bans
        :type only_active: bool
        :return: Response to Tools V1 Service get bans request
        :rtype: Response
        """

        return self.request('tools/api/v1/player/get-bans').params({
            'account_id': wgid,
            'only_active': only_active,
        }).get()

    def delete_ban(self, ban_id):
        """
        Delete ban using Tools V1 Service
        :param ban_id: Ban ID issued
        :type ban_id: long
        :return: Response to Tools V1 Service delete ban request
        :rtype: Response
        """

        return self.request('tools/api/v1/player/delete-ban').params({
            'ban_id': ban_id,
        }).get()

    def create_ban(self, wgid, reason, author, game, project, expires):
        """
        Create a ban to a specified WGID using Tools V1 Service
        :param wgid: WGID of profile
        :type wgid: long
        :param reason: Ban reason
        :type reason: str
        :param author: Author creating the ban
        :type author: str
        :param game: Game code to ban
        :type game: str
        :param project: Project code to ban
        :type project: str
        :param expires: Expiration in UTC time format
        :type expires: long
        :return: Response to Tools V1 Service create ban request
        :rtype: Response
        """
        return self.request('tools/api/v1/player/create-ban').params({
            'account_id': wgid,
            'reason': reason,
            'author': author,
            'game': game,
            'project': project,
            'expires': expires,
        }).get()

    def kick_by_wgid(self, wgid):
        """
        Kick WGID from the platform by invalidating their session and notifying the game server using Tools V1 Service
        :param wgid: WGID of account
        :type wgid: long
        :return: Response to Tools V1 Service kick by wgid request
        :rtype: Response
        """

        return self.request(
            'tools/api/v1/player/kick/wg/{0}'.format(wgid)
        ).post()

    def kick_by_wgid_and_title(self, title_code, wgid):
        """
        Kick WGID from the platform by invalidating their session and notifying the game server using Tools V1 Service
        :param title_code: Code of title
        :type title_code: str
        :param wgid: WGID of account
        :type wgid: long
        :return: Response to Tools V1 Service kick by wgid and title request
        :rtype: Response
        """

        return self.request(
            'tools/api/v1/player/kick/{0}/wg/{1}'.format(title_code, wgid)
        ).post()

    def kick_by_title_and_profile_id(self, title_code, profile_id):
        """
        Kick Profile ID from the platform by invalidating their session and notifying the game server using Tools V1 Service
        :param title_code: Code of title
        :type title_code: str
        :param profile_id: Profile ID of account
        :type profile_id: long
        :return: Response to Tools V1 Service kick by title and profile id request
        :rtype: Response
        """

        return self.request(
            'tools/api/v1/player/kick/{0}/profile/{1}'.format(title_code, profile_id)
        ).post()

    def create_title_profile(self, wgid, title_code, region=RequestConstants.Parameters.OPTIONAL):
        """
        Create a player profile by WGID and title code using Tools V1 Service
        :param wgid: WGID of account
        :type wgid: str
        :param title_code: Code of title
        :type title_code: str
        :param region: Region code
        :type region: str
        :return: Response to Tools V1 Service create title profile request
        :rtype: Response
        """

        return self.request('tools/api/v1/player/id/{0}/profile/{1}'.format(wgid, title_code)).headers({
            'Accept': RequestConstants.ContentTypes.JSON,
            'Content-Type': RequestConstants.ContentTypes.URL_ENCODED,
        }).data({
            'region': region
        }).post()

    def get_player_profile(self, wgid, title_code):
        """
        Retrieves player profile by WGID and title code using Tools V1 Service
        :param wgid: WGID of account
        :type wgid: str
        :param title_code: Code of title
        :type title_code: str
        :return: Response to Tools V1 Service get player profile request
        :rtype: Response
        """

        return self.request('tools/api/v1/player/id/{0}/profile/{1}'.format(wgid, title_code)).headers({
            'Accept': RequestConstants.ContentTypes.JSON
        }).get()


class ToolsCatalog(Gateway):

    def catalog(self, catalog_code):
        """
        Retrieve a specified catalog using Tools V1 Service
        :param catalog_code: Code of catalog to retrieve
        :type catalog_code: str
        :return: Response to Tools V1 Service catalog request
        :rtype: Response
        """

        return self.request('tools/api/v1/catalog/{0}'.format(catalog_code)).get()

    def catalog_currencies(self, catalog_code):
        """
        Retrieve the currency(ies) of a specified catalog using Tools V1 Service
        :param catalog_code: Code of catalog to retrieve the currency(ies)
        :type catalog_code: str
        :return: Response to Tools V1 Service catalog currencies request
        :rtype: Response
        """

        return self.request('tools/api/v1/catalog/{0}/currency'.format(catalog_code)).get()

    def catalog_storefronts(self, catalog_code):
        """
        Retrieve the storefront(s) of a specified catalog using Tools V1 Service
        :param catalog_code: Code of catalog to retrieve the storefront(s)
        :type catalog_code: str
        :return: Response to Tools V1 Service catalog storefronts request
        :rtype: Response
        """

        return self.request('tools/api/v1/catalog/{0}/storefront'.format(catalog_code)).get()

    def catalog_products(self, catalog_code):
        """
        Retrieve the product(s) of a specified catalog using Tools V1 Service
        :param catalog_code: Code of catalog to retrieve the product(s)
        :type catalog_code: str
        :return: Response to Tools V1 Service catalog products request
        :rtype: Response
        """

        return self.request('tools/api/v1/catalog/{0}/product'.format(catalog_code)).get()

    def catalog_entitlements(self, catalog_code):
        """
        Retrieve the entitlement(s) of a specified catalog using Tools V1 Service
        :param catalog_code: Code of catalog to retrieve the entitlement(s)
        :type catalog_code: str
        :return: Response to Tools V1 Service catalog entitlements request
        :rtype: Response
        """

        return self.request('tools/api/v1/catalog/{0}/entitlement'.format(catalog_code)).get()

    def catalog_specific_currency(self, catalog_code, currency_code):
        """
        Retrieve a specified currency of a specified catalog using Tools V1 Service
        :param catalog_code: Code of catalog to retrieve the specified currency
        :type catalog_code: str
        :param currency_code: Code of currency to retrieve
        :type currency_code: str
        :return: Response to Tools V1 Service catalog specific currency request
        :rtype: Response
        """

        return self.request('tools/api/v1/catalog/{0}/currency/{1}'.format(catalog_code, currency_code)).get()

    def catalog_specific_storefront(self, catalog_code, storefront_code):
        """
        Retrieve a specified storefront of a specified catalog using Tools V1 Service
        :param catalog_code: Code of catalog to retrieve the specified storefront
        :type catalog_code: str
        :param storefront_code: Code of storefront to retrieve
        :type storefront_code: str
        :return: Response to Tools V1 Service catalog specific storefront request
        :rtype: Response
        """

        return self.request('tools/api/v1/catalog/{0}/storefront/{1}'.format(catalog_code, storefront_code)).get()

    def catalog_specific_product(self, catalog_code, product_code):
        """
        Retrieve a specified product of a specified catalog using Tools V1 Service
        :param catalog_code: Code of catalog to retrieve the specified product
        :type catalog_code: str
        :param product_code: Code of product to retrieve
        :type product_code: str
        :return: Response to Tools V1 Service catalog specific product request
        :rtype: Response
        """

        return self.request('tools/api/v1/catalog/{0}/product/{1}'.format(catalog_code, product_code)).get()

    def catalog_specific_entitlement(self, catalog_code, entitlement_code):
        """
        Retrieve a specified entitlement of a specified catalog using Tools V1 Service
        :param catalog_code: Code of catalog to retrieve the specified entitlement
        :type catalog_code: str
        :param entitlement_code: Code of entitlement to retrieve
        :type entitlement_code: str
        :return: Response to Tools V1 Service catalog specific entitlement request
        :rtype: Response
        """

        return self.request('tools/api/v1/catalog/{0}/entitlement/{1}'.format(catalog_code, entitlement_code)).get()


class AdminLoginStore(object):
    # needs to be a singleton because this needs to persist throughout everything
    # to make sure not to ever lock out an account
    __metaclass__ = Singleton

    def __init__(self):
        self.failed_attempts = 0
        self.last_successful_response = None
        self.has_failed = False


class ToolsLogin(Gateway):

    def auth_login(self, username, otp, secret_override=RequestConstants.Parameters.OPTIONAL):
        """
        Tools V1 Service login
        :param username: Login username
        :type username: str
        :param otp: Login otp or password
        :type otp: str
        :param secret_override: Override code
        :type secret_override: str
        :return: Response to Tools V1 Service auth login request
        :rtype: Response
        """

        persist_store = AdminLoginStore()

        # do not log in twice in case of OTP
        if self.session.cookies.get('JSESSIONID') is None:

            login_response = self.request('tools/api/v1/auth/login').data({
                'username': username,
                'secret_override': secret_override,
                'otp': otp,
            }).post()

            if login_response.success:
                persist_store.last_successful_response = login_response
            else:
                persist_store.failed_attempts += 1

            return login_response

        # this assert should never trigger because if session has
        # JSESSIONID then there must have been one last successful call
        assert persist_store.last_successful_response is not None

        return persist_store.last_successful_response

    def auth_adfs_login(self, username, password):
        """
        Tools V1 ADFS login
        :param username: Login username
        :type username: str
        :param password: Login password
        :type password: str
        :return: Response to Tools V1 ADFS login request
        :rtype: Response
        """

        return self.request('tools/api/v1/auth/loginAdfs').data({
            'username': username,
            'password': password
        }).post()

    def auth_login_password(self, username, password):
        """
        Tools V1 login
        :param username: Login username
        :type username: str
        :param password: Login password
        :type password: str
        :return: Response to Tools V1 login request
        :rtype: Response
        """

        return self.request('tools/api/v1/auth/loginPassword').data({
            'username': username,
            'password': password
        }).post()

    def auth_logout(self):
        """
        Tools V1 Service logout
        :return: Response to Tools V1 Service auth logout request
        :rtype: Response
        """

        logout_response = self.request('tools/api/v1/auth/logout').get()
        if logout_response.success:
            self.session.cookies.clear()
        return logout_response

    def user_info(self):
        """
        Retrieve user info for the admin account that is logged in
        :return: Response to Tools V1 Service user info request
        :rtype: Response
        """

        return self.request('tools/api/v1/auth/userinfo').get()

    def full_user_info(self):
        """
        Retrieve full user info for the admin account that is logged in
        :return: Response to Tools V1 Service full user info request
        :rtype: Response
        """

        return self.request('tools/api/v1/auth/fulluserinfo').get()

    def check_permission(self, permission):
        """
        Retrieve the admin permissions
        :param permission: Permission to check
        :type permission: str
        :return: Response to Tools V1 Service check permission request
        :rtype: Response
        """

        return self.request('tools/api/v1/auth/check/permission').params({
            'permission': permission,
        }).get()

    def search_users(self, params):
        """
        Retrieve users specified by search parameters
        :param params: Parameters to search users
        :type params: dict of (str, object)
        :return: Response to Tools V1 Service search users request
        :rtype: Response
        """

        return self.request('tools/api/v1/auth/searchusers').params(params).get()


class ToolsGG(Gateway):

    def discover(self, title_code, server_api_key):
        """
        Discover GGAPI methods using Tools V1 Service
        :param title_code: Code of title
        :type title_code: str
        :param server_api_key: Server API Key
        :type server_api_key: str
        :return: Response to Tools V1 Service discover request
        :rtype: Response
        """

        return self.request('tools/api/v1/gg/{0}/discover'.format(title_code)).headers({
            'x-freya-server-api-key': server_api_key
        }).get()

    def methods(self, title_code, server_api_key):
        """
        Retrieve GGAPI methods using Tools V1 Service
        :param title_code: Code of title
        :type title_code: str
        :param server_api_key: Server API Key
        :type server_api_key: str
        :return: Response to Tools V1 Service methods request
        :rtype: Response
        """

        return self.request('tools/api/v1/gg/{0}/methods'.format(title_code)).headers({
            'x-freya-server-api-key': server_api_key
        }).get()

    def execute(self, title_code, method_name, server_api_key, extra_params=RequestConstants.Parameters.OPTIONAL):
        """
        Execute GGAPI method using Tools V1 Service
        :param title_code: Code of title
        :type title_code: str
        :param method_name: Name of method
        :type method_name: str
        :param server_api_key: Server API key
        :type server_api_key: str
        :param extra_params: Any extra parameters to the execution request
        :type extra_params: dict of (str, object)
        :return: Response to Tools V1 Service execute request
        :rtype: Response
        """

        return self.request('tools/api/v1/gg/{0}/execute'.format(title_code)).headers({
            'x-freya-server-api-key': server_api_key,
        }).json({
            "method_name": method_name,
            "version": 1,
            "params": extra_params
        }).post()


class ToolsTitle(Gateway):

    def title_list(
            self,
            page_number=1,
            page_size=10,
            order_direction='ASC',
            order_by='TITLE_ID',
            code=RequestConstants.Parameters.OPTIONAL,
            friendly_name=RequestConstants.Parameters.OPTIONAL,
            title_id=RequestConstants.Parameters.OPTIONAL,
            title_group_ui=RequestConstants.Parameters.OPTIONAL,
            tags=RequestConstants.Parameters.OPTIONAL,
            search=RequestConstants.Parameters.OPTIONAL
    ):
        """
        Retrieve list of titles using Tools V1 Service
        :param page_number: Page number
        :type page_number: int
        :param page_size: Page size of results
        :type page_size: int
        :param order_direction: Order direction of results
        :type order_direction: str
        :param order_by: Order by parameter for results
        :type order_by: str
        :param code: Code of titles
        :type code: list of str
        :param friendly_name: Friendly name of titles
        :type friendly_name: list of str
        :param title_id: Title IDs
        :type title_id: list of str
        :param title_group_ui: Title group UIDs
        :type title_group_ui: list of str
        :param tags: Filter results by tags
        :type tags: list of str
        :param search: Filter results by any input string
        :type search: list of str
        :return: Response to Tools V1 Service title list request
        :rtype: Response
        """

        return self.request('tools/api/v1/title/').params({
            'page_number': page_number,
            'page_size': page_size,
            'order_direction': order_direction,
            'order_by': order_by,
            'code': code,
            'friendly_name': friendly_name,
            'title_id': title_id,
            'title_group_ui': title_group_ui,
            'tags': tags,
            'search': search
        }).get()

    def add_title(
            self,
            id,
            code,
            type,
            notification_single_purchase,
            notification_multi_purpose,
            pop,
            pgn,
            view_entitlement_code=RequestConstants.Parameters.OPTIONAL,
            access_entitlement_code=RequestConstants.Parameters.OPTIONAL,
            comment=RequestConstants.Parameters.OPTIONAL,
            webhook_endpoint=RequestConstants.Parameters.OPTIONAL,
            ggapi_discovery=RequestConstants.Parameters.OPTIONAL,
            ggapi_method=RequestConstants.Parameters.OPTIONAL,
            webhook_gzip_accepted=RequestConstants.Parameters.OPTIONAL,
            webhook_security_token=RequestConstants.Parameters.OPTIONAL,
            automatic_registration=RequestConstants.Parameters.OPTIONAL,
            internal=RequestConstants.Parameters.OPTIONAL,
            event_schemas=RequestConstants.Parameters.OPTIONAL,
            document_schemas=RequestConstants.Parameters.OPTIONAL,
            namespaces=RequestConstants.Parameters.OPTIONAL,
            title_versions=RequestConstants.Parameters.OPTIONAL,
            title_permissions=RequestConstants.Parameters.OPTIONAL,
            permitting_titles=RequestConstants.Parameters.OPTIONAL,
            enforce_prerequisites=RequestConstants.Parameters.OPTIONAL,
            shared_titles=RequestConstants.Parameters.OPTIONAL,
            title_group=RequestConstants.Parameters.OPTIONAL,
            title_group_ui=RequestConstants.Parameters.OPTIONAL,
            title_id=RequestConstants.Parameters.OPTIONAL,
            friendly_name=RequestConstants.Parameters.OPTIONAL,
            description=RequestConstants.Parameters.OPTIONAL,
            tags=RequestConstants.Parameters.OPTIONAL,
            sentinel_uuid=RequestConstants.Parameters.OPTIONAL,
            branches=RequestConstants.Parameters.OPTIONAL,
            default_language=RequestConstants.Parameters.OPTIONAL,
            required_languages=RequestConstants.Parameters.OPTIONAL,
            optional_languages=RequestConstants.Parameters.OPTIONAL,
            next_schema_versions=RequestConstants.Parameters.OPTIONAL,
            created_at=RequestConstants.Parameters.OPTIONAL,
            updated_at=RequestConstants.Parameters.OPTIONAL
    ):
        """
        Add a new title using Tools V1 Service
        :param id: SPA game ID
        :type id: str
        :param code: Code of title
        :type code: str
        :param type: Title type: SHARED, GAME, SERVICE
        :type type: str
        :param notification_single_purchase: WGNC notification data for a single purchase
        :type notification_single_purchase: dict of (str, object)
        :param notification_multi_purpose: WGNC notification data for multiple purchases
        :type notification_multi_purpose: dict of (str, object)
        :param pop: Point of presence, primary data center for this game
        :type pop: str
        :param pgn: Field for compatibility with legacy services
        :type pgn: str
        :param view_entitlement_code: Entitlement required to see the title
        :type view_entitlement_code: str
        :param access_entitlement_code: Entitlement required to access the title
        :type access_entitlement_code: str
        :param comment: Arbitrary string for publisher to add comments or notes about the title
        :type comment: str
        :param webhook_endpoint: URL to game server webhook that will be called after certain events happen
        :type webhook_endpoint: str
        :param ggapi_discovery: GGAPI URL that will be called for discovery
        :type ggapi_discovery: str
        :param ggapi_method: GGAPI URL that will be called for methods
        :type ggapi_method: str
        :param webhook_gzip_accepted: Flag to indicate if the webhook endpoint accept gzipped content
        :type webhook_gzip_accepted: bool
        :param webhook_security_token: Secret token used to authenticate webhook sender
        :type webhook_security_token: str
        :param automatic_registration: Flag to indicate if title want automatic SPA account registration on first login
        or does it manually call after account creation
        :type automatic_registration: bool
        :param internal: Flag to indicate if title is internal
        :type internal: bool
        :param event_schemas: Map of event names to event schemas (json)
        :type event_schemas: dict of (str, object)
        :param document_schemas: Map of document names to document schemas (json)
        :type document_schemas: dict of (str, object)
        :param namespaces: Title namespace
        :type namespaces: list of dict
        :param title_versions: Title versions
        :type title_versions: list of dict
        :param title_permissions: Permissions related to this title
        :type title_permissions: dict of (str, object)
        :param permitting_titles: List of titles that have given this title some kind of permission
        :type permitting_titles: list of str
        :param enforce_prerequisites: Flag to indicate if prerequisites be checked for this title during purchase
        :type enforce_prerequisites: bool
        :param shared_titles: Shared title IDs
        :type shared_titles: list of str
        :param title_group: Title group
        :type title_group: str
        :param title_group_ui: Title group UI
        :type title_group_ui: str
        :param title_id: Title ID
        :type title_id: int
        :param friendly_name: Friendly name of title
        :type friendly_name: str
        :param description: Description of title
        :type description: str
        :param tags: Tags to associate with title
        :type tags: list of str
        :param sentinel_uuid: Sentinel UUID
        :type sentinel_uuid: str
        :param branches: List of branch data
        :type branches: list of dict
        :param default_language: Default language
        :type default_language: str
        :param required_languages: Required language(s)
        :type required_languages: list of str
        :param optional_languages: Optional language(s)
        :type optional_languages: list of str
        :param next_schema_versions: Next schema versions
        :type next_schema_versions: dict of (str, object)
        :param created_at: Date/time when the title was created
        :type created_at: int
        :param updated_at: Date/time when the title was updated
        :type updated_at: int
        :return: Response to Tools V1 Service add title request
        :rtype: Response
        """

        return self.request('tools/api/v1/title').json({
            'id': id,
            'code': code,
            'type': type,
            'notification_single_purpose': notification_single_purchase,
            'notification_multi_purpose': notification_multi_purpose,
            'pop': pop,
            'pgn': pgn,
            'view_entitlement_code': view_entitlement_code,
            'access_entitlement_code': access_entitlement_code,
            'comment': comment,
            'webhook_endpoint': webhook_endpoint,
            'ggapi_discovery': ggapi_discovery,
            'ggapi_method': ggapi_method,
            'webhook_gzip_accepted': webhook_gzip_accepted,
            'webhook_security_token': webhook_security_token,
            'automatic_registration': automatic_registration,
            'internal': internal,
            'event_schemas': event_schemas,
            'document_schemas': document_schemas,
            'namespaces': namespaces,
            'title_versions': title_versions,
            'title_permissions': title_permissions,
            'permitting_titles': permitting_titles,
            'enforce_prerequisites': enforce_prerequisites,
            'shared_titles': shared_titles,
            'title_group': title_group,
            'title_group_ui': title_group_ui,
            'title_id': title_id,
            'friendly_name': friendly_name,
            'description': description,
            'tags': tags,
            'sentinel_uuid': sentinel_uuid,
            'branches': branches,
            'default_language': default_language,
            'required_languages': required_languages,
            'optional_languages': optional_languages,
            'next_schema_versions': next_schema_versions,
            'created_at': created_at,
            'updated_at': updated_at
        }).post()

    def get_title(self, title_code):
        """
        Retrieve a title using Tools V1 Service
        :param title_code: Code of title
        :type title_code: str
        :return: Response to Tools V1 Service get title request
        :rtype: Response
        """

        return self.request('tools/api/v1/title/{}'.format(title_code)).get()

    def update_title(
            self,
            title_code,
            id,
            code,
            type,
            notification_single_purchase,
            notification_multi_purpose,
            pop,
            pgn,
            view_entitlement_code=RequestConstants.Parameters.OPTIONAL,
            access_entitlement_code=RequestConstants.Parameters.OPTIONAL,
            comment=RequestConstants.Parameters.OPTIONAL,
            webhook_endpoint=RequestConstants.Parameters.OPTIONAL,
            ggapi_discovery=RequestConstants.Parameters.OPTIONAL,
            ggapi_method=RequestConstants.Parameters.OPTIONAL,
            webhook_gzip_accepted=RequestConstants.Parameters.OPTIONAL,
            webhook_security_token=RequestConstants.Parameters.OPTIONAL,
            automatic_registration=RequestConstants.Parameters.OPTIONAL,
            internal=RequestConstants.Parameters.OPTIONAL,
            event_schemas=RequestConstants.Parameters.OPTIONAL,
            document_schemas=RequestConstants.Parameters.OPTIONAL,
            namespaces=RequestConstants.Parameters.OPTIONAL,
            title_versions=RequestConstants.Parameters.OPTIONAL,
            title_permissions=RequestConstants.Parameters.OPTIONAL,
            permitting_titles=RequestConstants.Parameters.OPTIONAL,
            enforce_prerequisites=RequestConstants.Parameters.OPTIONAL,
            shared_titles=RequestConstants.Parameters.OPTIONAL,
            title_group=RequestConstants.Parameters.OPTIONAL,
            title_group_ui=RequestConstants.Parameters.OPTIONAL,
            title_id=RequestConstants.Parameters.OPTIONAL,
            friendly_name=RequestConstants.Parameters.OPTIONAL,
            description=RequestConstants.Parameters.OPTIONAL,
            tags=RequestConstants.Parameters.OPTIONAL,
            sentinel_uuid=RequestConstants.Parameters.OPTIONAL,
            branches=RequestConstants.Parameters.OPTIONAL,
            default_language=RequestConstants.Parameters.OPTIONAL,
            required_languages=RequestConstants.Parameters.OPTIONAL,
            optional_languages=RequestConstants.Parameters.OPTIONAL,
            next_schema_versions=RequestConstants.Parameters.OPTIONAL,
            created_at=RequestConstants.Parameters.OPTIONAL,
            updated_at=RequestConstants.Parameters.OPTIONAL
    ):
        """
        Update a specified title using Tools V1 Service
        :param title_code: Code of title
        :type title_code: str
        :param id: ID of title
        :type id: int
        :param code: Unique title code
        :type code: str
        :param type: Title type: SHARED, GAME, SERVICE
        :type type: str
        :param notification_single_purchase: WGNC notification data for a single purchase
        :type notification_single_purchase: dict of (str, object)
        :param notification_multi_purpose: WGNC notification data for multiple purchase
        :type notification_multi_purpose: dict of (str, object)
        :param pop: Point of presence, primary data center for this game
        :type pop: str
        :param pgn: Field for compatibility with legacy services
        :type pgn: str
        :param view_entitlement_code: Entitlement required to see the title
        :type view_entitlement_code: str
        :param access_entitlement_code: Entitlement required to access the title
        :type access_entitlement_code: str
        :param comment: Arbitrary string for publisher to add comments or notes about the title
        :type comment: str
        :param webhook_endpoint: URL to game server webhook that will be called after certain events happen
        :type webhook_endpoint: str
        :param ggapi_discovery: GGAPI URL that will be called for discovery
        :type ggapi_discovery: str
        :param ggapi_method: GGAPI URL that will be called for methods
        :type ggapi_method: str
        :param webhook_gzip_accepted: Flag to indicate if the webhook endpoint accept gzipped content
        :type webhook_gzip_accepted: bool
        :param webhook_security_token: Secret token used to authenticate webhook sender
        :type webhook_security_token: str
        :param automatic_registration: Flag to indicate if title want automatic SPA account registration on first login
        or does it manually call after account creation
        :type automatic_registration: bool
        :param internal: Flag to indicate if title is internal
        :type internal: bool
        :param event_schemas: Map of event names to event schemas (json)
        :type event_schemas: dict of (str, object)
        :param document_schemas: Map of document names to document schemas (json)
        :type document_schemas: dict of (str, object)
        :param namespaces: Title namespace
        :type namespaces: list of dict
        :param title_versions: Title versions
        :type title_versions: list of dict
        :param title_permissions: Permissions related to this title
        :type title_permissions: dict of (str, object)
        :param permitting_titles: List of titles that have given this title some kind of permission
        :type permitting_titles: list of str
        :param enforce_prerequisites: Flag to indicate if prerequisites be checked for this title during purchase
        :type enforce_prerequisites: bool
        :param shared_titles: Shared title IDs
        :type shared_titles: list of str
        :param title_group: Title group
        :type title_group: str
        :param title_group_ui: Title group UI
        :type title_group_ui: str
        :param title_id: Title ID
        :type title_id: int
        :param friendly_name: Friendly name of title
        :type friendly_name: str
        :param description: Description of title
        :type description: str
        :param tags: Tags to associate with title
        :type tags: list of str
        :param sentinel_uuid: Sentinel UUID
        :type sentinel_uuid: str
        :param branches: List of branch data
        :type branches: list of dict
        :param default_language: Default language
        :type default_language: str
        :param required_languages: Required language(s)
        :type required_languages: list of str
        :param optional_languages: Optional language(s)
        :type optional_languages: list of str
        :param next_schema_versions: Next schema versions
        :type next_schema_versions: dict of (str, object)
        :param created_at: Date/time when the title was created
        :type created_at: int
        :param updated_at: Date/time when the title was updated
        :type updated_at: int
        :return: Response to Tools V1 Service update title request
        :rtype: Response
        """

        return self.request('tools/api/v1/title/{0}'.format(title_code)).json({
            'id': id,
            'code': code,
            'type': type,
            'notification_single_purpose': notification_single_purchase,
            'notification_multi_purpose': notification_multi_purpose,
            'pop': pop,
            'pgn': pgn,
            'view_entitlement_code': view_entitlement_code,
            'access_entitlement_code': access_entitlement_code,
            'comment': comment,
            'webhook_endpoint': webhook_endpoint,
            'ggapi_discovery': ggapi_discovery,
            'ggapi_method': ggapi_method,
            'webhook_gzip_accepted': webhook_gzip_accepted,
            'webhook_security_token': webhook_security_token,
            'automatic_registration': automatic_registration,
            'internal': internal,
            'event_schemas': event_schemas,
            'document_schemas': document_schemas,
            'namespaces': namespaces,
            'title_versions': title_versions,
            'title_permissions': title_permissions,
            'permitting_titles': permitting_titles,
            'enforce_prerequisites': enforce_prerequisites,
            'shared_titles': shared_titles,
            'title_group': title_group,
            'title_group_ui': title_group_ui,
            'title_id': title_id,
            'friendly_name': friendly_name,
            'description': description,
            'sentinel_uuid': sentinel_uuid,
            'tags': tags,
            'branches': branches,
            'default_language': default_language,
            'required_languages': required_languages,
            'optional_languages': optional_languages,
            'next_schema_versions': next_schema_versions,
            'created_at': created_at,
            'updated_at': updated_at
        }).post()

    def update_title_json(self, title_code, title_dict_data):
        """
        Update a specified title with json data using Tools V1 Service
        :param title_code: Code of title
        :type title_code: str
        :param title_dict_data: Map of json data to update title
        :type title_dict_data: dict
        :return: Response to Tools V1 Service update title json request
        :rtype: Response
        """
        return self.request('tools/api/v1/title/{}'.format(title_code)).json(
            title_dict_data
        ).post()

    def group_list(self):
        """
        Retrieve a list of title group using Tools V1 Service
        :return: Response to Tools V1 Service group list request
        :rtype: Response
        """

        return self.request('tools/api/v1/title/groups').get()

    def count(self):
        """
        Retrieve an estimate number of records for Title List using Tools V1 Service
        :return: Response to Tools V1 Service count request
        :rtype: Response
        """

        return self.request('tools/api/v1/title/count').get()

    def title_version_list(
            self,
            title_code,
            page_number=1,
            page_size=10,
            order_direction='ASC',
            order_by='NAME',
            name=RequestConstants.Parameters.OPTIONAL,
            id=RequestConstants.Parameters.OPTIONAL,
            active=RequestConstants.Parameters.OPTIONAL,
            view_entitlement_code=RequestConstants.Parameters.OPTIONAL,
            access_entitlement_code=RequestConstants.Parameters.OPTIONAL,
            comment=RequestConstants.Parameters.OPTIONAL,
            search=RequestConstants.Parameters.OPTIONAL
    ):
        """
        Retrieve the list of Title Versions for the specified title using Tools V1 Service
        :param title_code: Code of title
        :type title_code: str
        :param page_number: Page number
        :type page_number: int
        :param page_size: Page size of results
        :type page_size: int
        :param order_direction: Direction (Ascending or Descending) which to sort results
        :type order_direction: str
        :param order_by: Order(NAME, ID, COMMENT, VIEW_ENTITLEMENT_CODE, ACCESS_ENTITLEMENT_CODE) to sort results
        :type order_by: str
        :param name: Name to filter results
        :type name: list of str
        :param id: ID to filter results
        :type id: list of str
        :param active: Flag to filter results by active
        :type active: bool
        :param view_entitlement_code: Filter results by view entitlement code(s)
        :type view_entitlement_code: list of str
        :param access_entitlement_code: Filter results by access entitlement code(s)
        :type access_entitlement_code: list of str
        :param comment: Filter results by comment
        :type comment: list of str
        :param search: User search to filter results
        :type search: list of str
        :return: Response to Tools V1 Service title version list request
        :rtype: Response
        """

        return self.request('tools/api/v1/title/{0}/titleversion'.format(title_code)).params({
            'page_number': page_number,
            'page_size': page_size,
            'order_direction': order_direction,
            'order_by': order_by,
            'name': name,
            'id': id,
            'active': active,
            'view_entitlement_code': view_entitlement_code,
            'access_entitlement_code': access_entitlement_code,
            'comment': comment,
            'search': search
        }).get()

    def update_title_version_list(
            self,
            title_code,
            id,
            name,
            active,
            default,
            comment=RequestConstants.Parameters.OPTIONAL,
            server_api_key=RequestConstants.Parameters.OPTIONAL,
            client_api_key=RequestConstants.Parameters.OPTIONAL,
            view_entitlement_code=RequestConstants.Parameters.OPTIONAL,
            access_entitlement_code=RequestConstants.Parameters.OPTIONAL,
            starting_inventory_code=RequestConstants.Parameters.OPTIONAL,
            emitter_name_suffix=RequestConstants.Parameters.OPTIONAL,
            allowed_client_apis=RequestConstants.Parameters.OPTIONAL,
            dependent_title_versions=RequestConstants.Parameters.OPTIONAL,
            notification_single_purchase=RequestConstants.Parameters.OPTIONAL,
            notification_multi_purchase=RequestConstants.Parameters.OPTIONAL,
            catalogs_activations=RequestConstants.Parameters.OPTIONAL
    ):
        """
        Add a new Title Version to specified title using Tools V1 Service
        :param title_code: Code of title
        :type title_code: str
        :param id: UUID of title
        :type id: str
        :param name: Name of title
        :type name: str
        :param active: Flag to indicate title version active
        :type active: bool
        :param default: Flag to indicate default title version for cross-title and overrides
        :type default: bool
        :param comment: Arbitrary string for publisher to add comments or notes about the title
        :type comment: str
        :param server_api_key: Server API key associated with this title version
        :type server_api_key: str
        :param client_api_key: Client API key associated with this title version
        :type client_api_key: str
        :param view_entitlement_code: Optional additional entitlement required to see this title version
        :type view_entitlement_code:  str
        :param access_entitlement_code: Optional additional entitlement required to access this title version
        :type access_entitlement_code: str
        :param starting_inventory_code: Code for the Product that represents starting inventory for new accounts
        :type starting_inventory_code: str
        :param emitter_name_suffix: Optional suffix on the calling service name for use in the emitter registry
        :type emitter_name_suffix: str
        :param allowed_client_apis: Map of api names to boolean indicating of allowed (true) or blocked (false)
        :type allowed_client_apis: dict of (str, bool)
        :param dependent_title_versions: List of dependent title versions. Activating this title version, activates all
        dependent title versions
        :type dependent_title_versions: list of str
        :param notification_single_purchase: Set of notification info when purchasing a single product
        :type notification_single_purchase: dict of (str, object)
        :param notification_multi_purchase:  Set of notification info when purchasing multiple products
        :type notification_multi_purchase: dict of (str, object)
        :param catalogs_activations: List of catalogs paired with time it becomes active (in descending order by time)
        :type catalogs_activations: list of dict
        :return: Response to Tools V1 Service update title version list request
        :rtype: Response
        """

        return self.request('tools/api/v1/title/{0}/titleversion'.format(title_code)).json({
            'id': id,
            'name': name,
            'active': active,
            'default': default,
            'comment': comment,
            'server_api_key': server_api_key,
            'client_api_key': client_api_key,
            'view_entitlement_code': view_entitlement_code,
            'access_entitlement_code': access_entitlement_code,
            'starting_inventory_code': starting_inventory_code,
            'emitter_name_suffix': emitter_name_suffix,
            'allowed_client_apis': allowed_client_apis,
            'dependent_title_versions': dependent_title_versions,
            'notification_single_purchase': notification_single_purchase,
            'notification_multi_purchase': notification_multi_purchase,
            'catalogs_activations': catalogs_activations
        }).post()

    def branch(
            self,
            title_code,
            show_inactive=RequestConstants.Parameters.OPTIONAL,
            page_number=1,
            page_size=10,
            order_direction='ASC',
            order_by='CODE',
            code=RequestConstants.Parameters.OPTIONAL,
            parent_branch=RequestConstants.Parameters.OPTIONAL,
            description=RequestConstants.Parameters.OPTIONAL,
            search=RequestConstants.Parameters.OPTIONAL,
            friendly_name=RequestConstants.Parameters.OPTIONAL
    ):
        """
        Retrieve the list of Branches for the specified title using Tools V1 Service
        :param title_code: Code of title
        :type title_code: str
        :param show_inactive: Flag to filter result with inactive branch(es)
        :type show_inactive: bool
        :param page_number: Page number
        :type page_number: int
        :param page_size: Page size of results
        :type page_size: int
        :param order_direction: Direction (Ascending or Descending) which to sort results
        :type order_direction: str
        :param order_by: Order(CODE, FRIENDLY_NAME, PARENT_BRANCH, DESCRIPTION) to sort results
        :type order_by: list of str
        :param code: Filter results by branch code specified
        :type code: list of str
        :param parent_branch: Filter results by parent branch code specified
        :type parent_branch: list of str
        :param description: Filter results by description
        :type description: list of str
        :param search: User defined search filter
        :type search: list of str
        :param friendly_name: Filter results by friendly name
        :type friendly_name: list of str
        :return: Response to Tools V1 Service branch request
        :rtype: Response
        """

        return self.request('tools/api/v1/title/{0}/branch'.format(title_code)).params({
            'show_inactive': show_inactive,
            'page_number': page_number,
            'page_size': page_size,
            'order_direction': order_direction,
            'order_by': order_by,
            'code': code,
            'parent_branch': parent_branch,
            'description': description,
            'search': search,
            'friendly_name': friendly_name
        }).get()

    def update_branch(
            self,
            title_code,
            description=RequestConstants.Parameters.OPTIONAL,
            is_overlay=RequestConstants.Parameters.OPTIONAL,
            friendly_name=RequestConstants.Parameters.OPTIONAL,
            parent_branch=RequestConstants.Parameters.OPTIONAL,
            branch_name=RequestConstants.Parameters.OPTIONAL
    ):
        """
        Create a branch for specified title using Tools V1 Service
        :param title_code: Code of title
        :type title_code: str
        :param description: User defined description
        :type description: str
        :param is_overlay: Flag to indicate overlay activation
        :type is_overlay: bool
        :param friendly_name: Friendly name for branch
        :type friendly_name: str
        :param parent_branch: Code of parent branch
        :type parent_branch: str
        :param branch_name: Code of branch to create or update
        :type branch_name: str
        :return: Response to Tools V1 Service update branch request
        :rtype: Response
        """

        return self.request('tools/api/v1/title/{0}/branch'.format(title_code)).json({
            'description': description,
            'is_overlay': is_overlay,
            'friendly_name': friendly_name,
            'parent_branch': parent_branch,
            'branch_name': branch_name
        }).post()

    def update_title_component(
            self,
            title_code,
            component_type,
            title_component
    ):
        """
        Update title component with 'gifts' param
        :param title_code: Code of title
        :type title_code: str
        :param component_type: Component type e.g. 'commerce'
        :type component_type: str
        :param title_component: Body params for title component
        :type title_component: dict
        :return: Response to Tools V1 Service update title component
        :rtype: Response
        """

        return self.request('tools/api/v1/title/{0}/component/{1}'.format(title_code, component_type)).json({
            'gifts': title_component
        }).post()

    def publish(self, title_code):
        """
        Publish updated information about specified title using Tools V1 Service
        :param title_code: Code of title
        :type title_code: str
        :return: Response to Tools V1 Service branch update request
        :rtype: Response
        """

        return self.request('tools/api/v1/title/{0}/publish'.format(title_code)).get()

    def branch_catalog(
            self,
            title_code,
            branch_name,
            page_number=1,
            page_size=10,
            order_direction='ASC',
            order_by='PUB_VERSION'
    ):
        """
        Retrieve list of catalogs from specified branch and title using Tools V1 Service
        :param title_code: Code of title
        :type title_code: str
        :param branch_name: Code of branch
        :type branch_name: str
        :param page_number: Page number
        :type page_number: int
        :param page_size: Page size of results
        :type page_size: int
        :param order_direction: Direction (Ascending or Descending) which to sort results
        :type order_direction: str
        :param order_by: Order(CODE, PARENT_CATALOG, LAST_UPDATED, PUB_VERSION) to sort results
        :type order_by: str
        :return: Response to Tools V1 Service branch catalog request
        :rtype: Response
        """

        return self.request('tools/api/v1/title/{0}/branch/{1}/catalog'.format(title_code, branch_name)).params({
            'page_number': page_number,
            'page_size': page_size,
            'order_direction': order_direction,
            'order_by': order_by
        }).get()

    def branch_name(self, title_code, branch_name):
        """
        Retrieve specified branch from specific title using Tools V1 Service
        :param title_code: Code of title
        :type title_code: str
        :param branch_name: Code of branch
        :type branch_name: str
        :return: Response to Tools V1 Service branch name request
        :rtype: Response
        """

        return self.request('tools/api/v1/title/{0}/branch/{1}'.format(title_code, branch_name)).get()

    def version(self, title_code, tv_id):
        """
        Retrieve specified title version from specific title using Tools V1 Service
        :param title_code: Code of title
        :type title_code: str
        :param tv_id: Title version ID to retrieve
        :type tv_id: str
        :return: Response to Tools V1 Service version request
        :rtype: Response
        """

        return self.request('tools/api/v1/title/{0}/titleversion/{1}'.format(title_code, tv_id)).get()

    def update_version(
            self,
            title_code,
            tv_id,
            id,
            name,
            active,
            default,
            comment=RequestConstants.Parameters.OPTIONAL,
            server_api_key=RequestConstants.Parameters.OPTIONAL,
            client_api_key=RequestConstants.Parameters.OPTIONAL,
            view_entitlement_code=RequestConstants.Parameters.OPTIONAL,
            access_entitlement_code=RequestConstants.Parameters.OPTIONAL,
            starting_inventory_code=RequestConstants.Parameters.OPTIONAL,
            emitter_name_suffix=RequestConstants.Parameters.OPTIONAL,
            dependent_title_versions=RequestConstants.Parameters.OPTIONAL,
            allowed_client_apis=RequestConstants.Parameters.OPTIONAL,
            notification_single_purchase=RequestConstants.Parameters.OPTIONAL,
            notification_multi_purchase=RequestConstants.Parameters.OPTIONAL,
            catalogs_activations=RequestConstants.Parameters.OPTIONAL
    ):
        """
        Add a new title version to a specified title using Tools V1 Service
        :param title_code: Code of title
        :type title_code: str
        :param tv_id: Title version ID to update
        :type tv_id: str
        :param id: UUID for title version
        :type id: str
        :param name: Name of title version
        :type name: str
        :param active: Flag to indicate title version active
        :type active: bool
        :param default: Flag to indicate default title version for cross-title and overrides
        :type default: bool
        :param comment: Arbitrary string for publisher to add comments or notes about the title
        :type comment: str
        :param server_api_key: Server API key associated with this title version
        :type server_api_key: str
        :param client_api_key: Client API key associated with this title version
        :type client_api_key: str
        :param view_entitlement_code: Optional additional entitlement required to see this title version
        :type view_entitlement_code: str
        :param access_entitlement_code: Optional additional entitlement required to access this title version
        :type access_entitlement_code: str
        :param starting_inventory_code: Code for the Product that represents starting inventory for new accounts
        :type starting_inventory_code: str
        :param emitter_name_suffix: List of dependent title versions. Activating this title version, activates all
        dependent title versions
        :type emitter_name_suffix: list of str
        :param dependent_title_versions: Code for the Product that represents starting inventory for new accounts
        :type dependent_title_versions: str
        :param allowed_client_apis: Map of api names to boolean indicating of allowed (true) or blocked (false)
        :type allowed_client_apis: dict of (str, bool)
        :param notification_single_purchase: Set of notification info when purchasing one product
        :type notification_single_purchase: dict of (str, object)
        :param notification_multi_purchase: Set of notification info when purchasing multiple products
        :type notification_multi_purchase: dict of (str, object)
        :param catalogs_activations: List of catalogs paired when title becomes active (in descending order by time)
        :type catalogs_activations: list of dict
        :return: Response to Tools V1 Service title version request
        :rtype: Response
        """

        return self.request('tools/api/v1/title/{0}/titleversion/{1}'.format(title_code, tv_id)).json({
            'id': id,
            'name': name,
            'active': active,
            'default': default,
            'comment': comment,
            'server_api_key': server_api_key,
            'client_api_key': client_api_key,
            'view_entitlement_code': view_entitlement_code,
            'access_entitlement_code': access_entitlement_code,
            'starting_inventory_code': starting_inventory_code,
            'emitter_name_suffix': emitter_name_suffix,
            'dependent_title_versions': dependent_title_versions,
            'allowed_client_apis': allowed_client_apis,
            'notification_single_purchase': notification_single_purchase,
            'notification_multi_purchase': notification_multi_purchase,
            'catalogs_activations': catalogs_activations
        }).post()

    def import_data(
            self,
            id,
            code,
            type,
            notification_single_purchase,
            notification_multi_purpose,
            pop,
            pgn,
            view_entitlement_code=RequestConstants.Parameters.OPTIONAL,
            access_entitlement_code=RequestConstants.Parameters.OPTIONAL,
            comment=RequestConstants.Parameters.OPTIONAL,
            webhook_endpoint=RequestConstants.Parameters.OPTIONAL,
            ggapi_discovery=RequestConstants.Parameters.OPTIONAL,
            ggapi_method=RequestConstants.Parameters.OPTIONAL,
            webhook_gzip_accepted=RequestConstants.Parameters.OPTIONAL,
            webhook_security_token=RequestConstants.Parameters.OPTIONAL,
            automatic_registration=RequestConstants.Parameters.OPTIONAL,
            internal=RequestConstants.Parameters.OPTIONAL,
            external_product_cdn=RequestConstants.Parameters.OPTIONAL,
            enforce_prerequisites=RequestConstants.Parameters.OPTIONAL,
            event_schemas=RequestConstants.Parameters.OPTIONAL,
            document_schemas=RequestConstants.Parameters.OPTIONAL,
            namespaces=RequestConstants.Parameters.OPTIONAL,
            title_versions=RequestConstants.Parameters.OPTIONAL,
            title_permissions=RequestConstants.Parameters.OPTIONAL,
            permitting_titles=RequestConstants.Parameters.OPTIONAL,
            shared_titles=RequestConstants.Parameters.OPTIONAL,
            title_group=RequestConstants.Parameters.OPTIONAL,
            title_group_ui=RequestConstants.Parameters.OPTIONAL,
            title_id=RequestConstants.Parameters.OPTIONAL,
            friendly_name=RequestConstants.Parameters.OPTIONAL,
            description=RequestConstants.Parameters.OPTIONAL,
            sentinel_uuid=RequestConstants.Parameters.OPTIONAL,
            branches=RequestConstants.Parameters.OPTIONAL,
            default_language=RequestConstants.Parameters.OPTIONAL,
            required_languages=RequestConstants.Parameters.OPTIONAL,
            optional_languages=RequestConstants.Parameters.OPTIONAL,
            bulk_operations=RequestConstants.Parameters.OPTIONAL,
            next_schema_versions=RequestConstants.Parameters.OPTIONAL,
            created_at=RequestConstants.Parameters.OPTIONAL,
            updated_at=RequestConstants.Parameters.OPTIONAL
    ):
        """
        Create a new title from import data using Tools V1 Service
        :param id: SPA game ID
        :type id: int
        :param code: Code of title
        :type code: str
        :param type: Title type: SHARED, GAME, SERVICE
        :type type: str
        :param notification_single_purchase: Set of notification info when purchasing one product
        :type notification_single_purchase: dict of (str, object)
        :param notification_multi_purpose: Set of notification info when purchasing multiple products
        :type notification_multi_purpose: dict of (str, object)
        :param pop: Point of presence, primary data center for this game
        :type pop: str
        :param pgn: Field for compatibility with legacy services
        :type pgn: str
        :param view_entitlement_code: Entitlement required to see the title
        :type view_entitlement_code: str
        :param access_entitlement_code: Entitlement required to access the title
        :type access_entitlement_code: str
        :param comment: Arbitrary string for publisher to add comments or notes about the title
        :type comment: str
        :param webhook_endpoint: URL to game server webhook that will be called after certain events happen
        :type webhook_endpoint: str
        :param ggapi_discovery: GGAPI URL that will be called for discovery
        :type ggapi_discovery: str
        :param ggapi_method: GGAPI URL that will be called for methods
        :type ggapi_method: str
        :param webhook_gzip_accepted: Flag to indicate if the webhook endpoint accept gzipped content
        :type webhook_gzip_accepted: bool
        :param webhook_security_token: Secret token used to authenticate webhook sender
        :type webhook_security_token: str
        :param automatic_registration: Flag to indicate if title want automatic SPA account registration on first login
        or does it manually call after account creation
        :type automatic_registration: bool
        :param internal: Flag to indicate if title is internal
        :type internal: bool
        :param external_product_cdn: Flag to indicate if title use the environment's external CDN for product
        inventory calls
        :type external_product_cdn: bool
        :param enforce_prerequisites: Flag to indicate if prerequisites are checked for this title during purchase
        :type enforce_prerequisites: bool
        :param event_schemas: Map of event names to event schemas (json)
        :type event_schemas: dict of (str, object)
        :param document_schemas: Map of document names to document schemas (json)
        :type document_schemas: dict of (str, object)
        :param namespaces: Title namespace
        :type namespaces: list of dict
        :param title_versions: Title versions
        :type title_versions: list of dict
        :param title_permissions: Permissions related to this title
        :type title_permissions: dict of (str, object)
        :param permitting_titles: List of titles that have given this title some kind of permission
        :type permitting_titles: list of str
        :param shared_titles: Shared title IDs
        :type shared_titles: list of str
        :param title_group: Title group
        :type title_group: str
        :param title_group_ui: Title group UI
        :type title_group_ui: str
        :param title_id: Title ID
        :type title_id: int
        :param friendly_name: Friendly name for this title
        :type friendly_name: str
        :param description: Description for this title
        :type description: str
        :param sentinel_uuid: Sentinel UUID
        :type sentinel_uuid: str
        :param branches: List of branch data
        :type branches: list of dict
        :param default_language: Default language
        :type default_language: str
        :param required_languages: Required language(s)
        :type required_languages: list of str
        :param optional_languages: Optional language(s)
        :type optional_languages: list of str
        :param bulk_operations: Bulk operations
        :type bulk_operations: list of str
        :param next_schema_versions: Next schema versions
        :type next_schema_versions: dict of (str, object)
        :param created_at: Title creation time
        :type created_at: int
        :param updated_at: Title update time
        :type updated_at: int
        :return: Response to Tools V1 Service import request
        :rtype: Response
        """

        return self.request('tools/api/v1/title/import').json({
            'id': id,
            'code': code,
            'type': type,
            'notification_single_purpose': notification_single_purchase,
            'notification_multi_purpose': notification_multi_purpose,
            'pop': pop,
            'pgn': pgn,
            'view_entitlement_code': view_entitlement_code,
            'access_entitlement_code': access_entitlement_code,
            'comment': comment,
            'webhook_endpoint': webhook_endpoint,
            'ggapi_discovery': ggapi_discovery,
            'ggapi_method': ggapi_method,
            'webhook_gzip_accepted': webhook_gzip_accepted,
            'webhook_security_token': webhook_security_token,
            'automatic_registration': automatic_registration,
            'internal': internal,
            'external_product_cdn': external_product_cdn,
            'enforce_prerequisites': enforce_prerequisites,
            'event_schemas': event_schemas,
            'document_schemas': document_schemas,
            'namespaces': namespaces,
            'title_versions': title_versions,
            'title_permissions': title_permissions,
            'permitting_titles': permitting_titles,
            'shared_titles': shared_titles,
            'title_group': title_group,
            'title_group_ui': title_group_ui,
            'title_id': title_id,
            'friendly_name': friendly_name,
            'description': description,
            'sentinel_uuid': sentinel_uuid,
            'branches': branches,
            'default_language': default_language,
            'required_languages': required_languages,
            'optional_languages': optional_languages,
            'bulk_operations': bulk_operations,
            'next_schema_versions': next_schema_versions,
            'created_at': created_at,
            'updated_at': updated_at
        }).post()

    def abandon_branch(self, title_code, branch_name):
        """
        Abandon specified branch from specific title using Tools V1 Service
        :param title_code: Code of title
        :type title_code: str
        :param branch_name: Code of branch
        :type branch_name: str
        :return: Response to Tools V1 Service abandon branch request
        :rtype: Response
        """

        return self.request('tools/api/v1/title/{0}/branch/{1}/abandon'.format(title_code, branch_name)).headers({
            'Content-Type': RequestConstants.ContentTypes.JSON,
            'Accept': RequestConstants.ContentTypes.JSON,
        }).post()

    def update_permissions(self, title_code, permission_changes):
        """
        Update permissions contained in specified title using Tools V1 Service
        :param title_code: Code of title
        :type title_code: str
        :param permission_changes: List of permissions to modify
        :type permission_changes: list of dict
        :return: Response to Tools V1 Service update permissions request
        :rtype: Response
        """

        return self.request('tools/api/v1/title/{0}/permissions'.format(
            title_code)
        ).headers({
            'Content-Type': RequestConstants.ContentTypes.JSON,
            'Accept': RequestConstants.ContentTypes.JSON,
        }).json({
            "permission_changes": permission_changes
        }).put()


class ToolsExtension(Gateway):

    def get_extension(self, extension_code):
        """
        Retrieve extension data using Tools V1 Service
        :param extension_code: Code of extension
        :type extension_code: str
        :return: Response to Tools V1 Service get extension request
        :rtype: Response
        """

        return self.request('tools/api/v1/ext/registry/{0}'.format(extension_code)).get()

    def update_extension(
            self,
            extension_code,
            code=RequestConstants.Parameters.OPTIONAL,
            friendly_name=RequestConstants.Parameters.OPTIONAL,
            api_base=RequestConstants.Parameters.OPTIONAL,
            name=RequestConstants.Parameters.OPTIONAL,
            location=RequestConstants.Parameters.OPTIONAL,
            owner=RequestConstants.Parameters.OPTIONAL):
        """
        Update the specified extension data using Tools V1 Service
        :param extension_code: Code of extension to update
        :type extension_code: str
        :param code: Code of extension
        :type code: str
        :param friendly_name: Friendly name of extension
        :type friendly_name: str
        :param api_base: Base API
        :type api_base: str
        :param name: Name of extension
        :type name: dict of (str, object)
        :param location: Location of extension
        :type location: str
        :param owner: Owner of extension
        :type owner: str
        :return: Response to Tools V1 Service update extension request
        :rtype: Response
        """

        return self.request(
            'tools/api/v1/ext/registry/{0}'.format(extension_code)
        ).json({
            'code': code,
            'friendly_name': friendly_name,
            'api_base': api_base,
            'name': name,
            'location': location,
            'owner': owner
        }).post()

    def get_extension_list(self):
        """
        Retrieve a list of registered extensions using Tools V1 Service
        :return: Response to Tools V1 Service get extension list request
        :rtype: Response
        """

        return self.request('tools/api/v1/ext/registry').get()

    def register_extension(
            self,
            code,
            api_base,
            friendly_name=RequestConstants.Parameters.OPTIONAL,
            location=RequestConstants.Parameters.OPTIONAL,
            owner=RequestConstants.Parameters.OPTIONAL,
            name=RequestConstants.Parameters.OPTIONAL
    ):
        """
        Register new Extension data using Tools V1 Service
        :param code: Code of extension to register
        :type code: str
        :param api_base: Base API
        :type api_base: str
        :param friendly_name: Friendly name to designate this extension
        :type friendly_name: str
        :param location: Location of extension
        :type location: str
        :param owner: Owner of extension
        :type owner: str
        :param name: Name of extension
        :type name: dict of (str, object)
        :return: Response to Tools V1 Service register extension request
        :rtype: Response
        """
        return self.request('tools/api/v1/ext/registry').json({
            "code": code,
            "api_base": api_base,
            "friendly_name": friendly_name,
            "location": location,
            "owner": owner,
            "name": name
        }).post()

    def unregister_extension(self, ext_code):
        """
        Delete an extension from registry using Tools V1 Service
        :param ext_code: Code of extension
        :type ext_code: str
        :return: Response to Tools V1 Service unregister extension request
        :rtype: Response
        """
        return self.request('tools/api/v1/ext/registry/{}'.format(ext_code)).delete()

    def call_get_extension(self, extension_code):
        """
        Tools V1 Service proxy to extension GET API
        :param extension_code: Code of extension
        :type extension_code: str
        :return: Response to Tools V1 Service call get extension proxy request
        :rtype: Response
        """

        return self.request('tools/api/v1/ext/api/{0}'.format(extension_code)).get()


class ToolsOperations(Gateway):

    def get_audit_log(
            self,
            page_key=RequestConstants.Parameters.OPTIONAL,
            limit=10,
            order_direction='DESC',
            title_code=RequestConstants.Parameters.OPTIONAL,
            object_type=RequestConstants.Parameters.OPTIONAL,
            entity_code=RequestConstants.Parameters.OPTIONAL,
            audit_log_id=RequestConstants.Parameters.OPTIONAL,
            branch_name=RequestConstants.Parameters.OPTIONAL,
            pub_version=RequestConstants.Parameters.OPTIONAL,
            working_version=RequestConstants.Parameters.OPTIONAL,
            action_type=RequestConstants.Parameters.OPTIONAL,
            date_time=RequestConstants.Parameters.OPTIONAL,
            username=RequestConstants.Parameters.OPTIONAL,
            no_data=True,
            page_dir='NEXT'
    ):
        """
        Retrieves logging for searched parameters such as title_code or object_type
        :param page_key: The record ID offset used to start the
        :type page_key: long
        :param limit:
        :type limit: int
        :param order_direction: Indicate order direction which results are displayed, DESC(descending) is default
        :type order_direction: str
        :param title_code: Search filter by title code
        :type title_code: list of str
        :param object_type: Search filter by object types: TITLE, BRANCH, TITLE_VERSION, CATALOG, PRODUCT, CURRENCY,
        ENTITLEMENT, STOREFRONT, OVERRIDE, PROMOTION
        :type object_type: list of str
        :param entity_code: Search filter by entity code, e.g. test_override
        :type entity_code: list of str
        :param audit_log_id: Search filter by audit log id
        :type audit_log_id: list of str
        :param branch_name: Search filter by branch name, e.g. MAIN
        :type branch_name: list of str
        :param pub_version: Search filter by published catalog version
        :type pub_version: list of str
        :param working_version: Search filter by working catalog version
        :type working_version: list of str
        :param action_type: Search filter by action types: UPDATE, INSERT, DELETE, PUBLISH
        :type action_type: list of str
        :param date_time: Search filter by epoch date time
        :type date_time: list of str
        :param username: Search filter by username, e.g. admin
        :type username: list of str
        :param no_data: Boolean flag to exclude old_data and new_data from the result
        :type no_data: bool
        :param page_dir: Page direction: PREV or NEXT
        :type page_dir: str
        :return: Response to audit log search request
        :rtype: Response
        """

        return self.request('tools/api/v1/auditLog/entity').params({
            'page_key': page_key,
            'limit': limit,
            'order_direction': order_direction,
            'title_code': title_code,
            'object_type': object_type,
            'entity_code': entity_code,
            'audit_log_id': audit_log_id,
            'branch_name': branch_name,
            'pub_version': pub_version,
            'working_version': working_version,
            'action_type': action_type,
            'date_time': date_time,
            'username': username,
            'no_data': no_data,
            'page_dir': page_dir
        }).get()


class ToolsWorkingCatalog(Gateway):

    def get_catalog(self, title_code, branch_name):
        """
        Retrieve the working catalog for specified title and branch using Tools V1 Service
        :param title_code: Code of title
        :type title_code: str
        :param branch_name: Code of branch
        :type branch_name: str
        :return: Response to Tools V1 Service get catalog request
        :rtype: Response
        """

        return self.request(
            'tools/api/v1/title/{0}/branch/{1}/catalog/working'.format(title_code, branch_name)
        ).set_timeout(60).get()

    def revert(self, title_code, branch_name, version, force=True):
        """
        Revert the working catalog to a specific version using Tools V1 Service
        :param title_code: Code of title
        :type title_code: str
        :param branch_name: Code of branch
        :type branch_name: str
        :param version: Catalog version number
        :type version: str
        :param force: Flag to indicate a force reversion
        :type force: bool
        :return: Response to Tools V1 Service revert request
        :rtype: Response
        """

        return self.request(
            'tools/api/v1/title/{0}/branch/{1}/catalog/{2}/makeworking'.format(title_code, branch_name, version)
        ).json({
            'force': force
        }).post()

    def get_version(self, title_code, branch_name, publish_version):
        """
        Retrieve working version of catalog for specified title and branch using Tools V1 Service
        :param title_code: Code of title
        :type title_code: str
        :param branch_name: Code of branch
        :type branch_name: str
        :param publish_version: Version of published catalog
        :type publish_version: int
        :return: Response to Tools V1 Service get version request
        :rtype: Response
        """

        return self.request(
            'tools/api/v1/title/{0}/branch/{1}/catalog/{2}'.format(title_code, branch_name, publish_version)
        ).get()

    def create_branch(self, title_code, branch_name, new_branch_name, overlay):
        """
        Create a branch for specified title by forking an existing branch using Tools V1 Service
        :param title_code: Code of title
        :type title_code: str
        :param branch_name: Code of branch
        :type branch_name: str
        :param new_branch_name: Code of new branch to create
        :type new_branch_name: str
        :param overlay: Flag to indicate whether overlay will be used
        :type overlay: bool
        :return: Response to Tools V1 Service create branch request
        :rtype: Response
        """

        return self.request(
            'tools/api/v1/title/{0}/branch/{1}/catalog/createbranch'.format(title_code, branch_name)
        ).json({
            'new_branch_name': new_branch_name,
            'overlay': overlay
        }).post()

    def merge_branches(self, title_code, branch_name, version, target_branch, on_conflict, conflict_list,
                       delete_source_on_success):
        """
        Merge branches using Tools V1 Service
        :param title_code: Code of title
        :type title_code: str
        :param branch_name: Code of branch
        :type branch_name: str
        :param version: Published catalog version number
        :type version: str
        :param target_branch: Target branch to merge
        :type target_branch: str
        :param on_conflict: Merge conflict solution
        :type on_conflict: str
        :param conflict_list: Conflict list of merge
        :type conflict_list: dict of (str, object)
        :param delete_source_on_success: Flag to indicate deletion of source catalog when merge is successful
        :type delete_source_on_success: bool
        :return: Response to Tools V1 Service merge branches request
        :rtype: Response
        """

        return self.request(
            'tools/api/v1/title/{0}/branch/{1}/catalog/{2}/mergeinto/{3}'.format(title_code, branch_name, version,
                                                                                 target_branch)
        ).json({
            'on_conflict': on_conflict,
            'conflict_list': conflict_list,
            'delete_source_on_success': delete_source_on_success
        }).post()

    def import_catalog(self, title_code, branch_name, filename, disable_missing=False):
        """
        Attempts to import catalog to active title and branch using Tools V1 Service
        :param title_code: Code of title
        :type title_code: str
        :param branch_name: Code of branch
        :type branch_name: str
        :param filename: Name of file to import
        :type filename: str
        :param disable_missing: Flag to indicate if all the existing entities that aren't present in the file will be
        set as inactive
        :type disable_missing: bool
        :return: Response to Tools V1 Service import catalog request
        :rtype: Response
        """

        return self.request('tools/api/v1/title/{0}/branch/{1}/import'.format(
            title_code,
            branch_name)
        ).headers({
            'Accept': RequestConstants.ContentTypes.JSON,
        }).params({
            "disable_missing": disable_missing
        }).json({
            "type": "formData"
        }).set_timeout(60).post(RequestConstants.ContentTypes.JSON, file=open(filename, 'rb'))

    def import_glossary(
            self,
            title_code,
            branch_name,
            version=RequestConstants.Parameters.OPTIONAL,
            platform_game_name=RequestConstants.Parameters.OPTIONAL,
            nation=RequestConstants.Parameters.OPTIONAL,
            tag=RequestConstants.Parameters.OPTIONAL,
            lang=RequestConstants.Parameters.OPTIONAL,
            item_type=RequestConstants.Parameters.OPTIONAL,
            related_to=RequestConstants.Parameters.OPTIONAL,
            glossary_entitlement_type=RequestConstants.Parameters.OPTIONAL
    ):
        """
        Import glossary service entities to the active branch working catalog entitlements using Tools V1 Service
        :param title_code: Code of title
        :type title_code: str
        :param branch_name: Code of branch
        :type branch_name: str
        :param version: Release version
        :type version: str
        :param platform_game_name: Game code
        :type platform_game_name: str
        :param nation: Nation filter for both items/vehicles
        :type nation: str
        :param tag: Tag filter for items/vehicles/emblems
        :type tag: str
        :param lang: Language filter for items/vehicles/crews/emblems
        :type lang: str
        :param item_type: Item type filter for items
        :type item_type: str
        :param related_to: Related to filter for items
        :type related_to: str
        :param glossary_entitlement_type: Glossary entity type to import
        :type glossary_entitlement_type: str
        :return: Response to Tools V1 Service import glossary request
        :rtype: Response
        """

        return self.request(
            'tools/api/v1/title/{0}/branch/{1}/catalog/working/entitlement/importglossary'.format(title_code,
                                                                                                  branch_name)
        ).params({
            'version': version,
            'platform_game_name': platform_game_name,
            'nation': nation,
            'tag': tag,
            'lang': lang,
            'item_type': item_type,
            'related_to': related_to,
            'glossary_entity_type': glossary_entitlement_type
        }).get()


class ToolsPublishCatalog(Gateway):

    def activate_catalog(self, title_code, version_id, catalog_code, activate_at=RequestConstants.Parameters.OPTIONAL):
        """
        Activate the catalog version using Tools V1 Service
        :param title_code: Code of title
        :type title_code: str
        :param version_id: Version ID
        :type version_id: str
        :param catalog_code: Code of catalog to activate
        :type catalog_code: str
        :param activate_at: Activation time of catalog
        :type activate_at: int
        :return: Response to Tools V1 Service activate catalog request
        :rtype: Response
        """

        return self.request(
            'tools/api/v1/title/{0}/version/{1}/activatecatalog'.format(title_code, version_id)
        ).json({
            'catalog_code': catalog_code,
            'activate_at': activate_at
        }).post()

    def get_published_version(self, title_code, branch_name, pub_version):
        """
        Retrieve a published version of specified catalog and branch using Tools V1 Service
        :param title_code: Code of title
        :type title_code: str
        :param branch_name: Code of branch
        :type branch_name: str
        :param pub_version: Publish version of catalog
        :type pub_version: int
        :return: Response to Tools V1 Service get published version request
        :rtype: Response
        """

        return self.request(
            'tools/api/v1/title/{0}/branch/{1}/catalog/{2}/published'.format(title_code, branch_name, pub_version)
        ).get()

    def validate_working_catalog(self, title_code, branch_name, activate_at=RequestConstants.Parameters.OPTIONAL):
        """
        Validate working catalog for specified title and branch using Tools V1 Service
        :param title_code: Code of title
        :type title_code: str
        :param branch_name: Code of branch
        :type branch_name: str
        :param activate_at: Activation time of catalog
        :type activate_at: long
        :return: Response to Tools V1 Service validate working catalog
        :rtype: Response
        """

        return self.request(
            'tools/api/v1/title/{0}/branch/{1}/validate'.format(title_code, branch_name)
        ).json({
            'activate_at': activate_at
        }).post()

    def publish_working_catalog(
            self,
            title_code,
            branch_name,
            version_ids=RequestConstants.Parameters.OPTIONAL,
            activate_at=RequestConstants.Parameters.OPTIONAL
    ):
        """
        Publish working catalog for specified title and branch using Tools V1 Service
        :param title_code: Code of title
        :type title_code: str
        :param branch_name: Code of branch
        :type branch_name: str
        :param version_ids: List of version IDs
        :type version_ids: list of str
        :param activate_at: Activation time of catalog
        :type activate_at: int
        :return: Response to Tools V1 Service publish working catalog request
        :rtype: Response
        """

        return self.request(
            'tools/api/v1/title/{0}/branch/{1}/publish'.format(title_code, branch_name)
        ).headers({
            'Content-Type': RequestConstants.ContentTypes.JSON,
            'Accept': RequestConstants.ContentTypes.JSON,
        }).json({
            "version_ids": version_ids,
            "activate_at": activate_at
        }).post()


class ToolsPublishedCatalog(Gateway):

    def get_published_entity(self, title_code, branch_name, pub_version, entity_type, entity_code):
        """
        Retrieve a specific of entity from the published version of current catalog using Tools V1 Service

        This method can be applied to -- among other things -- entitlements, products, and storefronts, since their
        endpoints are virtually identical. The type of the entity to be updated is entity_type.

        :param title_code: Code of title
        :type title_code: str
        :param branch_name: Code of branch
        :type branch_name: str
        :param pub_version: Published catalog version number
        :type pub_version: int
        :param entity_type: Type of entity [CURRENCY, ENTITLEMENT, PRODUCT, STOREFRONT, OVERRIDE, PROMOTION]
        :type entity_type: str
        :param entity_code: Code of entity
        :type entity_code: str
        :return: Response to Tools V1 Service get published entity request
        :rtype: Response
        """

        return self.request(
            'tools/api/v1/title/{0}/branch/{1}/pubversion/{2}/{3}/{4}'.format(
                title_code, branch_name, pub_version, entity_type, entity_code)
        ).get()

    def get_published_catalog_products(
            self,
            title_code,
            branch_name,
            pub_version,
            page_number=1,
            page_size=10,
            order_direction='ASC',
            order_by='CODE',
            active=True,
            code=RequestConstants.Parameters.OPTIONAL,
            friendly_name=RequestConstants.Parameters.OPTIONAL,
            search=RequestConstants.Parameters.OPTIONAL,
            code_exact=RequestConstants.Parameters.OPTIONAL,
            friendly_name_exact=RequestConstants.Parameters.OPTIONAL,
            status=RequestConstants.Parameters.OPTIONAL,
            status_exact=RequestConstants.Parameters.OPTIONAL,
            virt_currency_min=RequestConstants.Parameters.OPTIONAL,
            virt_currency_max=RequestConstants.Parameters.OPTIONAL,
            base_price_min=RequestConstants.Parameters.OPTIONAL,
            base_price_max=RequestConstants.Parameters.OPTIONAL,
            entitlement_code=RequestConstants.Parameters.OPTIONAL,
            entitlement_code_exact=RequestConstants.Parameters.OPTIONAL,
            currency_code=RequestConstants.Parameters.OPTIONAL,
            currency_code_exact=RequestConstants.Parameters.OPTIONAL,
            spa_access_game_code=RequestConstants.Parameters.OPTIONAL,
            spa_access_game_code_exact=RequestConstants.Parameters.OPTIONAL,
            bonus_set_codeset_id=RequestConstants.Parameters.OPTIONAL,
            available_in=RequestConstants.Parameters.OPTIONAL,
            search_exact=RequestConstants.Parameters.OPTIONAL,
            category=RequestConstants.Parameters.OPTIONAL,
            category_exact=RequestConstants.Parameters.OPTIONAL
    ):
        """
        Retrieve products from the published version of current catalog using Tools V1 Service

        :param title_code: Code of title
        :type title_code: str
        :param branch_name: Code of branch
        :type branch_name: str
        :param pub_version: Published catalog version number
        :type pub_version: int
        :param page_number: Number of pages per query to display
        :type page_number: int
        :param page_size: Page size of query to display, 10 is default
        :type page_size: int
        :param order_direction: Order direction of query results, ASC is default
        :type order_direction: str
        :param code: Code of product to filter
        :type code: list of str
        :param friendly_name: Friendly name filter
        :type friendly_name: list of str
        :param search: User search
        :type search: list of str
        :param code_exact: Turn on or off exact search for product queries
        :type code_exact: bool
        :param friendly_name_exact: Turn on or off exact search for friendly name queries
        :type friendly_name_exact: bool
        :param status: Status filter
        :type status: list of str
        :param status_exact: Turn on or off exact search for status queries
        :type status_exact: bool
        :param virt_currency_min: Virtual currency minimum filter
        :type virt_currency_min: int
        :param virt_currency_max: Virtual currency maximum filter
        :type virt_currency_max: int
        :param base_price_min: Base price minimum filter
        :type base_price_min: int
        :param base_price_max: Base price maximum filter
        :type base_price_max: int
        :param entitlement_code:
        :type entitlement_code: list of str
        :param entitlement_code_exact: Turn on or off exact search for entitlement queries
        :type entitlement_code_exact: bool
        :param currency_code: Currency code filter
        :type currency_code: list of str
        :param currency_code_exact: Turn on or off exact search for currency queries
        :type currency_code_exact: bool
        :param spa_access_game_code: Spa access game code filter
        :type spa_access_game_code: list of str
        :param spa_access_game_code_exact: Turn on or off exact search for spa access game code queries
        :type spa_access_game_code_exact: bool
        :param bonus_set_codeset_id: Bonus codes filter
        :type bonus_set_codeset_id: list of int
        :param available_in: Country availability filter
        :type available_in: list of str
        :param search_exact: Turn on or off exact search type
        :type search_exact: bool
        :param category: Code of category
        :type category: str
        :param category_exact: Turn on or off exact search for category
        :type category_exact: bool
        :param order_by: Ordering options [CODE, FRIENDLY_NAME, STATUS, CREATED_AT], CODE is default
        :type order_by: str
        :param active: Turn on or off searching only active products
        :type active: bool
        :return: Response to Tools V1 Service get published products request
        :rtype: Response
        """

        return self.request('tools/api/v1/title/{0}/branch/{1}/pubversion/{2}/products'.format(
            title_code, branch_name, pub_version)
        ).params({
            'page_number': page_number,
            'page_size': page_size,
            'order_direction': order_direction,
            'code': code,
            'friendly_name': friendly_name,
            'search': search,
            'code_exact': code_exact,
            'friendly_name_exact': friendly_name_exact,
            'status': status,
            'status_exact': status_exact,
            'virt_currency_min': virt_currency_min,
            'virt_currency_max': virt_currency_max,
            'base_price_min': base_price_min,
            'base_price_max': base_price_max,
            'entitlement_code': entitlement_code,
            'entitlement_code_exact': entitlement_code_exact,
            'currency_code': currency_code,
            'currency_code_exact': currency_code_exact,
            'spa_access_game_code': spa_access_game_code,
            'spa_access_game_code_exact': spa_access_game_code_exact,
            'bonus_set_codeset_id': bonus_set_codeset_id,
            'available_in': available_in,
            'search_exact': search_exact,
            'category': category,
            'category_exact': category_exact,
            'order_by': order_by,
            'active': active
        }).get()

    def get_published_catalog_storefronts(
            self,
            title_code,
            branch_name,
            pub_version,
            page_number=1,
            page_size=10,
            order_direction='ASC',
            active=True,
            code=RequestConstants.Parameters.OPTIONAL,
            friendly_name=RequestConstants.Parameters.OPTIONAL,
            search=RequestConstants.Parameters.OPTIONAL,
            code_exact=RequestConstants.Parameters.OPTIONAL,
            friendly_name_exact=RequestConstants.Parameters.OPTIONAL,
            product_code=RequestConstants.Parameters.OPTIONAL,
            product_code_exact=RequestConstants.Parameters.OPTIONAL,
            search_exact=RequestConstants.Parameters.OPTIONAL,
            category=RequestConstants.Parameters.OPTIONAL,
            category_exact=RequestConstants.Parameters.OPTIONAL,
            order_by='CODE'
    ):
        """
        Retrieve storefronts from the published version of current catalog using Tools V1 Service

        :param title_code: Code of title
        :type title_code: str
        :param branch_name: Code of branch
        :type branch_name: str
        :param pub_version: Published catalog version number
        :type pub_version: int
        :param page_number: Number of pages per query to display
        :type page_number: int
        :param page_size: Page size of query to display, 10 is default
        :type page_size: int
        :param order_direction: Order direction of query results, ASC is default
        :type order_direction: str
        :param code: Code of product to filter
        :type code: list of str
        :param friendly_name: Friendly name filter
        :type friendly_name: list of str
        :param search: User search
        :type search: list of str
        :param code_exact: Turn on or off exact search for product queries
        :type code_exact: bool
        :param friendly_name_exact: Turn on or off exact search for friendly name queries
        :type friendly_name_exact: bool
        :param product_code: Status filter
        :type product_code: list of str
        :param product_code_exact: Turn on or off exact search for status queries
        :type product_code_exact: bool
        :param search_exact: Turn on or off exact search type
        :type search_exact: bool
        :param category: Code of category
        :type category: str
        :param category_exact: Turn on or off exact search for category
        :type category_exact: bool
        :param order_by: Ordering options [CODE, FRIENDLY_NAME, STATUS, CREATED_AT], CODE is default
        :type order_by: str
        :param active: Turn on or off searching only active storefronts
        :type active: bool
        :return: Response to Tools V1 Service get published storefronts request
        :rtype: Response
        """

        return self.request('tools/api/v1/title/{0}/branch/{1}/pubversion/{2}/storefronts'.format(
            title_code, branch_name, pub_version)
        ).params({
            'page_number': page_number,
            'page_size': page_size,
            'order_direction': order_direction,
            'code': code,
            'friendly_name': friendly_name,
            'search': search,
            'code_exact': code_exact,
            'friendly_name_exact': friendly_name_exact,
            'product_code': product_code,
            'product_code_exact': product_code_exact,
            'search_exact': search_exact,
            'category': category,
            'category_exact': category_exact,
            'order_by': order_by,
            'active': active
        }).get()


class ToolsWorkingCatalogEntities(Gateway):

    def get_entity_list(self, title_code, branch_name, entity_type):
        """
        Retrieve a list of entities from the active branch of working catalog using Tools V1 Service

        This method can be applied to -- among other things -- entitlements, products, and storefronts, since their
        endpoints are virtually identical. The type of the entity to be updated is entity_type
        :param title_code: Code of title
        :type title_code: str
        :param branch_name: Code of branch
        :type branch_name: str
        :param entity_type: Type of entity to retrieve(currency, entitlement, product, override, promotion, storefront)
        :type entity_type: str
        :return: Response to Tools V1 Service get entity list request
        :rtype: Response
        """

        return self.request(
            'tools/api/v1/title/{0}/branch/{1}/catalog/working/{2}'.format(title_code, branch_name, entity_type)
        ).get()

    def get_working_catalog_product_list(
            self,
            title_code,
            branch_name,
            page_number=1,
            page_size=10,
            order_direction='ASC',
            active=True,
            code=RequestConstants.Parameters.OPTIONAL,
            friendly_name=RequestConstants.Parameters.OPTIONAL,
            search=RequestConstants.Parameters.OPTIONAL,
            code_exact=RequestConstants.Parameters.OPTIONAL,
            friendly_name_exact=RequestConstants.Parameters.OPTIONAL,
            status=RequestConstants.Parameters.OPTIONAL,
            status_exact=RequestConstants.Parameters.OPTIONAL,
            virt_currency_min=RequestConstants.Parameters.OPTIONAL,
            virt_currency_max=RequestConstants.Parameters.OPTIONAL,
            base_price_min=RequestConstants.Parameters.OPTIONAL,
            base_price_max=RequestConstants.Parameters.OPTIONAL,
            entitlement_code=RequestConstants.Parameters.OPTIONAL,
            entitlement_code_exact=RequestConstants.Parameters.OPTIONAL,
            currency_code=RequestConstants.Parameters.OPTIONAL,
            currency_code_exact=RequestConstants.Parameters.OPTIONAL,
            spa_access_game_code=RequestConstants.Parameters.OPTIONAL,
            spa_access_game_code_exact=RequestConstants.Parameters.OPTIONAL,
            bonus_set_codeset_id=RequestConstants.Parameters.OPTIONAL,
            available_in=RequestConstants.Parameters.OPTIONAL,
            search_exact=RequestConstants.Parameters.OPTIONAL,
            category=RequestConstants.Parameters.OPTIONAL,
            category_exact=RequestConstants.Parameters.OPTIONAL,
            order_by=RequestConstants.Parameters.OPTIONAL
    ):
        """
        Retrieve list of products from the working catalog using Tools V1 Service

        :param title_code: Code of title
        :type title_code: str
        :param branch_name: Code of branch
        :type branch_name: str
        :param page_number: Number of pages per query to display
        :type page_number: int
        :param page_size: Page size of query to display, 10 is default
        :type page_size: int
        :param order_direction: Order direction of query results, ASC is default
        :type order_direction: str
        :param code: Code of product to filter
        :type code: list of str
        :param friendly_name: Friendly name filter
        :type friendly_name: list of str
        :param search: User search
        :type search: list of str
        :param code_exact: Turn on or off exact search for product queries
        :type code_exact: bool
        :param friendly_name_exact: Turn on or off exact search for friendly name queries
        :type friendly_name_exact: bool
        :param status: Status filter
        :type status: list of str
        :param status_exact: Turn on or off exact search for status queries
        :type status_exact: bool
        :param virt_currency_min: Virtual currency minimum filter
        :type virt_currency_min: int
        :param virt_currency_max: Virtual currency maximum filter
        :type virt_currency_max: int
        :param base_price_min: Base price minimum filter
        :type base_price_min: int
        :param base_price_max: Base price maximum filter
        :type base_price_max: int
        :param entitlement_code:
        :type entitlement_code: list of str
        :param entitlement_code_exact: Turn on or off exact search for entitlement queries
        :type entitlement_code_exact: bool
        :param currency_code: Currency code filter
        :type currency_code: list of str
        :param currency_code_exact: Turn on or off exact search for currency queries
        :type currency_code_exact: bool
        :param spa_access_game_code: Spa access game code filter
        :type spa_access_game_code: list of str
        :param spa_access_game_code_exact: Turn on or off exact search for spa access game code queries
        :type spa_access_game_code_exact: bool
        :param bonus_set_codeset_id: Bonus codes filter
        :type bonus_set_codeset_id: list of int
        :param available_in: Country availability filter
        :type available_in: list of str
        :param search_exact: Turn on or off exact search type
        :type search_exact: bool
        :param category: Code of category
        :type category: str
        :param category_exact: Turn on or off exact search for category
        :type category_exact: bool
        :param order_by: Ordering options [CODE, FRIENDLY_NAME, STATUS, CREATED_AT]
        :type order_by: str
        :param active: Turn on or off searching only active products
        :type active: bool
        :return: Response to Tools V1 Service get working catalog list of products request
        :rtype: Response
        """

        return self.request('tools/api/v1/title/{0}/branch/{1}/catalog/working/product'.format(
            title_code, branch_name)
        ).params({
            'page_number': page_number,
            'page_size': page_size,
            'order_direction': order_direction,
            'code': code,
            'friendly_name': friendly_name,
            'search': search,
            'code_exact': code_exact,
            'friendly_name_exact': friendly_name_exact,
            'status': status,
            'status_exact': status_exact,
            'virt_currency_min': virt_currency_min,
            'virt_currency_max': virt_currency_max,
            'base_price_min': base_price_min,
            'base_price_max': base_price_max,
            'entitlement_code': entitlement_code,
            'entitlement_code_exact': entitlement_code_exact,
            'currency_code': currency_code,
            'currency_code_exact': currency_code_exact,
            'spa_access_game_code': spa_access_game_code,
            'spa_access_game_code_exact': spa_access_game_code_exact,
            'bonus_set_codeset_id': bonus_set_codeset_id,
            'available_in': available_in,
            'search_exact': search_exact,
            'category': category,
            'category_exact': category_exact,
            'order_by': order_by,
            'active': active
        }).get()

    def get_working_catalog_storefront_list(
            self,
            title_code,
            branch_name,
            page_number=1,
            page_size=10,
            order_direction='ASC',
            active=True,
            code=RequestConstants.Parameters.OPTIONAL,
            friendly_name=RequestConstants.Parameters.OPTIONAL,
            search=RequestConstants.Parameters.OPTIONAL,
            code_exact=RequestConstants.Parameters.OPTIONAL,
            friendly_name_exact=RequestConstants.Parameters.OPTIONAL,
            product_code=RequestConstants.Parameters.OPTIONAL,
            product_code_exact=RequestConstants.Parameters.OPTIONAL,
            search_exact=RequestConstants.Parameters.OPTIONAL,
            category=RequestConstants.Parameters.OPTIONAL,
            category_exact=RequestConstants.Parameters.OPTIONAL,
            order_by=RequestConstants.Parameters.OPTIONAL
    ):
        """
        Retrieve list of storefronts from the working catalog using Tools V1 Service

        :param title_code: Code of title
        :type title_code: str
        :param branch_name: Code of branch
        :type branch_name: str
        :param page_number: Number of pages per query to display
        :type page_number: int
        :param page_size: Page size of query to display, 10 is default
        :type page_size: int
        :param order_direction: Order direction of query results, ASC is default
        :type order_direction: str
        :param code: Code of product to filter
        :type code: list of str
        :param friendly_name: Friendly name filter
        :type friendly_name: list of str
        :param search: User search
        :type search: list of str
        :param code_exact: Turn on or off exact search for product queries
        :type code_exact: bool
        :param friendly_name_exact: Turn on or off exact search for friendly name queries
        :type friendly_name_exact: bool
        :param product_code: Status filter
        :type product_code: list of str
        :param product_code_exact: Turn on or off exact search for status queries
        :type product_code_exact: bool
        :param search_exact: Turn on or off exact search type
        :type search_exact: bool
        :param category: Code of category
        :type category: str
        :param category_exact: Turn on or off exact search for category
        :type category_exact: bool
        :param order_by: Ordering options [CODE, FRIENDLY_NAME, STATUS, CREATED_AT]
        :type order_by: str
        :param active: Turn on or off searching only active storefronts
        :type active: bool
        :return: Response to Tools V1 Service get working catalog list of storefronts request
        :rtype: Response
        """

        return self.request('tools/api/v1/title/{0}/branch/{1}/catalog/working/storefront'.format(
            title_code, branch_name)
        ).params({
            'page_number': page_number,
            'page_size': page_size,
            'order_direction': order_direction,
            'code': code,
            'friendly_name': friendly_name,
            'search': search,
            'code_exact': code_exact,
            'friendly_name_exact': friendly_name_exact,
            'product_code': product_code,
            'product_code_exact': product_code_exact,
            'search_exact': search_exact,
            'category': category,
            'category_exact': category_exact,
            'order_by': order_by,
            'active': active
        }).get()

    def create_new_storefront_in_active_branch_working_catalog(
            self,
            title_code,
            branch_name,
            code='test_storefront_code_{}'.format(int(time.time())),
            friendly_name='test_storefront_friendly_name_{}'.format(int(time.time())),
            metadata=RequestConstants.Parameters.OPTIONAL,
            current_version=RequestConstants.Parameters.OPTIONAL,
            old_uuid=RequestConstants.Parameters.OPTIONAL,
            is_dirty=RequestConstants.Parameters.OPTIONAL,
            active=True,
            name=RequestConstants.Parameters.OPTIONAL,
            description=RequestConstants.Parameters.OPTIONAL,
            created_at=RequestConstants.Parameters.OPTIONAL,
            updated_at=RequestConstants.Parameters.OPTIONAL,
            products=RequestConstants.Parameters.OPTIONAL,
            tags_query=RequestConstants.Parameters.OPTIONAL,
            metadata_query=RequestConstants.Parameters.OPTIONAL,
            metadata_namespace_filter=RequestConstants.Parameters.OPTIONAL,
            categories=RequestConstants.Parameters.OPTIONAL,
            validation=RequestConstants.Parameters.OPTIONAL
    ):
        """
        Create a new Storefront in the active branch working catalog using Tools V1 Service

        :param title_code: Code of title
        :type title_code: str
        :param branch_name: Code of branch
        :type branch_name: str
        :param metadata: Metadata attached to the entity
        :type metadata: dict of (str, object)
        :param current_version: Current version of entity
        :type current_version: int
        :param is_dirty: Flag to indicate if entity is dirty
        :type is_dirty: bool
        :param old_uuid: UUID assigned to the previously published version of this entity
        :type old_uuid: str
        :param friendly_name: Friendly name filter
        :type friendly_name: list of str
        :param name: Localized name
        :type name: dict of (str, object)
        :param description: Localized description
        :type description: str
        :param created_at: Date of entity creation. Set by the system, user input is ignored
        :type created_at: int
        :param updated_at: Date when entity was updated. Set by the system, user input is ignored
        :type updated_at: int
        :param products: Products in the Storefront
        :type products: str
        :param active: Turn on or off searching only active storefronts
        :type active: bool
        :return: Response to Tools V1 Service get working catalog list of storefronts request
        :rtype: Response
        :param code: Code of entity to create to send in request json
        :type code: str
        :param tags_query: Array of tags that match tags in products
        :type tags_query: list of str
        :param metadata_query: Array of query strings to search meta data
        :type metadata_query: list of str
        :param validation: Validation messages
        :type validation: list of str
        :param metadata_namespace_filter: Metadata namespaces that should be included in product details
        :type metadata_namespace_filter: list of str
        :param categories: 	categories description for this storefront
        :type categories: dict of (str, object)
        """

        return self.request('tools/api/v1/title/{0}/branch/{1}/catalog/working/storefront'.format(
            title_code, branch_name)
        ).headers({
            'Content-Type': RequestConstants.ContentTypes.JSON,
            'Accept': RequestConstants.ContentTypes.JSON,
        }).json({
            'code': code,
            'active': active,
            'metadata': metadata,
            'current_version': current_version,
            'is_dirty': is_dirty,
            'old_uuid': old_uuid,
            'name': name,
            'description': description,
            'created_at': created_at,
            'updated_at': updated_at,
            'friendly_name': friendly_name,
            'products': products,
            'tags_query': tags_query,
            'metadata_query': metadata_query,
            'metadata_namespace_filter': metadata_namespace_filter,
            'categories': categories,
            'validation': validation
        }).post()

    def create_entity(
            self,
            title_code,
            branch_name,
            entity_type,
            entity_code,
            code,
            active,
            metadata=RequestConstants.Parameters.OPTIONAL,
            current_version=RequestConstants.Parameters.OPTIONAL,
            is_dirty=RequestConstants.Parameters.OPTIONAL,
            old_uuid=RequestConstants.Parameters.OPTIONAL,
            name=RequestConstants.Parameters.OPTIONAL,
            description=RequestConstants.Parameters.OPTIONAL,
            created_at=RequestConstants.Parameters.OPTIONAL,
            updated_at=RequestConstants.Parameters.OPTIONAL,
            friendly_name=RequestConstants.Parameters.OPTIONAL
    ):
        """
        Create a new entity in the active branch working catalog using Tools V1 Service

        This method can be applied to -- among other things -- entitlements, products, and storefronts,
        since their endpoints are virtually identical. The type of the entity to be updated is entity_type
        :param title_code: Code of title
        :type title_code: str
        :param branch_name: Code of branch
        :type branch_name: str
        :param entity_type: Entity type to create(currency, entitlement, product, override, promotion, storefront)
        :type entity_type: str
        :param entity_code: Code of entity to specify in request URL
        :type entity_code: str
        :param code: Code of entity to create to send in request json
        :type code: str
        :param active: Flag to indicate if entity is active
        :type active: bool
        :param metadata: Metadata attached to the entity
        :type metadata: dict of (str, object)
        :param current_version: Current version of entity
        :type current_version: int
        :param is_dirty: Flag to indicate if entity is dirty
        :type is_dirty: bool
        :param old_uuid: UUID assigned to the previously published version of this entity
        :type old_uuid: str
        :param name: Localized name
        :type name: dict of (str, object)
        :param description: Localized description
        :type description: str
        :param created_at: Date of entity creation. Set by the system, user input is ignored
        :type created_at: int
        :param updated_at: Date when entity was updated. Set by the system, user input is ignored
        :type updated_at: int
        :param friendly_name: Human readable name for the entity, only used in tools
        :type friendly_name: str
        :return: Response to Tools V1 Service create entity request
        :rtype: Response
        """

        return self.request('tools/api/v1/title/{0}/branch/{1}/catalog/working/{2}/{3}'.format(
            title_code,
            branch_name,
            entity_type,
            entity_code)
        ).headers({
            'Content-Type': RequestConstants.ContentTypes.JSON,
            'Accept': RequestConstants.ContentTypes.JSON,
        }).json({
            'code': code,
            'active': active,
            'metadata': metadata,
            'current_version': current_version,
            'is_dirty': is_dirty,
            'old_uuid': old_uuid,
            'name': name,
            'description': description,
            'created_at': created_at,
            'updated_at': updated_at,
            'friendly_name': friendly_name
        }).post()

    def get_entity(self, title_code, branch_name, entity_code, entity_type):
        """
        Get a specific entity in the active branch working catalog using Tools V1 Service

        This method can be applied to -- among other things -- entitlements, products, and storefronts, since their
        endpoints are virtually identical. The type of the entity to be updated is entity_type
        :param title_code: Code of title
        :type title_code: str
        :param branch_name: Code of branch
        :type branch_name: str
        :param entity_code: Code of entity
        :type entity_code: str
        :param entity_type: Entity type to retrieve(currency, entitlement, product, override, promotion, storefront)
        :type entity_type: str
        :return: Response to Tools V1 Service get entity request
        :rtype: Response
        """

        return self.request(
            'tools/api/v1/title/{0}/branch/{1}/catalog/working/{2}/{3}'.format(title_code, branch_name, entity_type,
                                                                               entity_code)
        ).get()

    def update_entity(self, title_code, branch_name, entity_code, entity_definition, entity_type):
        """
        Update definition of an entity with entity_code in title/branch using Tools V1 Service
        Must be published to become part of active catalog

        This method can be applied to -- among other things -- entitlements, products, and storefronts, since their
        endpoints are virtually identical. The type of the entity to be updated is entity_type
        :param title_code: Code of title
        :type title_code: str
        :param branch_name: Code of branch
        :type branch_name: str
        :param entity_code: Code of entity
        :type entity_code: str
        :param entity_definition: Updated entity definition
        :type entity_definition: dict of (str, object)
        :param entity_type: Entity type to update(currency, entitlement, product, override, promotion, storefront)
        :type entity_type: str
        :return: Response to Tools V1 Service update entity requet
        :rtype: Response
        """

        return self.request('tools/api/v1/title/{0}/branch/{1}/catalog/working/{2}/{3}'.format(
            title_code,
            branch_name,
            entity_type,
            entity_code)
        ).headers({
            'Content-Type': RequestConstants.ContentTypes.JSON,
            'Accept': RequestConstants.ContentTypes.JSON,
        }).json(entity_definition).post()

