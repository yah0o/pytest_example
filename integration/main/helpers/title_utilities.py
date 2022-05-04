import random
import uuid

from integration.main.helpers.utils import generate_unixtime_based_string


class TitleUtilities(object):

    @staticmethod
    def get_api_key(tools, title):
        """

        :param tools:
        :param title:
        :return:
        """

        get_title_response = tools.title.get_title(
            title
        )
        if not get_title_response.success:
            return None

        api_key = next(
            (
                title_version['server_api_key'] for title_version in get_title_response.content['title_versions']
                if title_version['default'] and title_version['active']
            ),
            None
        )

        return api_key


class TCSTitleEntities:
    # Params for title publish method in titleconfigservice
    reason = 'auto' + generate_unixtime_based_string()
    titleid = random.randint(0, 32767)  # TR full_title_id, 32767 - small int in postgres (affect SPA)
    title_id = random.randint(0, 32767)  # SPA Game ID
    friendly_name = reason  # Title friendly name
    pgn = reason  # Field for compatibility with legacy services. Example: WOT
    pop = 'ru'  # Region / realm name. Point of presence, primary data center for this game
    code = str(pop + '.' + pgn)
    namespace_id = random.randint(0, 32767)  # Title's title_id / game_id
    title_version_id = str(uuid.uuid4())
    server_api_key = str(uuid.uuid4())
    client_api_key = str(uuid.uuid4())


class TCSTitleEntitiesv2(TCSTitleEntities):
    # Params for title v2 publish method in titleconfigservice
    entity_type_id = 2  # Namespace entity type id. Currently allowed are 0 (players), 1 (clans), 2(titles).
    key = TCSTitleEntities.code + '.' + 'game'
    full_title_id = TCSTitleEntities.titleid
    namespace_title_id = TCSTitleEntities.title_id
    platfrom_config = {"game": {"bantypes": ["access_denied"]}}


class TCSSharedTitleEntitiesv2:
    # Params for title publish method in titleconfigservice
    reason = 'auto' + generate_unixtime_based_string()
    titleid = random.randint(0, 32767)  # TR full_title_id, 32767 - small int in postgres (affect SPA)
    title_id = random.randint(0, 32767)  # SPA Game ID
    friendly_name = reason  # Title friendly name
    pgn = 'shared_' + \
          generate_unixtime_based_string()  # Field for compatibility with legacy services. Example: WOT
    pop = 'ru'  # Region / realm name. Point of presence, primary data center for this game
    code = str(pop + '.' + pgn)
    namespace_id = random.randint(0, 32767)  # Title's title_id / game_id
    title_version_id = str(uuid.uuid4())
    server_api_key = str(uuid.uuid4())
    client_api_key = str(uuid.uuid4())
    entity_type_id = 2  # Namespace entity type id. Currently allowed are 0 (players), 1 (clans), 2(titles).
    key = code + '.' + 'game'
    full_title_id = random.randint(0, 32767)
    namespace_title_id = random.randint(0, 32767)
    title_type = "shared"
