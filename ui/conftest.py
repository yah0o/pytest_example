import os

import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.remote_connection import RemoteConnection
from selenium.webdriver.remote.webdriver import WebDriver

from ui.main.session import ConfigAdapter
from ui.steps import UISteps


def pytest_addoption(parser):
    parser.addoption('--env', action='store', help='the environment file session')
    parser.addoption('--username', action='store', default='admin', help='tools admin username')
    parser.addoption('--password', action='store', default='111111', help='tools admin password')
    parser.addoption('--pin', action='store', help='tools admin pin. Necessary for OTP')
    parser.addoption('--secret_key', action='store', help='tools admin secret key. Necessary for OTP')
    parser.addoption('--env_color', action='store', choices=['blue', 'green'], help='environment color (blue/green)')
    parser.addoption(
        '--browser',
        action='store',
        default='chrome',
        choices=['chrome', 'firefox', 'safari'],
        help='browser to use in testing'
    )
    parser.addoption(
        '--headless',
        action='store',
        default='True',
        choices=['True', 'False'],
        help='Run tests without UI (only Chrome and Firefox)'
    )
    parser.addoption('--remote', action='store', default='False', choices=['True', 'False'], help='Run tests remotely')


@pytest.fixture(scope='session')
def config(request):
    """
    Configuration element to store environment and test data
    :param request: parameters used when calling pytest
    :type request:
    :return: configuration element
    :rtype: ConfigAdapter
    """
    environment_file_name = request.config.getoption('--env')
    username = request.config.getoption('--username')
    password = request.config.getoption('--password')
    pin = request.config.getoption('--pin')
    secret_key = request.config.getoption('--secret_key')
    env_color = request.config.getoption('--env_color')

    config_adapter = ConfigAdapter(environment_file_name, username, password, pin, secret_key, env_color)

    return config_adapter


@pytest.fixture
def browser(request, config):
    """
    Initializes the WebDriver used by Selenium when running the tests
    :param request: parameters used when calling pytest
    :type request:
    :param config: configuration element
    :type config: ConfigAdapter
    :return: browser to run tests against
    :rtype: WebDriver
    """
    requested_browser = request.config.getoption('--browser')
    headless = request.config.getoption('--headless') == 'True'
    remote = request.config.getoption('--remote') == 'True'

    download_dir = os.getcwd()
    config.store.headless = headless
    config.store.browser_name = requested_browser

    browser = None
    if remote:
        # Use http://selenoid.ptf.wtp.iv/#/ to see tests running if remote command executor is
        # http://selenoid-bck.ptf.wtp.iv/wd/hub

        capabilities = {
            'browserName': requested_browser,
            'enableVNC': True,
            'enableVideo': False,
            'name': request.node.name
        }
        browser = webdriver.Remote(
            command_executor=RemoteConnection('http://selenoid-bck.ptf.wtp.iv/wd/hub', resolve_ip=False),
            desired_capabilities=capabilities
        )
    elif requested_browser == 'chrome':
        options = webdriver.ChromeOptions()
        if headless:
            options.headless = headless
            options.add_argument('disable-gpu')
        options.add_argument('log-level=3')  # disable info and errors, keep fatal errors
        prefs = {
            'download.default_directory': download_dir,
            'download.prompt_for_download': False,
            'download.directory_upgrade': True,
            'safebrowsing.enabled': False,
            'safebrowsing.disable_download_protection': True
        }
        options.add_experimental_option('prefs', prefs)
        browser = webdriver.Chrome(options=options)
        browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        params = {
            'cmd': 'Page.setDownloadBehavior',
            'params': {
                'behavior': 'allow',
                'downloadPath': download_dir
            }
        }
        browser.execute("send_command", params)
    elif requested_browser == 'firefox':
        options = Options()
        options.headless = headless
        fp = webdriver.FirefoxProfile()
        fp.set_preference('browser.download.manager.showWhenStarting', False)
        fp.set_preference('browser.download.manager.showAlertOnComplete', False)
        fp.set_preference('browser.helperApps.neverAsk.saveToDisk', 'json')
        fp.set_preference('browser.download.dir', download_dir)
        browser = webdriver.Firefox(options=options, firefox_profile=fp)
    elif requested_browser == 'safari':
        config.log.info('Headless execution not supported by Safari')
        browser = webdriver.Safari()
    else:
        config.log.error('Requested browser not supported')
        exit(1)

    browser.set_window_size(1200, 800)
    browser.maximize_window()
    browser.get(config.environment['url'])

    yield browser

    browser.quit()


@pytest.fixture
def steps(browser):
    """
    All steps available to be used to build tests
    :param browser: browser to run tests against
    :type browser: WebDriver
    :return: Class containing all available steps
    :rtype: UISteps
    """
    return UISteps(browser)
