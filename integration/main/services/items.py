import json

from integration.main.request import RequestConstants


class ItemBase(object):

    def __repr__(self):
        return str(self)

    def __str__(self):
        return json.dumps(self.as_json, sort_keys=True, indent=4, separators=(',', ': '))

    @property
    def as_json(self):
        properties = [n for n in dir(self) if not n.startswith('__') and not n.endswith('__') and not n == 'as_json']
        return {attribute: self.__getattribute__(attribute) for attribute in properties}


class LegacyCurrencyItem(ItemBase):

    def __init__(self, currency_code, amount, coupons=RequestConstants.Parameters.OPTIONAL):
        self.currency_code = currency_code
        self.amount = amount
        self.coupons = coupons


class LegacyProductItem(ItemBase):

    def __init__(self, product_code, amount, coupons=RequestConstants.Parameters.OPTIONAL):
        self.product_code = product_code
        self.amount = amount
        self.coupons = coupons


class PurchaseProductItem(ItemBase):

    def __init__(self, product_id, amount, coupons=RequestConstants.Parameters.OPTIONAL):
        self.product_id = product_id
        self.amount = amount
        self.coupons = coupons


class CurrencyItem(ItemBase):

    def __init__(self, currency_code, amount):
        self.code = currency_code
        self.amount = amount


class GoogleAnalyticsItem(ItemBase):

    def __init__(self, tid, cid):
        self.tid = tid
        self.cid = cid


class WalletItem(ItemBase):

    def __init__(self, profile_id, currency_code, amount):
        self.profile_id = profile_id
        self.currency_code = currency_code
        self.amount = str(amount)


class CommitPurchasePaymentData(ItemBase):

    def __init__(
            self,
            payment_amount=RequestConstants.Parameters.OPTIONAL,
            payment_code=RequestConstants.Parameters.OPTIONAL,
            payment_method=RequestConstants.Parameters.OPTIONAL):
        self.amount = payment_amount
        self.currency = payment_code
        self.payment_method = payment_method


class CommitPurchaseTwoFactorAuthInfo(ItemBase):

    def __init__(
            self,
            twofa_code=RequestConstants.Parameters.OPTIONAL,
            twofa_type=RequestConstants.Parameters.OPTIONAL):
        self.code = twofa_code
        self.type = twofa_type


class SteamItem(ItemBase):

    def __init__(self, steam_id, app_id):
        self.steam_id = steam_id
        self.app_id = app_id


class WinstoreItem(ItemBase):

    def __init__(self, winstore_id_key):
        self.winstore_id_key = winstore_id_key


class ExtCommitSteamItem(ItemBase):

    def __init__(self, order_id, app_id):
        self.order_id = order_id
        self.app_id = app_id