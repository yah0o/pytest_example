import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities
from integration.main.request import RequestBuilder
from integration.schemas import Schemas


@pytest.allure.feature('functional')
@pytest.allure.story('check product metadata')
class TestMetadata(object):

    @pytest.fixture(autouse=True)
    def setup(self, config):
        ###
        # Test setup
        config.store.account = AccountUtilities.create_account(attrs='user_stated_country=ZZ')

        account_created = config.spa.http.create_account(config.store.account.__dict__)
        account_created.assert_is_success()
        update_account = config.spa.http.update(account_created.content['id'],
                                                game=config.environment['test_title_pgn'])
        update_account.assert_is_success()

        config.store.wgid = account_created.content['id']

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here
        delete_response = config.spa.http.delete_account(config.store.wgid)
        delete_response.assert_is_success()

    @pytest.allure.severity(severity_level.NORMAL)
    def test_fetch_product_check_basic_metadata_schema(self, config):
        """
        Fetches info about a product with basic metadata, and checks it against a defined schema.
        """
        product_codes = [config.data.TEST_PRODUCT_BASIC_METADATA.PRODUCT_CODE]
        language = config.data.TEST_PRODUCT_BASIC_METADATA.LANGUAGE
        country = config.data.TEST_PRODUCT_BASIC_METADATA.COUNTRY

        fetch_response = config.freya.server_gateway.fetch_products(product_codes, config.store.wgid, country, language)
        fetch_response.assert_is_success()

        product_urls = fetch_response.content['body']['uriList']
        assert_that(product_urls, has_length(1))
        uri = product_urls[0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        config.log.info("Checking that basic metadata is displayed according to schema.")
        assert_that(product_response.content["metadata"], not_none())
        Schemas.validate(product_response.content["metadata"], Schemas.BASIC_METADATA)

    @pytest.allure.severity(severity_level.NORMAL)
    def test_fetch_product_check_localized_metadata_schema(self, config):
        """
        Fetches info about a product with localizable metadata, and checks it against a defined schema.
        """
        product_codes = [config.data.TEST_PRODUCT_LOCALIZABLE_METADATA.PRODUCT_CODE]
        language = config.data.TEST_PRODUCT_LOCALIZABLE_METADATA.INCLUDED_LANGUAGE
        country = config.data.TEST_PRODUCT_LOCALIZABLE_METADATA.COUNTRY

        fetch_response = config.freya.server_gateway.fetch_products(product_codes, config.store.wgid, country, language)
        fetch_response.assert_is_success()

        product_urls = fetch_response.content['body']['uriList']
        assert_that(product_urls, has_length(1))
        uri = product_urls[0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        config.log.info("Checking metadata localized using '{}' against schema.".format(language))
        assert_that(product_response.content["metadata"], not_none())
        Schemas.validate(product_response.content["metadata"], Schemas.LOCALIZED_METADATA)

    @pytest.allure.severity(severity_level.NORMAL)
    def test_fetch_product_localize_metadata_using_present_language(self, config):
        """
        Attempts to localize and check a product's metadata using a language key that is present in it.
        """
        product_codes = [config.data.TEST_PRODUCT_LOCALIZABLE_METADATA.PRODUCT_CODE]
        language = config.data.TEST_PRODUCT_LOCALIZABLE_METADATA.INCLUDED_LANGUAGE
        country = config.data.TEST_PRODUCT_LOCALIZABLE_METADATA.COUNTRY

        expected_value = config.data.TEST_PRODUCT_LOCALIZABLE_METADATA.METADATA_LANGUAGE_VALUE

        fetch_response = config.freya.server_gateway.fetch_products(product_codes, config.store.wgid, country, language)
        fetch_response.assert_is_success()

        product_urls = fetch_response.content['body']['uriList']
        assert_that(product_urls, has_length(1))
        uri = product_urls[0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        config.log.info("Checking that metadata was properly localized using present language '{}'.".format(language))
        assert_that(product_response.content["metadata"], not_none())

        # check LocString localization
        assert_that(product_response.content["metadata"]["wgpm"]["some_locstring"]["data"][language],
                    equal_to(expected_value))
        assert_that(product_response.content["metadata"]["wgpm"]["some_locstring"]["data"]["value"],
                    equal_to(expected_value))

        # check LocMedia localization
        assert_that(product_response.content["metadata"]["wgpm"]["some_loc_media"]["data"]["text"][language],
                    equal_to(expected_value))
        assert_that(product_response.content["metadata"]["wgpm"]["some_loc_media"]["data"]["text"]["value"],
                    equal_to(expected_value))

        assert_that(product_response.content["metadata"]["wgpm"]["some_loc_media"]["data"]["url"][language],
                    equal_to(expected_value))
        assert_that(product_response.content["metadata"]["wgpm"]["some_loc_media"]["data"]["url"]["value"],
                    equal_to(expected_value))

        assert_that(product_response.content["metadata"]["wgpm"]["some_loc_media"]["data"]["preview_url"][language],
                    equal_to(expected_value))
        assert_that(product_response.content["metadata"]["wgpm"]["some_loc_media"]["data"]["preview_url"]["value"],
                    equal_to(expected_value))

        # check localization of first item of a LocMediaList
        assert_that(product_response.content["metadata"]["wgpm"]["some_loc_media_list"]["data"][0]["text"][language],
                    equal_to(expected_value))
        assert_that(product_response.content["metadata"]["wgpm"]["some_loc_media_list"]["data"][0]["text"]["value"],
                    equal_to(expected_value))

        assert_that(product_response.content["metadata"]["wgpm"]["some_loc_media_list"]["data"][0]["url"][language],
                    equal_to(expected_value))
        assert_that(product_response.content["metadata"]["wgpm"]["some_loc_media_list"]["data"][0]["url"]["value"],
                    equal_to(expected_value))

        assert_that(
            product_response.content["metadata"]["wgpm"]["some_loc_media_list"]["data"][0]["preview_url"][language],
            equal_to(expected_value))
        assert_that(
            product_response.content["metadata"]["wgpm"]["some_loc_media_list"]["data"][0]["preview_url"]["value"],
            equal_to(expected_value))

    @pytest.mark.skip_for_regions('wgt1')
    @pytest.allure.severity(severity_level.NORMAL)
    def test_fetch_product_localize_metadata_using_hyphenated_language(self, config):
        """
        If user requests metadata be localized using 'en-xx' and it is not present,
        check that it defaults to 'en' instead.
        """
        product_codes = [config.data.TEST_PRODUCT_LOCALIZABLE_METADATA.PRODUCT_CODE]
        language = config.data.TEST_PRODUCT_LOCALIZABLE_METADATA.HYPHENATED_LANGUAGE
        country = config.data.TEST_PRODUCT_LOCALIZABLE_METADATA.COUNTRY

        expected_value = config.data.TEST_PRODUCT_LOCALIZABLE_METADATA.METADATA_LANGUAGE_VALUE

        fetch_response = config.freya.server_gateway.fetch_products(product_codes, config.store.wgid, country, language)
        fetch_response.assert_is_success()

        product_urls = fetch_response.content['body']['uriList']
        assert_that(product_urls, has_length(1))
        uri = product_urls[0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        config.log.info(
            "Checking that if '{}' was requested, metadata was localized using values stored for '{}' instead.".format(
                language, language.split("-")[0]))
        assert_that(product_response.content["metadata"], not_none())

        # check LocString localization
        assert_that(product_response.content["metadata"]["wgpm"]["some_locstring"]["data"][language],
                    equal_to(expected_value))
        assert_that(product_response.content["metadata"]["wgpm"]["some_locstring"]["data"]["value"],
                    equal_to(expected_value))

        # check LocMedia localization
        assert_that(product_response.content["metadata"]["wgpm"]["some_loc_media"]["data"]["text"][language],
                    equal_to(expected_value))
        assert_that(product_response.content["metadata"]["wgpm"]["some_loc_media"]["data"]["text"]["value"],
                    equal_to(expected_value))

        assert_that(product_response.content["metadata"]["wgpm"]["some_loc_media"]["data"]["url"][language],
                    equal_to(expected_value))
        assert_that(product_response.content["metadata"]["wgpm"]["some_loc_media"]["data"]["url"]["value"],
                    equal_to(expected_value))

        assert_that(product_response.content["metadata"]["wgpm"]["some_loc_media"]["data"]["preview_url"][language],
                    equal_to(expected_value))
        assert_that(product_response.content["metadata"]["wgpm"]["some_loc_media"]["data"]["preview_url"]["value"],
                    equal_to(expected_value))

        # check localization of first item of a LocStringList
        assert_that(product_response.content["metadata"]["wgpm"]["some_loc_string_list"]["data"][0][language],
                    equal_to('some_englih'))
        assert_that(product_response.content["metadata"]["wgpm"]["some_loc_string_list"]["data"][0]["value"],
                    equal_to('some_englih'))

        # check localization of first item of a LocMediaList
        assert_that(product_response.content["metadata"]["wgpm"]["some_loc_media_list"]["data"][0]["text"][language],
                    equal_to(expected_value))
        assert_that(product_response.content["metadata"]["wgpm"]["some_loc_media_list"]["data"][0]["text"]["value"],
                    equal_to(expected_value))

        assert_that(product_response.content["metadata"]["wgpm"]["some_loc_media_list"]["data"][0]["url"][language],
                    equal_to(expected_value))
        assert_that(product_response.content["metadata"]["wgpm"]["some_loc_media_list"]["data"][0]["url"]["value"],
                    equal_to(expected_value))

        assert_that(
            product_response.content["metadata"]["wgpm"]["some_loc_media_list"]["data"][0]["preview_url"][language],
            equal_to(expected_value))
        assert_that(
            product_response.content["metadata"]["wgpm"]["some_loc_media_list"]["data"][0]["preview_url"]["value"],
            equal_to(expected_value))

    @pytest.mark.skip_for_regions('wgt1')
    @pytest.allure.severity(severity_level.NORMAL)
    def test_fetch_product_localize_metadata_using_nonexistent_language(self, config):
        """
        If user requests metadata be localized using a non-existent language,
        checks that it defaults to value of "value" key instead.
        """
        product_codes = [config.data.TEST_PRODUCT_LOCALIZABLE_METADATA.PRODUCT_CODE]
        language = config.data.TEST_PRODUCT_LOCALIZABLE_METADATA.NONEXISTENT_LANGUAGE
        country = config.data.TEST_PRODUCT_LOCALIZABLE_METADATA.COUNTRY

        expected_value = config.data.TEST_PRODUCT_LOCALIZABLE_METADATA.METADATA_DEFAULT_VALUE

        fetch_response = config.freya.server_gateway.fetch_products(product_codes, config.store.wgid, country, language)
        fetch_response.assert_is_success()

        product_urls = fetch_response.content['body']['uriList']
        assert_that(product_urls, has_length(1))
        uri = product_urls[0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        language = config.data.TEST_PRODUCT_LOCALIZABLE_METADATA.NONEXISTENT_LANGUAGE
        config.log.info(
            "Checking that if nonexistent '{}' was requested, "
            "metadata was localized using values for 'value' key instead.".format(
                language))
        assert_that(product_response.content["metadata"], not_none())

        # check LocString localization
        assert_that(product_response.content["metadata"]["wgpm"]["some_locstring"]["data"][language],
                    equal_to('some_english'))
        assert_that(product_response.content["metadata"]["wgpm"]["some_locstring"]["data"]["value"],
                    equal_to('some_english'))

        # check LocMedia localization
        assert_that(product_response.content["metadata"]["wgpm"]["some_loc_media"]["data"]["text"][language],
                    equal_to(expected_value))
        assert_that(product_response.content["metadata"]["wgpm"]["some_loc_media"]["data"]["text"]["value"],
                    equal_to(expected_value))

        assert_that(product_response.content["metadata"]["wgpm"]["some_loc_media"]["data"]["url"][language],
                    equal_to(expected_value))
        assert_that(product_response.content["metadata"]["wgpm"]["some_loc_media"]["data"]["url"]["value"],
                    equal_to(expected_value))

        assert_that(product_response.content["metadata"]["wgpm"]["some_loc_media"]["data"]["preview_url"][language],
                    equal_to(expected_value))
        assert_that(product_response.content["metadata"]["wgpm"]["some_loc_media"]["data"]["preview_url"]["value"],
                    equal_to(expected_value))

        # check localization of first item of a LocStringList
        assert_that(product_response.content["metadata"]["wgpm"]["some_loc_string_list"]["data"][0][language],
                    equal_to('some_englih'))
        assert_that(product_response.content["metadata"]["wgpm"]["some_loc_string_list"]["data"][0]["value"],
                    equal_to('some_englih'))

        # check localization of first item of a LocMediaList
        assert_that(product_response.content["metadata"]["wgpm"]["some_loc_media_list"]["data"][0]["text"][language],
                    equal_to(expected_value))
        assert_that(product_response.content["metadata"]["wgpm"]["some_loc_media_list"]["data"][0]["text"]["value"],
                    equal_to(expected_value))

        assert_that(product_response.content["metadata"]["wgpm"]["some_loc_media_list"]["data"][0]["url"][language],
                    equal_to(expected_value))
        assert_that(product_response.content["metadata"]["wgpm"]["some_loc_media_list"]["data"][0]["url"]["value"],
                    equal_to(expected_value))

        assert_that(
            product_response.content["metadata"]["wgpm"]["some_loc_media_list"]["data"][0]["preview_url"][language],
            equal_to(expected_value))
        assert_that(
            product_response.content["metadata"]["wgpm"]["some_loc_media_list"]["data"][0]["preview_url"]["value"],
            equal_to(expected_value))
