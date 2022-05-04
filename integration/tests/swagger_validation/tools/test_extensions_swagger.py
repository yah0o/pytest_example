import pytest
from jsonschema import ValidationError

from integration.main.helpers import RandomUtilities, DummyServer
from integration.schemas import Schemas


class TestExtensionsSwagger(object):

    @pytest.fixture(autouse=True)
    def setup(self, config):

        ###
        # Test setup
        login_response = config.freya.tools_gateway.login.auth_adfs_login(config.admin.username, config.admin.password)
        login_response.assert_is_success()

        config.store.dummy_server = DummyServer(config.environment['dummy_server'])

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_extensions_call(self, config):

        # No schema
        pass

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_extensions_get(self, config):

        error = None

        extension_code = 'test_extn_{}'.format(RandomUtilities.create_unique_id())

        try:
            register_response = config.freya.tools_gateway.extension.register_extension(extension_code,
                                                                                        config.store.dummy_server.ip)
            register_response.assert_is_success()

            extension = config.freya.tools_gateway.extension.get_extension(config.data.TEST_EXTENSION.CODE)
            extension.assert_is_success()
            Schemas.swagger_validate(extension, '/api/v1/ext/registry/{ext_code}')
        except (ValidationError, AssertionError), argument:
            error = argument

        unregister_extension = config.freya.tools_gateway.extension.unregister_extension(extension_code)
        unregister_extension.assert_is_success()

        if error:
            pytest.fail(error)

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_extensions_getList(self, config):

        extension_list = config.freya.tools_gateway.extension.get_extension_list()
        extension_list.assert_is_success()
        Schemas.swagger_validate(extension_list, '/api/v1/ext/registry')

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_extensions_register(self, config):

        error = None

        extension_code = 'test_extn_{}'.format(RandomUtilities.create_unique_id())

        try:
            register_response = config.freya.tools_gateway.extension.register_extension(extension_code,
                                                                                        config.store.dummy_server.ip)
            register_response.assert_is_success()
            Schemas.swagger_validate(register_response, '/api/v1/ext/registry')
        except (ValidationError, AssertionError), argument:
            error = argument

        unregister_extension = config.freya.tools_gateway.extension.unregister_extension(extension_code)
        unregister_extension.assert_is_success()

        if error:
            pytest.fail(error)

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_extensions_unregister(self, config):

        # No schema
        pass

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_extensions_update(self, config):

        error = None

        get_extension = config.freya.tools_gateway.extension.get_extension(config.data.TEST_EXTENSION.CODE)
        get_extension.assert_is_success()

        code = get_extension.content['code'] if 'code' in get_extension.content else None
        friendly_name = get_extension.content['friendly_name'] if 'friendly_name' in get_extension.content else None
        api_base = get_extension.content['api_base'] if 'api_base' in get_extension.content else None
        name = get_extension.content['name'] if 'name' in get_extension.content else None
        location = get_extension.content['location'] if 'location' in get_extension.content else None
        owner = get_extension.content['owner'] if 'owner' in get_extension.content else None

        try:
            update_extension = config.freya.tools_gateway.extension.update_extension(
                config.data.TEST_EXTENSION.CODE,
                code=config.data.TEST_EXTENSION.CODE,
                api_base='{0}_1'.format(api_base)
            )
            update_extension.assert_is_success()
            Schemas.swagger_validate(update_extension, '/api/v1/ext/registry/{ext_code}')
        except (ValidationError, AssertionError), argument:
            error = argument

        update_extension = config.freya.tools_gateway.extension.update_extension(
            config.data.TEST_EXTENSION.CODE,
            code=code,
            api_base=api_base,
            friendly_name=friendly_name,
            location=location,
            owner=owner,
            name=name)
        update_extension.assert_is_success()

        if error:
            pytest.fail(error)
