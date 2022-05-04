from logging import log


class CatalogUtilities(object):

    @staticmethod
    def compare_catalog_entities(original_catalog_entities, imported_catalog_entities, entity_types):

        """
        Comparison utility for 2 dictionaries with list of objects

        :param original_catalog_entities: Fetched catalog entities
        :type original_catalog_entities: list of dict
        :param imported_catalog_entities: Imported catalog entities
        :type imported_catalog_entities: list of dict
        :param entity_types: Determine which entity to compare [PRODUCT, ENTITLEMENT, CURRENCY, PROMOTION, OVERRIDE, STOREFRONT]
        :type entity_types: list
        :return: Boolean for each
        :rtype: bool
        """

        if len(entity_types) < 1:
            log.error('Must provided at least one entity type')
            return False

        matching = True
        if entity_types == ['ALL']:
            entities = ['product', 'entitlement', 'currency', 'storefront']

        else:
            entities = entity_types

        for entity_type in entities:
            for value in imported_catalog_entities[entity_type]:

                entity = next((entity for entity in original_catalog_entities[entity_type]
                               if entity['code'] == value['code']), None)
                if entity is None or entity != value:
                    found_value = entity if entity else None
                    log.info('looking for {} in {} instead found {}'.format(value, entity_type, found_value))
                    matching = False

        return matching
