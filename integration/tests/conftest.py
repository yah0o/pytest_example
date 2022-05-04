import pytest

import setup
from integration.main.helpers.pytest_utils import skip_regions_marker
from integration.main.services.tools import AdminLoginStore
from integration.main.session import ConfigAdapter


def pytest_addoption(parser):
    parser.addoption('--env', action='store', help='the environment file session')
    parser.addoption('--skip_pub', action='store', help='skips catalog publish before suite. Set to anything to skip')
    parser.addoption('--threaded', action='store', help='if threaded, this will skips catalog publish before suite')
    parser.addoption('--username', action='store', help='tools admin username (login)')
    parser.addoption('--password', action='store', help='tools admin password')
    parser.addoption('--pin', action='store', help='tools admin pin. Necessary for OTP')
    parser.addoption('--secret_key', action='store', help='tools admin secret key. Necessary for OTP')
    parser.addoption('--env_color', action='store', help='environment color (blue/green)')
    parser.addoption('--name', action='store', help='tools admin name')


@pytest.fixture(scope='session')
def config(request):
    environment_file_name = request.config.getoption('--env')
    username = request.config.getoption('--username')
    password = request.config.getoption('--password')
    pin = request.config.getoption('--pin')
    secret_key = request.config.getoption('--secret_key')
    skip_publish = request.config.getoption('--skip_pub')
    env_color = request.config.getoption('--env_color')
    name = request.config.getoption('--name')

    config_adapter = ConfigAdapter(environment_file_name, username, password, pin, secret_key, env_color, name)

   # if skip_publish is None:
        #        setup.setup_title_relationships_and_configurations(config_adapter)
        #      setup.import_and_publish_catalog(config_adapter)

    return config_adapter


NUM_RETRIES = 5


@pytest.fixture(autouse=True)
def adapter_store_reset(config):
    """
    Reset all stored configurations
    :param config: Configuration of test run session
    :type config: ConfigAdapter
    """

    config.reset_store()

    persist_store = AdminLoginStore()

    if persist_store.has_failed:
        pytest.exit("Exiting due to too many login failures")

    if persist_store.failed_attempts > NUM_RETRIES:
        persist_store.has_failed = True
        pytest.fail("Login Failed. Further login attempts could cause the account lock up.")


@pytest.fixture(autouse=True)
def regions_only(request, config):
    skip_regions_marker(request, config, 'regions_only')


@pytest.fixture(autouse=True)
def skip_for_regions(request, config):
    skip_regions_marker(request, config, 'skip_for_regions', include=False)
