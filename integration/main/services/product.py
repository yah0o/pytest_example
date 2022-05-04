from gateway import Gateway
from integration.main.request import RequestConstants


class ProductService(Gateway):

    def get_ces_data(
            self,
            message_id=RequestConstants.Parameters.OPTIONAL,
            content_type=RequestConstants.ContentTypes.JSON
    ):
        """
        Get current CES table being used by the service

        :param message_id: UUID4 identifier for the message
        :type message_id: str
        :param content_type: Content type to use when sending the request
        :type content_type: RequestConstants.ContentTypes
        :return: Response json returned from the request
        :rtype: :py:class: `Response`
        """

        return self.request(
            'product/api/v1/ces'
        ).headers({
            'Accept': content_type,
            'message_id': message_id
        }).get()
