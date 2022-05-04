from gateway import Gateway
from integration.main.request import RequestConstants


class InventoryService(object):
    """
    Inventory Service
    """

    def __init__(self, base_url, session):
        """
        :param base_url:
        """
        self.__v3 = InventoryServiceV3(base_url, session)

    @property
    def v3(self):
        return self.__v3


class InventoryServiceV3(Gateway):

    def reverse(
            self,
            namespace,
            root_external_id,
            message_id=RequestConstants.Parameters.OPTIONAL,
            tx_id_to_reverse=RequestConstants.Parameters.OPTIONAL,
            new_transaction_id=RequestConstants.Parameters.OPTIONAL,
            content_type=RequestConstants.ContentTypes.JSON):
        """
        Reverse (undo) the entitlement transaction

         :param namespace:
        namespace is from GAPI [titlecode].players = np.test.players
        :param root_external_id:
        root_external_id = root profile_id = WGID
        :param message_id:
        :param tx_id_to_reverse:
        :param new_transaction_id:
        :param content_type:
        :return: :py:class: `Response`
        """

        return self.request(
            'entitlement/api/v3/ns/{0}/root/{1}/reverse'.format(namespace, root_external_id)
        ).headers({
            'Content-Type': content_type,
            'Accept': RequestConstants.ContentTypes.JSON,
            'message_id': message_id
        }).json({
            'tx_id_to_reverse': tx_id_to_reverse,
            'new_transaction_id': new_transaction_id
        }).post(content_type)

    def rollback(
            self,
            namespace,
            root_external_id,
            external_id,
            transaction_id,
            message_id=RequestConstants.Parameters.OPTIONAL,
            content_type=RequestConstants.ContentTypes.JSON):
        """
        Rollback the entitlement transaction matching this namespace, external id, and transaction id

        :param namespace:
        namespace is from GAPI [titlecode].players = np.test.players
        :param root_external_id:
        root_external_id = root profile_id = WGID
        :param external_id:
        external_id = profile_id
        :param transaction_id:
        :param message_id:
        :param content_type:
        :return:
        """

        return self.request(
            'entitlement/api/v3/ns/{0}/root/{1}/{2}/rollback/{3}'.format(namespace, root_external_id, external_id,
                                                                         transaction_id)
        ).headers({
            'Content-Type': content_type,
            'Accept': RequestConstants.ContentTypes.JSON,
            'message_id': message_id
        }).json({}).post(content_type)

    def transaction_list(
            self,
            namespace,
            root_external_id,
            external_id,
            message_id=RequestConstants.Parameters.OPTIONAL,
            page=RequestConstants.Parameters.OPTIONAL,
            pageSize=RequestConstants.Parameters.OPTIONAL,
            includeStatus=RequestConstants.Parameters.OPTIONAL):
        """
        Gets the list of transactions this ID has created

        :param namespace:
        :param root_external_id:
        :param external_id:
        :param message_id:
        :param page:
        :param pageSize:
        :param includeStatus:
        :return: :py:class: `Response`
        """

        return self.request(
            'entitlement/api/v3/ns/{0}/root/{1}/{2}/transactions'.format(namespace, root_external_id, external_id)
        ).headers({
            'Content-Type': RequestConstants.ContentTypes.JSON,
            'Accept': RequestConstants.ContentTypes.JSON,
            'message_id': message_id
        }).params({
            'page': page,
            'pageSize': pageSize,
            'includeStatus': includeStatus
        }).get()

    def cancel(
            self,
            namespace,
            root_external_id,
            transaction_id,
            message_id=RequestConstants.Parameters.OPTIONAL,
            dry_run=False,
            content_type=RequestConstants.ContentTypes.JSON):
        """
        Cancel (undo) the entitlement transaction

       :param namespace:
        namespace is from GAPI [titlecode].players = np.test.players
        :param root_external_id:
        root_external_id = root profile_id = WGID
        :param transaction_id:
        :param message_id:
        :param dry_run:
        :param content_type:
        :return: :py:class: `Response`
        """

        return self.request(
            'entitlement/api/v3/ns/{0}/root/{1}/cancel/{2}'.format(namespace, root_external_id, transaction_id)
        ).headers({
            'Content-Type': content_type,
            'Accept': RequestConstants.ContentTypes.JSON,
            'message_id': message_id
        }).params({
            'dry-run': dry_run
        }).post(content_type)

    def grant(
            self,
            namespace,
            root_external_id,
            external_id,
            transaction_id,
            entitlement_code,
            title_code,
            catalog,
            amount,
            content_type=RequestConstants.ContentTypes.JSON):
        """
        Grant entitlement instance

        :param namespace:
        namespace is from GAPI [titlecode].players = np.test.players
        :param root_external_id:
        root_external_id = root profile_id = WGID
        :param external_id:
        external_id = profile_id
        :param transaction_id:
        :param entitlement_code:
        :param title_code:
        :param catalog:
        :param amount:
        :param content_type:
        :return: :py:class: `Response`
        """

        return self.request(
            'entitlement/api/v3/ns/{0}/root/{1}/{2}/grant/txn'.format(namespace, root_external_id, external_id)
        ).headers({
            'Content-Type': content_type,
            'Accept': RequestConstants.ContentTypes.JSON,
        }).json({
            'transaction_id': transaction_id,
            'entitlement_code': entitlement_code,
            'title_code': title_code,
            'catalog': catalog,
            'amount': amount
        }).post(content_type)
