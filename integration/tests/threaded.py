import argparse
import json

from plan.plan import Plan

TEST_SETS = {
    'nps1': {
        'env_file': 'integration/environments/nps1.yaml',
        'username': None,
        'password': None,
        'marks': 'not notnps1safe',
    },
    'nps11': {
        'env_file': 'integration/environments/nps11.yaml',
        'username': None,
        'password': None,
        'marks': 'not notnps1safe',
    },
    'wgs11': {
        'env_file': 'integration/environments/wgs11.yaml',
        'username': None,
        'password': None,
        'marks': 'not notwgs11safe',
    },
    'wgie': {
        'env_file': 'integration/environments/wgie.yaml',
        'username': 'prn.t_dfederov',
        'pin': 3574,
        'secret_key': '4E4DHQTPMU7QL4NKHOJD3KJTVJL7FURX',
        'marks': 'not notpreprodsafe',
    },
    'prv': {
        'env_file': 'integration/environments/prv.yaml',
        'username': None,
        'password': None,
        'marks': 'not notprodsafe',
    },
    'ct': {
        'env_file': 'integration/environments/blocker/ct.yaml',
        'username': 'prn.t_dfederov',
        'pin': 3574,
        'secret_key': '4E4DHQTPMU7QL4NKHOJD3KJTVJL7FURX',
        'marks': 'not notprodsafe',
    },
    'sg2': {
        'env_file': 'integration/environments/asia.yaml',
        'username': 'prn.t_dfederov',
        'pin': 3574,
        'secret_key': '4E4DHQTPMU7QL4NKHOJD3KJTVJL7FURX',
        'marks': 'not notprodsafe',
    },
    'eu': {
        'env_file': 'integration/environments/eu.yaml',
        'username': 'prn.t_dfederov',
        'pin': 3574,
        'secret_key': '4E4DHQTPMU7QL4NKHOJD3KJTVJL7FURX',
        'marks': 'not notprodsafe',
    },
    'us': {
        'env_file': 'integration/environments/na.yaml',
        'username': 'prn.t_dfederov',
        'pin': 3574,
        'secret_key': '4E4DHQTPMU7QL4NKHOJD3KJTVJL7FURX',
        'marks': 'not notprodsafe',
    },
    'ru': {
        'env_file': 'integration/environments/ru.yaml',
        'username': 'prn.t_dfederov',
        'pin': 3574,
        'secret_key': '4E4DHQTPMU7QL4NKHOJD3KJTVJL7FURX',
        'marks': 'not notprodsafe',
    },
    'sgrd': {
        'env_file': 'integration/environments/sgrd.yaml',
        'username': None,
        'password': None,
        'marks': 'not notpreprodsafe and not notprodsafe and not notsgrdsafe',
    },
    'wgt1': {
        'env_file': 'integration/environments/wgt1.yaml',
        'username': None,
        'password': None,
        'marks': 'not notnps1safe',
    },
    'union': {
        'env_file': 'integration/environments/union.yaml',
        'username': 'prn.t_dfederov',
        'pin': 3574,
        'secret_key': '4E4DHQTPMU7QL4NKHOJD3KJTVJL7FURX',
        'marks': 'not notprodsafe',
    },
    'cn360': {
        'env_file': 'integration/environments/cn360.yaml',
        'username': 'prn.t_dfederov',
        'pin': 3574,
        'secret_key': '4E4DHQTPMU7QL4NKHOJD3KJTVJL7FURX',
        'marks': 'not notprodsafe',
    },
    'trie': {
        'env_file': 'integration/environments/trie.yaml',
        'username': None,
        'password': None,
        'marks': 'not notnps1safe',
    },
}

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='setup test title')
    parser.add_argument('tests', help='tests')
    parser.add_argument('--env', required=False, action='store', help='the environment file session')
    parser.add_argument('--plan', required=False, action='store', help='the environment file session')
    parser.add_argument('--username', required=False, action='store', help='tools admin username')
    parser.add_argument('--password', required=False, action='store', help='tools admin password')
    parser.add_argument('--pin', required=False, action='store', help='tools admin pin. Necessary for OTP')
    parser.add_argument(
        '--secret_key',
        required=False,
        action='store',
        help='tools admin secret key. Necessary for OTP'
    )
    parser.add_argument(
        '--skip_pub',
        required=False,
        action='store',
        help='skips catalog publish before suite. Set to anything to skip'
    )
    parser.add_argument('--threads', required=False, action='store', default='auto', help='number of threads to use')
    parser.add_argument('--reruns', required=False, action='store', default=3, help='times to rerun failed tests')
    parser.add_argument(
        '--env_color',
        required=False,
        action='store',
        default='blue',
        help='skips catalog publish before suite. Set to anything to skip'
    )
    parser.add_argument(
        '--alluredir',
        required=False,
        action='store',
        default='integration/results/allure-results',
        help='allure directory'
    )
    args, other_args = parser.parse_known_args()

    env = None
    username = None
    password = None
    pin = None
    secret_key = None
    name = None

    if args.plan is not None:
        assert args.plan in TEST_SETS, 'TEST_SETS does not contain {}'.format(args.plan)

        test_set = TEST_SETS[args.plan]
        env = test_set['env_file']
        username = test_set['username']
        password = test_set['password'] if 'password' in test_set else None
        pin = test_set['pin'] if 'pin' in test_set else None
        secret_key = test_set['secret_key'] if 'secret_key' in test_set else None

    env = args.env if args.env is not None else env
    username = args.username if args.username is not None else username
    password = args.password if args.password is not None else password
    pin = args.pin if args.pin is not None else pin
    secret_key = args.secret_key if args.secret_key is not None else secret_key

    assert env is not None, 'Either --env or --plan are required'

    test_plan = Plan('Integration Test Plan')
    test_plan.initialize()

    test_plan.echo('installing requirements')
    test_plan.pip_install(
        '-U',
        '--extra-index-url',
        'https://pypi.python.org/simple',
        '-r',
        'integration/requirements.txt'
    )

    import setup
    from integration.main.services import ConsulManager, ServerAdmin
    from integration.main.session import ConfigAdapter

    test_plan.echo('Getting Freya version')

    config_adapter = ConfigAdapter(env, username, password, pin, secret_key, name)

    admin_url = config_adapter.environment['url']['base']

    if config_adapter.environment.use_consul_urls:
        test_plan.echo('Getting server admin url from consul for \'{}\' environment'.format(args.env_color))
        consul = ConsulManager(config_adapter.environment.consul, config_adapter.environment.environment_name)
        admin_url = consul.get_server_admin_url(args.env_color)

    test_plan.echo('Server admin url: \'{}\''.format(admin_url))
    server_admin = ServerAdmin(admin_url)

    test_plan.echo('Getting build info')
    build_info_response = server_admin.get_build_info()
    build_info_response.assert_is_success()

    test_plan.echo(json.dumps(build_info_response.content, indent=2))

    version = build_info_response.content['Implementation-Version']
    version_number = version.split('-')[0]
    test_plan.export('FREYA_VERSION', version_number)

    if args.skip_pub is None:

        test_plan.echo('Setting up title relationships and title configurations')
        # setup.setup_title_relationships_and_configurations(config_adapter)

        test_plan.echo('Disable Import catalog and publishing catalog')
        #
        # setup.import_and_publish_catalog(config_adapter)

    else:
        test_plan.echo('skipping publish')

    # test_plan.echo('Waiting for fetchProducts to finish and indicate publish is complete')
    # waiter = WaitOn(
    #     lambda: config_adapter.freya.server_gateway.fetchProducts(
    #         [config_adapter.data.TEST_PRODUCT.PRODUCT_CODE],
    #         0,
    #         config_adapter.data.TEST_PRODUCT.COUNTRY,
    #         config_adapter.data.TEST_PRODUCT.LANGUAGE
    #     ).success
    # ).until(ReturnValue.EQUAL_TO(True), 45)
    #
    # waiter.wait(message='fetchProducts did not successfully retrieve product from catalog after 45 seconds')

    test_plan.echo('we are skipping pub in the run because we have already configured title and published catalog')
    test_plan.echo('Running thread safe tests')

    thread_safe_allure_args = '{}-ts'.format(args.alluredir) if args.alluredir is not None else None
    ts_return = test_plan.integration_test(
        args.tests,
        env,
        username=username,
        password=password,
        pin=pin,
        secret_key=secret_key,
        allure=thread_safe_allure_args,
        reruns=args.reruns,
        threads=args.threads,
        marks=TEST_SETS[config_adapter.environment.environment_name]['marks'],
        other_args=other_args
    )

    test_plan.echo('we are skipping pub in the run because we have already configured title and published catalog')
    test_plan.echo('Running not thread safe tests')

    not_thread_safe_allure_args = '{}-nts'.format(args.alluredir) if args.alluredir is not None else None
    nts_return = test_plan.integration_test(
        args.tests,
        env,
        username=username,
        password=password,
        pin=pin,
        secret_key=secret_key,
        allure='{}-nts'.format(args.alluredir) if args.alluredir is not None else None,
        reruns=args.reruns,
        threads=None,
        marks=TEST_SETS[config_adapter.environment.environment_name]['marks'],
        other_args=other_args
    )

    test_plan.echo('SINGLE THREADED RESULTS: exit code: {}'.format(nts_return))
    nts_pass = nts_return == 0 or nts_return == 5
    test_plan.echo('PASS' if nts_pass else 'FAILED', output_color='green' if nts_pass else 'red')

    test_plan.echo('MULTI THREADED RESULTS: exit code: {}'.format(ts_return))
    ts_pass = ts_return == 0 or ts_return == 5
    test_plan.echo('PASS' if ts_pass else 'FAILED', output_color='green' if ts_pass else 'red')

    test_plan.echo('not thread safe allure tag = {}'.format(not_thread_safe_allure_args))
    test_plan.echo('thread safe allure tag = {}'.format(thread_safe_allure_args))

    if nts_pass and ts_pass:
        test_plan.exit(0)
    else:
        test_plan.exit(1)
