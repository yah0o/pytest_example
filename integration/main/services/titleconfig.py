from hamcrest import *

from gateway import Gateway
from integration.main.request import RequestConstants


class TitleConfigService(Gateway):
    """
    Title Config
    """

    def __init__(self, base_url, session):
        """
        :param base_url: 
        :param session: 
        """

        Gateway.__init__(self, base_url, session)

    def get_active_catalogs(self):
        """
        :return:
        """

        return self.request('titleconfig/api/v1/titles/active').get()

    def get_titles(self, title_id_or_code):
        # Get single title
        response = self.request('titleconfig/api/v1/titles/{0}'.format(title_id_or_code)).get()
        response.assert_is_success()
        return response.content['titles']

    def get_currencies_map(self):
        # Get currencies map
        response = self.request('titleconfig/titles/currencies/map').get()
        return response

    def get_all_titles(self):
        response = self.request('titleconfig/api/v1/titles/').get()
        return response

    def get_active_titles(self):
        response = self.request('titleconfig/api/v1/titles/active').get()
        return response

    def publish_titles_v2_with_data(self, title_code, title_dict_data):
        response = self.request('titleconfig/api/v2/titles/{}/'.format(title_code)).json(title_dict_data).put()
        return response

    def publish_titles_v2(self,
                          title_code,
                          titleid,
                          title_id,
                          friendly_name,
                          pgn,
                          pop,
                          key,
                          entity_type_id,
                          namespace_id,
                          title_type,
                          platform_config=RequestConstants.Parameters.OPTIONAL,
                          namespace_title_id=RequestConstants.Parameters.OPTIONAL,
                          full_title_id=RequestConstants.Parameters.OPTIONAL,
                          automatic_registration=RequestConstants.Parameters.OPTIONAL,
                          external_product_cdn=RequestConstants.Parameters.OPTIONAL,
                          access=RequestConstants.Parameters.OPTIONAL,
                          enforce_prerequisites=RequestConstants.Parameters.OPTIONAL,
                          public=RequestConstants.Parameters.OPTIONAL,
                          view_entitlement_code=RequestConstants.Parameters.OPTIONAL,
                          access_entitlement_code=RequestConstants.Parameters.OPTIONAL,
                          comment=RequestConstants.Parameters.OPTIONAL,
                          internal=RequestConstants.Parameters.OPTIONAL,
                          state=RequestConstants.Parameters.OPTIONAL
                          ):
        """
               Notify platform account has been created on game server using Server V1 Gateway
               :param title_code: title code
               :type title_code: int
               :param titleid: TR full_title_id.
               :type titleid: int
               :param title_id: SPA Game ID.
               :type title_id: int
               :param friendly_name: Title friendly name
               :type friendly_name: str
               :param pgn: Field for compatibility with legacy services. Example: WOT
               :type pgn: str
               :param pop: Region / realm name. Point of presence, primary data center for this game
               :type pop: str
               :param title_type: Type of title: ['game', 'shared']
               :type title_type: str
               :param key: Namespace name, e.g. ru.wot.players. Essentially this is title code + entity type name
               :type key: string pattern: [a-z]+[._a-z0-9]+
               :param entity_type_id: Namespace entity type id. Currently allowed are 0 (players), 1 (clans), 2(titles).
               :type entity_type_id: int
               :param namespace_id: Namespace ID. Generated based on title id (full_title_id) and namespace entity type
               :type namespace_id: int
               :param platform_config: platform config title
               :type platform_config: dict
               :param namespace_title_id: Namespace title ID
               :type namespace_title_id: int
               :param full_title_id: Namespace ID. Generated based on title id (full_title_id) and namespace entity type
               :type full_title_id: int
               :param automatic_registration: Does title want automatic SPA account registration on
               first login or does it manually call accountCreated?
               :type automatic_registration: bool
               :param external_product_cdn: May this title use the environment's
               external CDN for product inventory calls
               :type external_product_cdn: bool
               :param external_product_cdn: May this title use the environment's
               external CDN for product inventory calls
               :type external_product_cdn: bool
               :param access: Defines if the game is available for all users.
               :type access: bool
               :param enforce_prerequisites: Should prerequisites be checked for this title during purchase
               :type enforce_prerequisites: bool
               :param public: Indicates whether the game is for real players.
               :type public: bool
               :param view_entitlement_code: Entitlement required to see the title. [null] means everyone can view the title
               :type view_entitlement_code: str
               :param access_entitlement_code: Entitlement required to access the title. [null] means everyone can join the title
               :type access_entitlement_code: str
               :param comment: Arbitrary string for publisher to add comments or notes about the title
               :type comment: str
               :param state: Is the game active or inactive
               :type state: Is the game active or inactive
               :param internal: Is this an internal title or not
               :type internal: bool

               :return: Response to titleconfig api v2 publish title
               :rtype: Response
        """

        # Publish single title
        response = self.request('titleconfig/api/v2/titles/{}/'.format(title_code)).json({
            "id": titleid,
            "title_id": title_id,
            "friendly_name": friendly_name,
            "description": "auto test",
            "pgn": pgn,
            "pop": pop,
            "platform_config": platform_config,
            "namespaces": [
                {
                    "id": namespace_id,
                    "title_id": namespace_title_id,
                    "key": key,
                    "entity_type_id": entity_type_id,
                    "full_title_id": full_title_id
                }
            ],
            "type": title_type,
            'automatic_registration': automatic_registration,
            "external_product_cdn": external_product_cdn,
            "access": access,
            "enforce_prerequisites": enforce_prerequisites,
            "public": public,
            "view_entitlement_code": view_entitlement_code,
            "access_entitlement_code": access_entitlement_code,
            "comment": comment,
            "state": state,
            "internal": internal
        }).put()
        return response

    def get_version(self):
        response = self.request('version').get()
        return response
