import json


class InventoryUtilities(object):

    @staticmethod
    def get_all_entitlements(inventory):
        """
        gets all the entitlements from a profile including those of the sub profiles

        :return: :list: ToolsEntitlementInfo
        """

        children_queue = list(inventory['children'])
        all_entitlements = list(inventory['entitlements'])

        while len(children_queue) > 0:
            child = children_queue.pop()
            for sub_profile in child['children']:
                children_queue.extend(sub_profile['children'])
            all_entitlements.extend(child['entitlements'])

        return all_entitlements

    @staticmethod
    def inventory_has(server_gateway, log, profile_id, to_check_currencies, to_check_entitlements):
        """
        :param server_gateway:
        :param log:
        :param profile_id:
        :param to_check_currencies:
        :param to_check_entitlements:
        :return:
        """

        inventory_response = server_gateway.get_full_inventory(profile_id)
        if not inventory_response.success:
            return False
        inventory = inventory_response.content['body']['profile']
        log.info('profile {} full inventory: {}'.format(profile_id, json.dumps(inventory, indent=2)))

        for code, amount in to_check_currencies.iteritems():

            currency = next((currency for currency in inventory['currencies'] if currency['code'] == code), None)

            if currency is None or int(currency['amount']) != int(amount):
                found_code = currency['code'] if currency else None
                found_amount = currency['amount'] if currency else None
                log.info('looking for {} {} instead found {} {}'.format(code, amount, found_code, found_amount))
                return False

        for code, amount in to_check_entitlements.iteritems():

            entitlement = next(
                (entitlement for entitlement in inventory['entitlements'] if entitlement['code'] == code), None)

            if entitlement is None or int(entitlement['amount']) != amount:
                found_code = entitlement['code'] if entitlement else None
                found_amount = entitlement['amount'] if entitlement else None
                log.info('looking for {} {} instead found {} {}'.format(code, amount, found_code, found_amount))
                return False

        return True

    @staticmethod
    def inventory_empty(server_gateway, log, profile_id, check_currencies, check_entitlements):
        """

        :param server_gateway:
        :param log:
        :param profile_id:
        :param check_currencies:
        :param check_entitlements:
        :return:
        """

        inventory_response = server_gateway.get_full_inventory(profile_id)
        if not inventory_response.success:
            return False
        inventory = inventory_response.content['body']['profile']
        log.info('profile {} full inventory: {}'.format(profile_id, json.dumps(inventory, indent=2)))

        if check_currencies and inventory['currencies']:
            return False

        if check_entitlements and inventory['entitlements']:
            return False

        return True
