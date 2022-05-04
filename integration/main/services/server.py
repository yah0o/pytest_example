from requests import Session

from gateway import Gateway
from integration.main.request import RequestConstants, Response
from items import CommitPurchasePaymentData, CommitPurchaseTwoFactorAuthInfo, LegacyProductItem


class ServerGateway(Gateway):
    """
    Server V1 Gateway
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
        Calls Server V1 Gateway for usage
        :param api_key: Gateway server API key from environment file
        :type api_key: str
        :return: Server Gateway object
        :rtype: ServerGateway
        """
        self.api_key = api_key
        return self

    def get_3ds_status(self,
                       order_id,
                       transaction_id=RequestConstants.Parameters.OPTIONAL,
                       fingerprint_sent=RequestConstants.Parameters.OPTIONAL,
                       challenge_sent=RequestConstants.Parameters.OPTIONAL,
                       log_id=RequestConstants.Parameters.OPTIONAL,
                       title_override=RequestConstants.Parameters.OPTIONAL,
                       message_id=RequestConstants.Parameters.OPTIONAL
                       ):
        """

        :param transaction_id: unique id for 3ds transaction
        :type transaction_id: string
        :param order_id: id of the order created on prepare purchase step
        :type order_id: string
        :param fingerprint_sent: identifier of created and submitted fingerprint iframe
        :type  fingerprint_sent: boolean
        :param challenge_sent: 	identifier of created and submitted challenge iframe
        :type challenge_sent: boolean
        :param log_id:
        :type log_id:
        :param title_override:
        :type title_override:
        :param message_id:
        :type message_id:
        :return:
        """
        return self.request('server/api/v1/get3dsStatus').headers({
            'x-freya-server-api-key': self.api_key
        }).json({
            'header': {
                'log_id': log_id,
                'title_override': title_override,
                'message_id': message_id
            },
            'body': {
                'order_id': order_id,
                'transaction_id': transaction_id,
                'fingerprint_sent': fingerprint_sent,
                'challenge_sent': challenge_sent
            }
        }).post()

    def ping(self):
        """
        Ping Server V1 Gateway
        :return: Response to Server V1 ping request
        :rtype: Response
        """

        return self.request('server/api/v1/ping').get()

    def ping_client(self):
        """
        Ping Client through Server V1 Gateway
        :return: Response to Server V1 ping client request
        :rtype: Response
        """

        return self.request('server/api/v1/ping/client').get()

    def account_created(self, profile_id, error_code=RequestConstants.Parameters.OPTIONAL,
                        content_type=RequestConstants.ContentTypes.JSON):
        """
        Notify platform account has been created on game server using Server V1 Gateway
        :param profile_id: Profile ID of account
        :type profile_id: int
        :param error_code: Error code
        :type error_code: str
        :param content_type: Define content type (JSON or MSGPACK) of the body of the request
        :type content_type: RequestConstants
        :return: Response to Server V1 account created request
        :rtype: Response
        """

        return self.request(
            'server/api/v1/accountCreated'
        ).headers({
            'x-freya-server-api-key': self.api_key
        }).json({
            'header': {},
            'body': {
                'profile_id': profile_id,
                'err_code': error_code
            }
        }).post(content_type)

    def get_accounts_by_wgid(self, wg_ids, region=RequestConstants.Parameters.OPTIONAL,
                             content_type=RequestConstants.ContentTypes.JSON):
        """
        Retrieve player information based on WGID using Server V1 Gateway
        :param wg_ids: WGID(s)
        :type wg_ids: list of int
        :param region: Region code of WGID(s)
        :type region: str
        :param content_type: Define content type (JSON or MSGPACK) of the body of the request
        :type content_type: RequestConstants
        :return: Response to Server V1 get account by wgid request
        :rtype: Response
        """

        return self.request(
            'server/api/v1/getAccountsByWgId'
        ).headers({
            'x-freya-server-api-key': self.api_key
        }).json({
            'header': {},
            'body': {
                'wg_ids': wg_ids,
                'region': region
            }
        }).post(content_type)

    def get_accounts_by_profile_id(self, profile_ids, region=RequestConstants.Parameters.OPTIONAL,
                                   content_type=RequestConstants.ContentTypes.JSON):
        """
        Retrieve player information based on profile ID using Server V1 Gateway
        :param profile_ids: Profile ID(s)
        :type profile_ids: list of int
        :param region: Region code of profile id(s)
        :type region: str
        :param content_type: Define content type (JSON or MSGPACK) of the body of the request
        :type content_type: RequestConstants
        :return: Response to Server V1 get accounts by profile id request
        :rtype: Response
        """

        return self.request(
            'server/api/v1/getAccountsByProfileId'
        ).headers({
            'x-freya-server-api-key': self.api_key
        }).json({
            'header': {},
            'body': {
                'profile_ids': profile_ids,
                'region': region
            }
        }).post(content_type)

    def get_accounts_by_nickname(self, names, region=RequestConstants.Parameters.OPTIONAL,
                                 content_type=RequestConstants.ContentTypes.JSON):
        """
        Retrieve player information based on account nickname using Server V1 Gateway
        :param names: Nickname(s) of account
        :type names: list of str
        :param region: Region code of account
        :type region: str
        :param content_type: Define content type (JSON or MSGPACK) of the body of the request
        :type content_type: RequestConstants
        :return: Response to Server V1 get accounts by nickname request
        :rtype: Response
        """

        return self.request(
            'server/api/v1/getAccountsByNickname'
        ).headers({
            'x-freya-server-api-key': self.api_key
        }).json({
            'header': {},
            'body': {
                'names': names,
                'region': region
            }
        }).post(content_type)

    def get_accounts_by_login(self, logins, region=RequestConstants.Parameters.OPTIONAL,
                              content_type=RequestConstants.ContentTypes.JSON):
        """
        Retrieve player information based on account nickname using Server V1 Gateway
        :param logins: Login(s) to retrieve
        :type logins: list of str
        :param region: Region code of account
        :type region: str
        :param content_type: Define content type (JSON or MSGPACK) of the body of the request
        :type content_type: RequestConstants
        :return: Response to Server V1 get accounts by login request
        :rtype: Response
        """

        return self.request(
            'server/api/v1/getAccountsByLogin'
        ).headers({
            'x-freya-server-api-key': self.api_key
        }).json({
            'header': {},
            'body': {
                'logins': logins,
                'region': region
            }
        }).post(content_type)

    def get_account_by_uid(self, uid, external_name, region=RequestConstants.Parameters.OPTIONAL,
                           content_type=RequestConstants.ContentTypes.JSON):
        """
        Retrieve player information based on uid and external name using Server V1 Gateway
        :param uid: uid to retrieve
        :type uid: str
        :param region: Region code of account
        :type region: str
        :param content_type: Define content type (JSON or MSGPACK) of the body of the request
        :type content_type: RequestConstants
        :return: Response to Server V1 get accounts by login request
        :rtype: Response
        """

        return self.request(
            'server/api/v1/getAccountByExternalUid'
        ).headers({
            'x-freya-server-api-key': self.api_key
        }).json({
            'header': {},
            'body': {
                'uid': uid,
                'external_name': external_name,
                'region': region
            }
        }).post(content_type)

    def get_account_commerce_info(self, wgid, country=RequestConstants.Parameters.OPTIONAL,
                                  content_type=RequestConstants.ContentTypes.JSON):
        """
        Retrieve list of linked and non-linked accounts to payment methods using Server V1 Gateway
        :param wgid: WGID of account
        :type wgid: int
        :param country: Country code of account
        :type country: str
        :param content_type: Define content type (JSON or MSGPACK) of the body of the request
        :type content_type: RequestConstants
        :return: Response to Server V1 get accounts by login request
        :rtype: Response
        """

        return self.request(
            'server/api/v1/getAccountCommerceInfo'
        ).headers({
            'x-freya-server-api-key': self.api_key
        }).json({
            'header': {},
            'body': {
                'wgid': wgid,
                'country': country
            }
        }).post(content_type)

    def get_account_commerce_info_v2(self, wgid, country=RequestConstants.Parameters.OPTIONAL,
                                     content_type=RequestConstants.ContentTypes.JSON):
        """
        Retrieve list of linked and non-linked accounts to payment methods using Server V1 Gateway
        :param wgid: WGID of account
        :type wgid: int
        :param country: Country code of account
        :type country: str
        :param content_type: Define content type (JSON or MSGPACK) of the body of the request
        :type content_type: RequestConstants
        :return: Response to Server V1 get accounts by login request
        :rtype: Response
        """

        return self.request(
            'server/api/v2/getAccountCommerceInfo'
        ).headers({
            'x-freya-server-api-key': self.api_key
        }).json({
            'header': {},
            'body': {
                'wgid': wgid,
                'country': country
            }
        }).post(content_type)

    def create_ban(
            self, profile_id, project, ban_type, reason, author_id,
            component=RequestConstants.Parameters.OPTIONAL,
            start_at=RequestConstants.Parameters.OPTIONAL,
            expire_at=RequestConstants.Parameters.OPTIONAL,
            curfew_from=RequestConstants.Parameters.OPTIONAL,
            curfew_to=RequestConstants.Parameters.OPTIONAL,
            comment=RequestConstants.Parameters.OPTIONAL,
            tag=RequestConstants.Parameters.OPTIONAL,
            meta=RequestConstants.Parameters.OPTIONAL,
            content_type=RequestConstants.ContentTypes.JSON):
        """
        Create ban of specific profile and game using Server V1 Gateway
        :param profile_id: Profile ID to be banned
        :type profile_id: int
        :param project: Project to be baned from (or all) ['ALL', 'GAME', 'CHAT', 'TRADING', 'CLAN', 'BATTLE',
        'TOURNAMENT', 'COSTUMER_SUPPORT', 'WGRATING_SYSTEM', 'WARGAG', 'WGCOMMENTS']
        :type project: str
        :param ban_type: Type of ban ['ACCESS_DENIED', 'READ_ONLY', 'PREMODERATION']
        :type ban_type: str
        :param reason: Reason for ban creation which can be displayed to a player
        :type reason: str
        :param author_id: Identifier of admin who created ban
        :type author_id: str
        :param component: Component of a project on which ban will be set
        :type component: str
        :param start_at: Time when ban will begin
        :type start_at: int
        :param expire_at: Time when ban will end
        :type expire_at: int
        :param curfew_from: Curfew start time
        :type curfew_from: int
        :param curfew_to: Curfew end time
        :type curfew_to: int
        :param comment: Administrative information for customer support employees
        :type comment: str
        :param tag: Any additional information (tag) about a ban
        :type tag: str
        :param meta: Map of string:string pairs that are passed through with request
        :type meta: dict of (str, str)
        :param content_type: Define content type (JSON or MSGPACK) of the body of the request
        :type content_type: RequestConstants
        :return: Response to Server V1 get accounts by login request
        :rtype: Response
        """

        return self.request(
            'server/api/v1/createBan'
        ).headers({
            'x-freya-server-api-key': self.api_key
        }).json({
            'header': {},
            'body': {
                'profile_id': profile_id,
                'project': project,
                'ban_type': ban_type,
                'component': component,
                'start_at': start_at,
                'expire_at': expire_at,
                'curfew_from': curfew_from,
                'curfew_to': curfew_to,
                'reason': reason,
                'author_id': author_id,
                'comment': comment,
                'tag': tag,
                'meta': meta
            }
        }).post(content_type)

    def get_webhook_audit_log(
            self,
            page,
            page_size,
            start_date=RequestConstants.Parameters.OPTIONAL,
            end_date=RequestConstants.Parameters.OPTIONAL,
            content_type=RequestConstants.ContentTypes.JSON):
        """
        Retrieve audit log entries for webhook activity using Server V1 Gateway
        :param page: Page number to retrieve
        :type page: int
        :param page_size: Define result entries to be returned in a page
        :type page_size: int
        :param start_date: Start date to query (in Unix epoch seconds)
        :type start_date: int
        :param end_date: End date to query (in Unix epoch seconds)
        :type end_date: int
        :param content_type: Define content type (JSON or MSGPACK) of the body of the request
        :type content_type: RequestConstants
        :return: Response to Server V1 get webhook audit log request
        :rtype: Response
        """

        return self.request(
            'server/api/v1/getWebhookAuditLog'
        ).headers({
            'x-freya-server-api-key': self.api_key
        }).json({
            'header': {},
            'body': {
                'start_date': start_date,
                'end_date': end_date,
                'page': page,
                'page_size': page_size
            }
        }).post(content_type)

    def generate_webhook_test(self, profile_id=RequestConstants.Parameters.OPTIONAL,
                              content_type=RequestConstants.ContentTypes.JSON):
        """
        Generate a 'test' webhook message which will be sent to the registered webhook endpoint for this title
        using Server V1 Gateway
        :param profile_id: Profile ID to receive webhook ping
        :type profile_id: int
        :param content_type: Define content type (JSON or MSGPACK) of the body of the request
        :type content_type: RequestConstants
        :return: Response to Server V1 generate webhook test request
        :rtype: Response
        """

        return self.request(
            'server/api/v1/generateWebhookTest'
        ).headers({
            'x-freya-server-api-key': self.api_key
        }).json({
            'header': {},
            'body': {
                'profile_id': profile_id
            }
        }).post(content_type)

    def move_currency(
            self,
            tx_id,
            source_profile_id,
            destination_profile_id,
            currency_code,
            amount,
            meta=RequestConstants.Parameters.OPTIONAL,
            content_type=RequestConstants.ContentTypes.JSON):
        """
        Transfer currency from one profile to another profile belonging to the same user using Server V1 Gateway
        :param tx_id: Caller supplied unique id for idempotency
        :type tx_id: str
        :param source_profile_id: Profile ID that currently owns the currency
        :type source_profile_id: int
        :param destination_profile_id: Profile ID to move the currency to
        :type destination_profile_id: int
        :param currency_code: Currency code to be transferred
        :type currency_code: str
        :param amount: Amount of currency to transfer
        :type amount: str
        :param meta: Map of string:string pairs that are passed through with request
        :type meta: dict of (str, str)
        :param content_type: Define content type (JSON or MSGPACK) of the body of the request
        :type content_type: RequestConstants
        :return: Response to Server V1 move currency request
        :rtype: Response
        """

        return self.request(
            'server/api/v1/moveCurrency'
        ).headers({
            'x-freya-server-api-key': self.api_key
        }).json({
            'header': {},
            'body': {
                'transaction_id': tx_id,
                'source_profile_id': source_profile_id,
                'destination_profile_id': destination_profile_id,
                'currency_code': currency_code,
                'amount': amount,
                'meta': meta
            }
        }).post(content_type)

    def prepare_purchase(
            self,
            tx_id,
            country,
            language,
            payer_wgid,
            receiver_wgid,
            products,
            payment_type,
            expected_price,
            payment_method,
            storefront,
            payer_email=RequestConstants.Parameters.OPTIONAL,
            payer_current_ip=RequestConstants.Parameters.OPTIONAL,
            payment_group_id=RequestConstants.Parameters.OPTIONAL,
            order_coupons=RequestConstants.Parameters.OPTIONAL,
            meta=RequestConstants.Parameters.OPTIONAL,
            content_type=RequestConstants.ContentTypes.JSON
    ):
        """
        Prepare a real money purchase of a product using Server V1 Gateway
        :param tx_id: Caller supplied unique transaction id
        :type tx_id: str
        :param country: Country code
        :type country: str
        :param language: Language locale format
        :type language: str
        :param payer_wgid: WGID of buyer
        :type payer_wgid: int
        :param payer_email: Email of buyer
        :type payer_email: str
        :param receiver_wgid: WGID of account receiving purchase
        :type receiver_wgid: int
        :param products: List of products to purchase
        :type products: list of dict
        :param payment_type: Payment type = ['NONE', 'WGM', 'PSA', 'BONUS_CODE', 'IGP', 'CUSTOMER_SUPPORT']
        :type payment_type: str
        :param expected_price: Expected price of product to purchase
        :type expected_price: dict of (str, str)
        :param payment_group_id: Payment group ID
        :type payment_group_id: int
        :param payment_method: Method of payment
        :type payment_method: str
        :param storefront: Code of storefront which contains product
        :type storefront: str
        :param order_coupons: Any coupon code(s) used for this purchase
        :type order_coupons: list of str
        :param meta: Map of string:string pairs that are passed through with request
        :type meta: dict of (str, str)
        :param content_type: Define content type (JSON or MSGPACK) of the body of the request
        :type content_type: RequestConstants
        :return: Response to Server V1 prepare purchase request
        :rtype: Response
        :param payer_current_ip: Payer IP address
        :type payer_current_ip: str
        """

        return self.request(
            'server/api/v1/preparePurchase'
        ).headers({
            'x-freya-server-api-key': self.api_key
        }).json({
            'header': {},
            'body': {
                'transaction_id': tx_id,
                'storefront': storefront,
                'payer_current_ip': payer_current_ip,
                'country': country,
                'language': language,
                'meta': meta,
                'payer_wgid': payer_wgid,
                'payer_email': payer_email,
                'receiver_wgid': receiver_wgid,
                'products': [product.as_json for product in products],
                'order_coupons': order_coupons,
                'expected_price': expected_price.as_json,
                'payment_type': payment_type,
                'payment_method': payment_method,
                'payment_group_id': payment_group_id,
            }
        }).post(content_type)

    def commit_purchase(
            self,
            transaction_id,
            order_id,
            payer_wgid,
            payment_amount,
            payment_code,
            payment_method,
            twofa_code,
            twofa_type,
            payer_current_ip=RequestConstants.Parameters.OPTIONAL,
            token_id=RequestConstants.Parameters.OPTIONAL,
            set3ds_data=RequestConstants.Parameters.OPTIONAL,
            set3ds_url=RequestConstants.Parameters.OPTIONAL,
            content_type=RequestConstants.ContentTypes.JSON):
        """
        Validate 2FA authorization for user and process purchase for provided order using bound payment method through
        Server V1 Gateway
        :param transaction_id: Caller supplied unique transaction id
        :type transaction_id: str
        :param order_id: Order ID
        :type order_id: str
        :param payer_wgid: WGID of buyer
        :type payer_wgid: int
        :param payment_amount: Amount of payment
        :type payment_amount: str
        :param payment_code: Code of payment
        :type payment_code: str
        :param payment_method: Payment method
        :type payment_method: str
        :param twofa_code: Code of 2FA
        :type twofa_code: str
        :param twofa_type: Type of 2FA
        :type twofa_type: str
        :param token_id: ID of the credit card for Alfabank
        :type token_id: int
        :param set3ds_data: struct to pass data required for 3ds process
        :type set3ds_data: object
        :param set3ds_url: str
        :type set3ds_url: Url to 3ds web payment
        :param content_type: Define content type (JSON or MSGPACK) of the body of the request
        :type content_type: RequestConstants
        :return: Response to Server V1 commit purchase request
        :rtype: Response
        :param: payer_current_ip: Payer IP address
        :type payer_current_ip: str
        """

        payment_data = CommitPurchasePaymentData(payment_amount, payment_code, payment_method)
        twofa_info = CommitPurchaseTwoFactorAuthInfo(twofa_code, twofa_type)

        return self.request(
            'server/api/v1/commitPurchase'
        ).headers({
            'x-freya-server-api-key': self.api_key
        }).json({
            'header': {},
            'body': {
                'transaction_id': transaction_id,
                'order_id': order_id,
                'payer_wgid': payer_wgid,
                'payment_data': payment_data.as_json,
                '2fa_info': twofa_info.as_json,
                'token_id': token_id,
                '3ds_web_payment_url': set3ds_url,
                '3ds_data': set3ds_data,
                'payer_current_ip': payer_current_ip
            }
        }).post(content_type)

    def purchase_product(
            self,
            tx_id,
            source_profile_id,
            destination_profile_id,
            product_code,
            amount,
            expected_prices,
            storefront,
            country=RequestConstants.Parameters.OPTIONAL,
            payer_current_ip=RequestConstants.Parameters.OPTIONAL,
            coupons=RequestConstants.Parameters.OPTIONAL,
            content_type=RequestConstants.ContentTypes.JSON):
        """
        Purchase product with virtual currency using Server V1 Gateway
        :param tx_id: Transaction ID to allow polling and enforce idempotency
        :type tx_id: str
        :param source_profile_id: Profile ID to withdraw purchase price
        :type source_profile_id: int
        :param destination_profile_id: Profile ID to receive the product
        :type destination_profile_id: int
        :param product_code: Code of product to purchase
        :type product_code: str
        :param amount: Amount of product to purchase
        :type amount: int
        :param expected_prices: Expected total price of purchase to verify user is charged the same amount as shown
        in the client
        :type expected_prices: list of dict
        :param coupons: Coupon(s) associated with this purchase
        :type coupons: list of str
        :param storefront: Code of storefront
        :type storefront: str
        :param country: Country code
        :type country: str
        :param content_type: Define content type (JSON or MSGPACK) of the body of the request
        :type content_type: RequestConstants
        :return: Response to Server V1 purchase product request
        :rtype: Response
        :param payer_current_ip: Payer IP address
        :type payer_current_ip: str
        """

        product = LegacyProductItem(product_code, amount, coupons=coupons)

        return self.request(
            'server/api/v1/purchaseProduct'
        ).headers({
            'x-freya-server-api-key': self.api_key
        }).json({
            'header': {},
            'body': {
                'transaction_id': tx_id,
                'source_profile_id': source_profile_id,
                'destination_profile_id': destination_profile_id,
                'product': product.as_json,
                'expected_prices': [expected_price.as_json for expected_price in expected_prices],
                'storefront': storefront,
                'payer_current_ip': payer_current_ip,
                'country': country
            }
        }).post(content_type)

    def purchase_product_with_money_v2(
            self,
            tx_id,
            country,
            language,
            payer_wgid,
            payer_email,
            receiver_wgid,
            products,
            payment_type,
            expected_price,
            storefront,
            client_payment_method_id,
            payer_current_ip=RequestConstants.Parameters.OPTIONAL,
            order_coupons=RequestConstants.Parameters.OPTIONAL,
            meta=RequestConstants.Parameters.OPTIONAL,
            gift=RequestConstants.Parameters.OPTIONAL,
            receiver_country=RequestConstants.Parameters.OPTIONAL,
            content_type=RequestConstants.ContentTypes.JSON
    ):
        """
        Purchase product with real money using Server V2 Gateway
        :param tx_id: Transaction ID to allow polling and enforce idempotency
        :type tx_id: str
        :param country: Country code
        :type country: str
        :param language: Language locale format
        :type language: str
        :param payer_wgid: WGID of payer
        :type payer_wgid: str
        :param payer_email: Email of payer
        :type payer_email: str
        :param receiver_wgid: WGID of receiver
        :type receiver_wgid: str
        :param products: Product(s) to purchase
        :type products: list of dict
        :param payment_type: Type of payment
        :type payment_type: str
        :param client_payment_method_id: client payment method id
        :type client_payment_method_id: int
        :param expected_price: Expected total price of purchase to verify user is charged the same amount as shown
        in the client
        :type expected_price: dict of(str, str)
        :param storefront: Storefront associated with product(s)
        :type storefront: str
        :param order_coupons: Coupon(s) associated with the purchase
        :type order_coupons: list of str
        :param meta: Map of string:string pairs that are passed through with request
        :type meta: dict of (str, str)
        :param content_type: Define content type (JSON or MSGPACK) of the body of the request
        :type content_type: RequestConstants
        :return: Response to Server V1 purchase product with money request
        :rtype: Response
        :param payer_current_ip: Payer IP address
        :type payer_current_ip: str
        :param gift: Gift product or not
        :type gift: dict
        :param receiver_country: Receiver country code
        :type receiver_country: str
        """

        return self.request(
            'server/api/v2/purchaseProductWithMoney'
        ).headers({
            'x-freya-server-api-key': self.api_key
        }).json({
            'header': {},
            'body': {
                'transaction_id': tx_id,
                'storefront': storefront,
                'payer_current_ip': payer_current_ip,
                'payer_country': country,
                'receiver_country': receiver_country,
                'language': language,
                'meta': meta,
                'payer_wgid': payer_wgid,
                'payer_email': payer_email,
                'receiver_wgid': receiver_wgid,
                'products': [product.as_json for product in products],
                'order_coupons': order_coupons,
                'expected_price': expected_price.as_json,
                'payment_type': payment_type,
                'client_payment_method_id': client_payment_method_id,
                'gift': gift
            }
        }).post(content_type)

    def grant_product(
            self,
            tx_id,
            country,
            language,
            destination_profile_id,
            products,
            grant_type=RequestConstants.Parameters.OPTIONAL,
            payer_current_ip=RequestConstants.Parameters.OPTIONAL,
            meta=RequestConstants.Parameters.OPTIONAL,
            storefront=RequestConstants.Parameters.OPTIONAL,
            content_type=RequestConstants.ContentTypes.JSON
    ):
        """
        Grant a product to specified profile using Server V1 Gateway
        :param tx_id: Transaction ID to allow polling and enforce idempotency
        :type tx_id: str
        :param country: Country code
        :type country: str
        :param language: Language locale format
        :type language: str
        :param destination_profile_id: Profile ID to receive the product(s)
        :type destination_profile_id: int
        :param products: Product(s) to grant
        :type products: list of dict
        :param grant_type: Type of grant, defaults to GAME = ['NONE', 'GAME', 'BONUS_CODE', 'CUSTOMER_SUPPORT']
        :type grant_type: str
        :param meta: Map of string:string pairs that are passed through with request
        :type meta: dict of (str, str)
        :param storefront: Storefront associated with product(s)
        :type storefront: str
        :param content_type: Define content type (JSON or MSGPACK) of the body of the request
        :type content_type: RequestConstants
        :return: Response to Server V1 grant product request
        :rtype: Response
        :param payer_current_ip: Real player IP
        :type payer_current_ip: str
        """

        meta = {} if meta is None else meta

        return self.request(
            'server/api/v1/grantProduct'
        ).headers({
            'x-freya-server-api-key': self.api_key
        }).json({
            'header': {},
            'body': {
                'transaction_id': tx_id,
                'destination_profile_id': destination_profile_id,
                'country': country,
                'language': language,
                'grant_type': grant_type,
                'meta': meta,
                'products': [product.as_json for product in products],
                'storefront': storefront,
                'payer_current_ip': payer_current_ip
            }
        }).post(content_type)

    def get_inventory(self, profile_id, content_type=RequestConstants.ContentTypes.JSON):
        """
        Retrieve inventory from specified profile using Server V1 Gateway
        :param profile_id: Profile ID to retrieve inventory and currency balance(s)
        :type profile_id: int
        :param content_type: Define content type (JSON or MSGPACK) of the body of the request
        :type content_type: RequestConstants
        :return: Response to Server V1 get inventory request
        :rtype: Response
        """

        return self.request(
            'server/api/v1/getInventory'
        ).headers({
            'x-freya-server-api-key': self.api_key
        }).json({
            'header': {},
            'body': {
                'profile_id': profile_id
            }
        }).post(content_type)

    def get_full_inventory(self, profile_id, content_type=RequestConstants.ContentTypes.JSON):
        """
        Retrieve inventory from specified profile and its subprofile(s) using Server V1 Gateway
        :param profile_id: Profile ID to retrieve inventory and currency balance(s)
        :type profile_id: int
        :param content_type: Define content type (JSON or MSGPACK) of the body of the request
        :type content_type: RequestConstants
        :return: Response to Server V1 get full inventory request
        :rtype: Response
        """

        # since FREYA-782 method gets inventory only for profile id

        return self.request(
            'server/api/v1/getFullInventory'
        ).headers({
            'x-freya-server-api-key': self.api_key
        }).json({
            'header': {},
            'body': {
                'profile_id': profile_id,
            }
        }).post(content_type)

    def fetch_product_list(self, storefront, wgid, country, language,
                           additional_data=RequestConstants.Parameters.OPTIONAL,
                           content_type=RequestConstants.ContentTypes.JSON,
                           tracking_id=RequestConstants.Parameters.OPTIONAL):
        """
        Retrieve list of product(s) in specified storefront using Server V1 Gateway
        :param storefront: Storefront code to retrieve the list of product(s)
        :type storefront: str
        :param wgid: WGID
        :type wgid: int
        :param country: Country code
        :type country: str
        :param language: Language locale format
        :type language: str
        :param tracking_id:
        :param additional_data: Additional data
        :type additional_data: dict of (str, object)
        :param content_type: Define content type (JSON or MSGPACK) of the body of the request
        :type content_type: RequestConstants
        :return: Response to Server V1 fetch product list request
        :rtype: Response
        """

        additional_data = {} if additional_data is None else additional_data

        return self.request(
            'server/api/v1/fetchProductList'
        ).headers({
            'x-freya-server-api-key': self.api_key,
            'x-np-tracking-id': tracking_id
        }).json({
            'header': {},
            'body': {
                'storefront': storefront,
                'wgid': wgid,
                'country': country,
                'language': language,
                'additional_data': additional_data
            }
        }).post(content_type)

    def fetch_product_list_state(self, storefront, wgid, country, language,
                                 response_fields=RequestConstants.Parameters.OPTIONAL,
                                 product_codes=None,
                                 additional_data=RequestConstants.Parameters.OPTIONAL,
                                 content_type=RequestConstants.ContentTypes.JSON):
        """
        Gets state of user's products (if product has any user-specific state) in specified storefront using Server
         V1 Gateway
        :param storefront: Storefront code to retrieve the list of product(s)
        :type storefront: str
        :param wgid: WGID
        :type wgid: int
        :param country: Country code
        :type country: str
        :param response_fields: fields to be in response
        :type response_fields: list
        :param product_codes: product codes
        :type product_codes: list
        :param language: Language locale format
        :type language: str
        :param additional_data: Additional data
        :type additional_data: dict of (str, object)
        :param content_type: Define content type (JSON or MSGPACK) of the body of the request
        :type content_type: RequestConstants
        :return: Response to Server V1 fetch product list request
        :rtype: Response
        """

        response_fields_true = {} if response_fields is None else {i: True for i in response_fields}
        additional_data = {} if additional_data is None else additional_data

        return self.request(
            'server/api/v1/fetchProductListState'
        ).headers({
            'x-freya-server-api-key': self.api_key
        }).json({
            'header': {},
            'body': {
                'storefront': storefront,
                'wgid': wgid,
                'country': country,
                'language': language,
                'additional_data': additional_data,
                'response_fields': response_fields_true,
                'product_codes': product_codes
            }
        }).post(content_type)

    def fetch_products(self, product_codes, wgid, country, language, storefront=RequestConstants.Parameters.OPTIONAL,
                       additional_data=RequestConstants.Parameters.OPTIONAL,
                       content_type=RequestConstants.ContentTypes.JSON):
        """
        Retrieve product  using Server V1 Gateway
        :param product_codes: Product code(s) to retrieve
        :type product_codes: list of str
        :param wgid: WGID
        :type wgid: int
        :param country: Country code
        :type country: str
        :param language: Language locale format
        :type language: str
        :param storefront: Storefront code
        :type storefront: str
        :param additional_data: Additional data
        :type additional_data: dict of (str, object)
        :param content_type: Define content type (JSON or MSGPACK) of the body of the request
        :type content_type: RequestConstants
        :return: Response to Server V1 fetch products request
        :rtype: Response
        """

        additional_data = {} if additional_data is None else additional_data

        return self.request(
            'server/api/v1/fetchProducts'
        ).headers({
            'x-freya-server-api-key': self.api_key
        }).json({
            'header': {},
            'body': {
                'product_codes': product_codes,
                'wgid': wgid,
                'country': country,
                'language': language,
                'storefront': storefront,
                'additional_data': additional_data
            }
        }).post(content_type)

    def fetch_product_price(self, product_code, country, quantity, storefront=RequestConstants.Parameters.OPTIONAL,
                            content_type=RequestConstants.ContentTypes.JSON):
        """
        Retrieve the price of specific product using Server V1 Gateway
        :param product_code: Product code
        :type product_code: str
        :param country: Country code
        :type country: str
        :param quantity: Amount of product to retrieve price
        :type quantity: int
        :param storefront: Storefront code
        :type storefront: str
        :param content_type: Define content type (JSON or MSGPACK) of the body of the request
        :type content_type: RequestConstants
        :return: Response to Server V1 fetch product price request
        :rtype: Response
        """

        return self.request(
            'server/api/v1/fetchProductPrice'
        ).headers({
            'x-freya-server-api-key': self.api_key
        }).json({
            'header': {},
            'body': {
                'product_code': product_code,
                'country': country,
                'quantity': quantity,
                'storefront': storefront
            }
        }).post(content_type)

    def fetch_product_price_v2(self, product_code, country, quantity, wgid,
                               storefront=RequestConstants.Parameters.OPTIONAL,
                               content_type=RequestConstants.ContentTypes.JSON,
                               response_fields=RequestConstants.ContentTypes.JSON,
                               receiver_country=RequestConstants.Parameters.OPTIONAL):
        """
        Retrieve the price of specific product using Server V2 Gateway
        :param product_code: Product code
        :type product_code: str
        :param country: Country code
        :type country: str
        :param quantity: Amount of product to retrieve price
        :type quantity: int
        :param storefront: Storefront code
        :type storefront: str
        :param content_type: Define content type (JSON or MSGPACK) of the body of the request
        :type content_type: RequestConstants
        :param receiver_country: Receiver's country code. ISO 3166-1
        :type receiver_country: str
        :return: Response to Server V1 fetch product price request
        :rtype: Response
        """

        return self.request(
            'server/api/v2/fetchProductPrice'
        ).headers({
            'x-freya-server-api-key': self.api_key
        }).json({
            'header': {},
            'body': {
                'product_code': product_code,
                'country': country,
                'quantity': quantity,
                'storefront': storefront,
                'wgid': wgid,
                'response_fields': response_fields,
                'receiver_country': receiver_country
            }
        }).post(content_type)

    def get_purchase_status_by_order_id(self, order_id, profile_id, content_type=RequestConstants.ContentTypes.JSON):
        """
        Retrieve purchase status by order ID using Server V1 Gateway
        :param order_id: Order ID of purchase
        :type order_id: str
        :param profile_id: Profile ID
        :type profile_id: int
        :param content_type: Define content type (JSON or MSGPACK) of the body of the request
        :type content_type: RequestConstants
        :return: Response to Server V1 get purchase status by order id request
        :rtype: Response
        """

        return self.request(
            'server/api/v1/getPurchaseStatusByOrderId'
        ).headers({
            'x-freya-server-api-key': self.api_key
        }).json({
            "header": {},
            "body": {
                "order_id": order_id,
                "profile_id": profile_id
            }
        }).post(content_type)

    def grant_currency(self, tx_id, profile_id, currency_code, amount, content_type=RequestConstants.ContentTypes.JSON):
        """
        Grant virtual currency to a profile using Server V1 Gateway
        :param tx_id: Transaction ID to allow polling and enforce idempotency
        :type tx_id: str
        :param profile_id: Profile ID to receive currency
        :type profile_id: int
        :param currency_code: Currency code to grant
        :type currency_code: str
        :param amount: Amount of currency to grant
        :type amount: str
        :param content_type: Define content type (JSON or MSGPACK) of the body of the request
        :type content_type: RequestConstants
        :return: Response to Server V1 grant currency request
        :rtype: Response
        """

        return self.request(
            'server/api/v1/grantCurrency'
        ).headers({
            'x-freya-server-api-key': self.api_key
        }).json({
            'header': {},
            'body': {
                'profile_id': profile_id,
                'currency_code': currency_code,
                'amount': amount,
                'transaction_id': tx_id,
            }
        }).post(content_type)

    def consume_currency(self, tx_id, profile_id, currency_code, amount,
                         content_type=RequestConstants.ContentTypes.JSON):
        """
        Consume virtual currency of a profile, returns updated balance using Server V1 Gateway
        :param tx_id: Transaction ID to allow polling and enforce idempotency
        :type tx_id: str
        :param profile_id: Profile ID to consume currency
        :type profile_id: int
        :param currency_code: Currency code to consume
        :type currency_code: str
        :param amount: Amount of currency to consume
        :type amount: str
        :param content_type: Define content type (JSON or MSGPACK) of the body of the request
        :type content_type: RequestConstants
        :return: Response to Server V1 consume currency request
        :rtype: Response
        """

        return self.request(
            'server/api/v1/consumeCurrency'
        ).headers({
            'x-freya-server-api-key': self.api_key
        }).json({
            'header': {},
            'body': {
                'profile_id': profile_id,
                'currency_code': currency_code,
                'amount': amount,
                'transaction_id': tx_id,
            }
        }).post(content_type)

    def delete_sub_profile(self, profile_id, meta=RequestConstants.Parameters.OPTIONAL,
                           content_type=RequestConstants.ContentTypes.JSON):
        """
        Deletes the specified profile using Server V1 Gateway. The profile must be empty with no children, entitlements,
        or currencies
        :param profile_id: Profile ID to delete
        :type profile_id: int
        :param meta: Map of string:string pairs that are passed through with request
        :type meta: dict of (str, str)
        :param content_type: Define content type (JSON or MSGPACK) of the body of the request
        :type content_type: RequestConstants
        :return: Response to Server V1 delete sub profile request
        :rtype: Response
        """

        return self.request(
            'server/api/v1/deleteSubProfile'
        ).headers({
            'x-freya-server-api-key': self.api_key
        }).json({
            'header': {},
            'body': {
                'profile_id': profile_id,
                'meta': meta
            }
        }).post(content_type)

    def grant_entitlement(
            self,
            profile_id,
            entitlement_code,
            amount,
            tx_id=RequestConstants.Parameters.OPTIONAL,
            content_type=RequestConstants.ContentTypes.JSON):
        """
        Grant entitlement to a profile using Server V1 Gateway
        :param profile_id: Profile ID to receive entitlement
        :type profile_id: int
        :param entitlement_code: Entitlement code to grant
        :type entitlement_code: str
        :param amount: Amount of entitlement to grant
        :type amount: str
        :param tx_id: Transaction ID to allow polling and enforce idempotency
        :type tx_id: str
        :param content_type: Define content type (JSON or MSGPACK) of the body of the request
        :type content_type: RequestConstants
        :return: Response to Server V1 grant entitlement request
        :rtype: Response
        """

        return self.request(
            'server/api/v1/grantEntitlement'
        ).headers({
            'x-freya-server-api-key': self.api_key
        }).json({
            'header': {},
            'body': {
                'profile_id': profile_id,
                'entitlement_code': entitlement_code,
                'amount': amount,
                'transaction_id': tx_id,
            }
        }).post(content_type)

    def consume_entitlement(
            self,
            profile_id,
            entitlement_code,
            amount,
            tx_id=RequestConstants.Parameters.OPTIONAL,
            meta=RequestConstants.Parameters.OPTIONAL,
            content_type=RequestConstants.ContentTypes.JSON):
        """
        Consume one or more instances of an entitlement. Returns the updated inventory information
        :param profile_id: Profile ID
        :type profile_id: int
        :param entitlement_code: Entitlement code to consume
        :type entitlement_code: str
        :param amount: Amount of entitlement to consume
        :type amount: int
        :param tx_id: Transaction ID to allow polling and enforce idempotency
        :type tx_id: str
        :param meta: Map of string:string pairs that are passed through with request
        :type meta: dict of (str, str)
        :param content_type: Define content type (JSON or MSGPACK) of the body of the request
        :type content_type: RequestConstants
        :return: Response to Server V1 consume entitlement request
        :rtype: Response
        """

        return self.request(
            'server/api/v1/consumeEntitlement'
        ).headers({
            'x-freya-server-api-key': self.api_key
        }).json({
            'header': {},
            'body': {
                'transaction_id': tx_id,
                'profile_id': profile_id,
                'entitlement_code': entitlement_code,
                'amount': amount,
                'meta': meta,
            }
        }).post(content_type)

    def cancel_entitlement(
            self,
            profile_id,
            cancel_transaction_id,
            transaction_id=RequestConstants.Parameters.OPTIONAL,
            content_type=RequestConstants.ContentTypes.JSON):
        """
        Cancel an entitlement transaction using Server V1 Gateway
        :param profile_id: Profile ID of transaction to cancel
        :type profile_id: int
        :param cancel_transaction_id: Transaction ID to allow polling and enforce idempotency
        :type cancel_transaction_id: str
        :param transaction_id: Transaction ID to cancel
        :type transaction_id: str
        :param content_type: Define content type (JSON or MSGPACK) of the body of the request
        :type content_type: RequestConstants
        :return: Response to Server V1 cancel entitlement request
        :rtype: Response
        """

        return self.request(
            'server/api/v1/cancelEntitlement'
        ).headers({
            'x-freya-server-api-key': self.api_key
        }).json({
            'header': {},
            'body': {
                'transaction_id': transaction_id,
                'profile_id': profile_id,
                'cancel_transaction_id': cancel_transaction_id
            }
        }).post(content_type)

    def reverse_entitlement(self, profile_id, transaction_id_to_reverse, new_transaction_id,
                            content_type=RequestConstants.ContentTypes.JSON):
        """
        Reverse an entitlement transaction using Server V1 Gateway
        :param profile_id: Profile ID of transaction to reverse
        :type profile_id: int
        :param transaction_id_to_reverse: Transaction ID to allow polling and enforce idempotency
        :type transaction_id_to_reverse: str
        :param new_transaction_id: Transaction ID to reverse
        :type new_transaction_id: str
        :param content_type: Define content type (JSON or MSGPACK) of the body of the request
        :type content_type: RequestConstants
        :return: Response to Server V1 reverse entitlement request
        :rtype: Response
        """

        return self.request(
            'server/api/v1/reverseEntitlement'
        ).headers({
            'x-freya-server-api-key': self.api_key
        }).json({
            'header': {},
            'body': {
                'txn_id_to_reverse': transaction_id_to_reverse,
                'new_transaction_id': new_transaction_id,
                'profile_id': profile_id
            }
        }).post(content_type)

    def create_auth_token(
            self,
            profile_id,
            target_application,
            region=RequestConstants.Parameters.OPTIONAL,
            client_ip='127.0.0.1',
            content_type=RequestConstants.ContentTypes.JSON):
        """
        Create authentication token using Server V1 Gateway
        :param profile_id: Profile ID
        :type profile_id: int
        :param target_application: Target application for the authentication token
        :type target_application: str
        :param region: SPA region
        :type region: str
        :param client_ip: Client IP address
        :type client_ip: str
        :param content_type: Define content type (JSON or MSGPACK) of the body of the request
        :type content_type: RequestConstants
        :return: Response to Server V1 create auth token request
        :rtype: Response
        """

        return self.request(
            'server/api/v1/createAuthToken'
        ).headers({
            'x-freya-server-api-key': self.api_key
        }).json({
            'header': {},
            'body': {
                'region': region,
                'profile_id': profile_id,
                'auth_token_target_application': target_application,
                'client_ip': client_ip
            }
        }).post(content_type)

    def create_remember_me_token(
            self,
            email,
            password,
            fingerprint=RequestConstants.Parameters.OPTIONAL,
            region=RequestConstants.Parameters.OPTIONAL,
            client_ip=RequestConstants.Parameters.OPTIONAL,
            content_type=RequestConstants.ContentTypes.JSON,
            client_language=RequestConstants.Parameters.OPTIONAL):
        """
        Create remember me token using Server V1 Gateway
        :param email: Wargaming account email
        :type email: str
        :param password: Wargaming account password
        :type password: str
        :param fingerprint: Client device fingerprint
        :type fingerprint: str
        :param region: SPA region
        :type region: str
        :param client_ip: Client IP address
        :type client_ip: str
        :param content_type: Define content type (JSON or MSGPACK) of the body of the request
        :type content_type: RequestConstants
        :return: Response to Server V1 create remember me token request
        :rtype: Response
        :param client_language: Client language
        :type client_language: str
        """

        return self.request(
            'server/api/v1/createRememberMeToken'
        ).headers({
            'x-freya-server-api-key': self.api_key
        }).json({
            'header': {},
            'body': {
                'email': email,
                'password': password,
                'fingerprint': fingerprint,
                'client_ip': client_ip,
                'region': region,
                'client_language': client_language
            }
        }).post(content_type)

    def begin_game_session(
            self,
            profile_id,
            parent_game_session_id=RequestConstants.Parameters.OPTIONAL,
            game_session_id=RequestConstants.Parameters.OPTIONAL,
            session_type=RequestConstants.Parameters.OPTIONAL,
            session_ttl=RequestConstants.Parameters.OPTIONAL,
            content_type=RequestConstants.ContentTypes.JSON,
            client_ip=RequestConstants.Parameters.OPTIONAL,
            client_language=RequestConstants.Parameters.OPTIONAL):
        """
        Notify platform game session has started for profile using Server V1 Gateway
        :param profile_id: Profile ID
        :type profile_id: int
        :param parent_game_session_id: Parent session id if this is a child session, e.g. a battle
        :type parent_game_session_id: str
        :param game_session_id: Game generated session id that must be unique within the game
        :type game_session_id: str
        :param session_type: Type of session
        :type session_type: str
        :param session_ttl: Maximum TTL for session
        :type session_ttl: int
        :param content_type: Define content type (JSON or MSGPACK) of the body of the request
        :type content_type: RequestConstants
        :return: Response to Server V1 begin game session request
        :rtype: Response
        :param client_ip: Client IP
        :type client_ip: str
        :param client_language: Client language
        :type client_language: str
        """

        return self.request(
            'server/api/v1/beginGameSession'
        ).headers({
            'x-freya-server-api-key': self.api_key
        }).json({
            'header': {},
            'body': {
                'profile_id': profile_id,
                'parent_game_session_id': parent_game_session_id,
                'game_session_id': game_session_id,
                'session_type': session_type,
                'session_ttl': session_ttl,
                'client_ip': client_ip,
                'client_language': client_language
            }
        }).post(content_type)

    def end_game_session(
            self,
            profile_id,
            session_type=RequestConstants.Parameters.OPTIONAL,
            session_id=RequestConstants.Parameters.OPTIONAL,
            content_type=RequestConstants.ContentTypes.JSON,
            client_ip=RequestConstants.Parameters.OPTIONAL,
            client_language=RequestConstants.Parameters.OPTIONAL):
        """
        Notify platform game session has ended for profile using Server V1 Gateway
        :param profile_id: Profile ID
        :type profile_id: int
        :param session_type: Type of session
        :type session_type: str
        :param session_id: Game generated session id that must be unique within the game
        :type session_id: str
        :param content_type: Define content type (JSON or MSGPACK) of the body of the request
        :type content_type: RequestConstants
        :return: Response to Server V1 end game session request
        :rtype: Response
        :param client_ip: Client IP
        :type client_ip: str
        :param client_language: Client language
        :type client_language: str
        """

        return self.request(
            'server/api/v1/endGameSession'
        ).headers({
            'x-freya-server-api-key': self.api_key
        }).json({
            'header': {},
            'body': {
                'profile_id': profile_id,
                'session_type': session_type,
                'session_id': session_id,
                'client_ip': client_ip,
                'client_language': client_language
            }
        }).post(content_type)

    def validate_client_session(self, client_session, fingerprint=RequestConstants.Parameters.OPTIONAL,
                                content_type=RequestConstants.ContentTypes.JSON):
        """
        Retrieve profile ID from client token using Server V1 Gateway
        :param client_session: Client session token
        :type client_session: str
        :param fingerprint: Client session fingerprint
        :type fingerprint: str
        :param content_type: Define content type (JSON or MSGPACK) of the body of the request
        :type content_type: RequestConstants
        :return: Response to Server V1 validate client session request
        :rtype: Response
        """

        return self.request(
            'server/api/v1/validateClientSession'
        ).headers({
            'x-freya-server-api-key': self.api_key
        }).json({
            'header': {},
            'body': {
                'client_session': client_session,
                'fingerprint': fingerprint
            }
        }).post(content_type)

    def get_full_inventory_from_session(self, client_session, content_type=RequestConstants.ContentTypes.JSON):
        """
        Retrieve inventory from client token session using Server V1 Gateway
        :param client_session: Client session token
        :type client_session: str
        :param content_type: Define content type (JSON or MSGPACK) of the body of the request
        :type content_type: RequestConstants
        :return: Response to Server V1 get full inventory from session request
        :rtype: Response
        """

        return self.request(
            'server/api/v1/getFullInventoryFromSession'
        ).headers({
            'x-freya-server-api-key': self.api_key
        }).json({
            'header': {},
            'body': {
                'client_session': client_session
            }
        }).post(content_type)

    def report_user(
            self,
            reporter_id,
            reportee_id=RequestConstants.Parameters.OPTIONAL,
            comment=RequestConstants.Parameters.OPTIONAL,
            content_type=RequestConstants.ContentTypes.JSON):
        """
        Report user using Server V1 Gateway
        :param reporter_id: Profile ID of reporter
        :type reporter_id: int
        :param reportee_id: Profile ID being reported
        :type reportee_id: int
        :param comment: Comment(s) associated with the report
        :type comment: str
        :param content_type: Define content type (JSON or MSGPACK) of the body of the request
        :type content_type: RequestConstants
        :return: Response to Server V1 report user request
        :rtype: Response
        """

        return self.request(
            'server/api/vi/reportUser'
        ).headers({
            'x-freya-server-api-key': self.api_key
        }).json({
            'header': {},
            'body': {
                'reporter_id': reporter_id,
                'reportee_id': reportee_id,
                'comment': comment
            }
        }).post(content_type)

    def get_child_profile_by_name(self, root_profile_id, profile_name, content_type=RequestConstants.ContentTypes.JSON):
        """
        Retrieve child profile information using Server V1 Gateway
        :param root_profile_id: Profile ID
        :type root_profile_id: int
        :param profile_name: Profile name
        :type profile_name: str
        :param content_type: Define content type (JSON or MSGPACK) of the body of the request
        :type content_type: RequestConstants
        :return: Response to Server V1 get child profile by name request
        :rtype: Response
        """

        return self.request(
            'server/api/v1/getChildProfileByName'
        ).headers({
            'x-freya-server-api-key': self.api_key
        }).json({
            'header': {},
            'body': {
                'root_profile_id': root_profile_id,
                'profile_name': profile_name
            }
        }).post(content_type)

    def fetch_categories(self, storefront,
                         language=RequestConstants.Parameters.OPTIONAL,
                         content_type=RequestConstants.ContentTypes.JSON,
                         periods=RequestConstants.Parameters.OPTIONAL):
        """
        Retrieve categories in a storefront using Server V1 Gateway
        :param storefront: Storefront to retrieve category(ies)
        :type storefront: str
        :param language: Language in Locate Format https://tools.ietf.org/html/bcp47
        :type language: str
        :param content_type: Define content type (JSON or MSGPACK) of the body of the request
        :type content_type: RequestConstants
        :return: Response to Server V1 fetch categories request
        :rtype: Response
        :param periods: filter param ('PAST', 'PRESENT', 'FUTURE')
        :type periods: list
        """
        return self.request(
            'server/api/v1/fetchCategories'
        ).headers({
            'x-freya-server-api-key': self.api_key
        }).json({
            'header': {},
            'body': {
                'storefront': storefront,
                'language': language,
                'periods': periods
            }
        }).post(content_type)

    def contract_call(self,
                      schema,
                      contract_id,
                      freya_api_key=None):
        """
        call contract from gapi
        :param schema: Contract data
        :type schema: object
        :param freya_api_key: freya server api key
        :type freya_api_key: str
        :param contract_id: Contract id
        :type contract_id: str
        """
        return self.request('server/api/v1/call/{contract_id}'.format(contract_id=contract_id)).headers({
            'x-freya-server-api-key': freya_api_key or self.api_key
        }).json(schema).post()
