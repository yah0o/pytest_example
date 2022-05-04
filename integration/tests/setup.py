import argparse
import codecs
import os
import time

from hamcrest import *

from integration.main.helpers import WaitOn, ReturnValue, DummyServer
from integration.main.session import ConfigAdapter


def import_and_publish_catalog(config):
    contains_catalog = False
    for k, v in config.data:
        if k == 'CATALOG':
            contains_catalog = True
            break

    if not contains_catalog:
        config.log.info('No catalog found to import and publish')
        return

    waiter = WaitOn(
        lambda: config.freya.tools_gateway.login.auth_login_password(config.admin.username, config.admin.password).success
    ).until(ReturnValue.EQUAL_TO(True), 30)

    waiter.wait(message='could not log into tools admin {}'.format(
        config.freya.tools_gateway.login.auth_login_password(config.admin.username, config.admin.password).details
    ))

    config.log.info('SETUP Import and publish np.integration')
    path, catalog_file = os.path.split(config.data.path)
    nptest_catalog_path = os.path.abspath(os.path.join(path, config.data.CATALOG))

    config.log.info('SETUP import np.integration\'s catalog json')

    no_access_pgn = config.environment['no_access_1_title'].split('.')[1]

    with open(nptest_catalog_path) as catalog_file:
        with open('temp_catalog.json', 'w') as temp_catalog:
            for line in catalog_file:
                if '<TITLE_CODE>' in line:
                    temp_catalog.write(line.replace('<TITLE_CODE>', config.environment['integration_title']))
                elif '<NO_ACCESS_1>' in line:
                    temp_catalog.write(line.replace('<NO_ACCESS_1>', no_access_pgn))
                else:
                    temp_catalog.write(line)
    temp_catalog_path = os.path.abspath('temp_catalog.json')

    import_response = config.freya.tools_gateway.working_catalog.import_catalog(
        config.environment['integration_title'],
        config.data.TEST_TITLE_BRANCH,
        temp_catalog_path,
        True
    )
    import_response.assert_is_success()
    assert_that(import_response.content['num_entities_imported'], greater_than(0))

    config.log.info("getting title versions")
    title_response = config.freya.tools_gateway.title.get_title(config.environment['integration_title'])
    title_response.assert_is_success()

    assert_that(title_response.content['title_versions'], has_length(greater_than(0)))
    title_version_ids = [version['id'] for version in title_response.content['title_versions']]

    config.log.info("skip publish np.integration")
    # publish_response = config.freya.tools_gateway.publish_catalog.publish_working_catalog(
    #     config.environment['integration_title'],
    #     config.data.TEST_TITLE_BRANCH,
    #     title_version_ids,
    #     int(time.time())
    # )
    # publish_response.assert_is_success()


def setup_title_relationships_and_configurations(config):
    """
    Two titles will be used for cross-title tests:
        np.tartest is the title containing all the products and entitlements
        np.test only contains the storefront with external references to <base_title's> products

    Their title info must also must be configured a certain way.
    np.test needs to have:

        "shared_titles": [ <np.tartest's title id, type long> ]

    The long is currently used to retrieve a title's namespace, in order to process a user's entitlement prerequisites.

    and np.tartest needs to have:

        "title_permissions": {
            "catalog": {
                "np.test": {
                    "visible_tags": [
                        "some_cross_title_tag"
                    ]
                }
            }
        }

    "some_cross_title_tag" must also be present in a product's "title_visibility_tags" list, in order for that product
     to be viewable through a storefront in np.test;

    """
    if 'v2' in config.environment['title']:
        config.log.info('No title relationships needed for v2 tests')
        return

    waiter = WaitOn(
        lambda: config.freya.tools_gateway.login.auth_login_password(config.admin.username, config.admin.password).success
    ).until(ReturnValue.EQUAL_TO(True), 30)

    waiter.wait(message='could not log into tools admin {}'.format(
        config.freya.tools_gateway.login.auth_login_password(config.admin.username, config.admin.password).details
    ))

    test_title_name = config.environment['integration_title']

    title_info_response = config.freya.tools_gateway.title.get_title(test_title_name)
    title_info_response.assert_is_success()

    test_title_info = title_info_response.content

    publish_test_title = False

    init_version = next((version for version in test_title_info['title_versions'] if version['active']), None)
    assert init_version, '{} does not have an active title version. This needs to be fixed before tests can run.'.format(
        test_title_name)

    if 'blocker' in config.environment['title']:
        config.log.info('Getting sharred currency title')
        if config.environment['shared_currency'] is None:
            publish_test_title = True
        else:
            shared_currency_info_response = config.freya.tools_gateway.title.get_title(
                config.environment['shared_currency']
            )
            shared_currency_info_response.assert_is_success()
            shared_currency_title_id = int(shared_currency_info_response.content['id'])
            if shared_currency_title_id not in test_title_info['shared_titles']:
                test_title_info['shared_titles'].append(shared_currency_title_id)
                publish_test_title = True

        shared_entitlement_info_response = config.freya.tools_gateway.title.get_title(
            config.environment['shared_entitlement']
        )
        shared_entitlement_info_response.assert_is_success()

        shared_entitlement_title_info = shared_entitlement_info_response.content
        shared_entitlement_title_id = int(shared_entitlement_title_info['id'])

        if shared_entitlement_title_id not in test_title_info['shared_titles']:
            test_title_info['shared_titles'].append(shared_entitlement_title_id)
            publish_test_title = True

    if 'starting_inventory_code' in init_version and init_version['starting_inventory_code'] != '':
        init_version['starting_inventory_code'] = ''
        publish_test_title = True

    schema_key = '{}.schema'.format(test_title_name)

    if schema_key not in test_title_info['document_schemas']:
        test_title_info['document_schemas'][schema_key] = [{
            "name": schema_key,
            "schema": "{\"type\": [\"object\", \"array\", \"string\",\"number\",\"boolean\",\"null\"]}",
            "version": 0
        }]
        publish_test_title = False

    # Publish set to False cause of Tools25 incorrect schema - delete code after set down webhooks
    if 'webhook_endpoint' not in test_title_info:
        test_title_info['webhook_endpoint'] = DummyServer.get_webhook_url(config.environment.environment_name)
        publish_test_title = False

    if test_title_info['webhook_endpoint'] != DummyServer.get_webhook_url(config.environment.environment_name):
        test_title_info['webhook_endpoint'] = DummyServer.get_webhook_url(config.environment.environment_name)
        publish_test_title = False

    if 'ggapi_discovery' not in test_title_info:
        test_title_info['ggapi_discovery'] = config.data.GG_DISCOVERY
        publish_test_title = False

    if 'ggapi_method' not in test_title_info:
        test_title_info['ggapi_method'] = config.data.GG_METHOD
        publish_test_title = False

    if 'GG_METHOD' in config.data and test_title_info['ggapi_method'] != config.data.GG_METHOD:
        test_title_info['ggapi_method'] = config.data.GG_METHOD
        publish_test_title = False

    if 'title_permissions' in test_title_info:
        if 'client_api' in test_title_info['title_permissions']:
            if 'api_list' in test_title_info['title_permissions']['client_api']:
                if test_title_info['title_permissions']['client_api']['api_list']:
                    test_title_info['title_permissions']['client_api']['api_list'] = []
                    publish_test_title = True

    if 'reason' not in test_title_info:
        test_title_info['reason'] = 'To run integration tests PLAT-3109'
        publish_test_title = False

    if publish_test_title:
        config.log.info('Update and publish test title:')

        update_test_title = config.freya.title_config.publish_titles_v2_with_data(test_title_name, test_title_info)
        update_test_title.assert_is_success()

        title_info_response5 = config.freya.tools_gateway.title.get_title(test_title_name)
        title_info_response5.assert_is_success()

        assert_that(title_info_response.content['title_versions'], has_length(greater_than(0)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='setup test title')

    parser.add_argument('--env', required=True, action='store', help='the environment file session')
    parser.add_argument('--username', action='store', help='tools admin username')
    parser.add_argument('--password', action='store', help='tools admin password')
    parser.add_argument('--pin', action='store', help='tools admin pin. Necessary for OTP')
    parser.add_argument('--secret_key', action='store', help='tools admin secret key. Necessary for OTP')
    parser.add_argument('--name', action='store', help='tools admin name')

    args = parser.parse_args()

    env_file_name = args.environment
    username = args.username
    password = args.password
    pin = args.pin
    secret_key = args.secret_key
    name = args.name

    config_adapter = ConfigAdapter(env_file_name, username, password, pin, secret_key, name)

    setup_title_relationships_and_configurations(config_adapter)
    print ("SKIPPING publish np.integration - INTEGRATION WITH NEW TOOLS")
    # import_and_publish_catalog(config_adapter)
