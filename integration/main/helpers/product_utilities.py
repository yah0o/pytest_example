from integration.main.request import RequestBuilder


class ProductUtilities(object):

    @staticmethod
    def product_codes_from_uri_list(uri_list):
        """
        Retrieves products codes from URI list and appends them into a new list for comparison

        :param uri_list:
        :return:
        """

        uri_list_products = []
        for uri in uri_list:
            uri_response = RequestBuilder(uri).get()
            uri_response.assert_is_success()
            uri_list_products.append(uri_response.content['product_code'])
        return uri_list_products
