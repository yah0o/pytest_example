from integration.main.request import RequestBuilder
import json


class TestTRTCSScript(object):

    def test_get_titles_should_succeed_when_compare_to_tr(self, config):
        config.log.info('Get TR Titles data')
        tr_url = config.environment['tr']['base']
        tr_response = RequestBuilder(tr_url).get()
        tr_response.assert_is_success()
        tr_titles = tr_response.content['titles']

        config.log.info('Get TCS Titles data')
        get_title_response = config.freya.title_registry.get_titles()
        get_title_response.assert_is_success()
        tcs_titles = get_title_response.content['titles']

        test_pass = True

        config.log.info('Compare TR title data to TCS title data')
        for tr_title in tr_titles:
            tcs_title = next(
                (
                    title for title in tcs_titles if title['code'] == tr_title['code']
                ),
                None
            )
            if tcs_title is None:
                continue

            tr_keys = sorted(tr_title.keys())
            tcs_keys = sorted(tcs_title.keys())

            if tr_keys != tcs_keys:
                test_pass = False
                config.log.error('TR {} keys are not the same as TCS\nTR keys: {}\nTCS keys: {}'.format(
                    tr_title['code'],
                    tr_keys,
                    tcs_keys
                ))

            for key in tr_keys:
                if key == 'server_api_key' or key not in tcs_keys:
                    continue
                if type(tr_title[key]) == list:
                    tr_title[key].sort()
                    tcs_title[key].sort()
                if (key != 'type' and tr_title[key] != tcs_title[key]) \
                        or (key == 'type' and tr_title[key] == 'system' and tcs_title[key] != 'service'):
                    test_pass = False
                    config.log.error('TR {} key "{}" value is not the same as TCS\nTR: {}\nTCS: {}'.format(
                        tr_title['code'],
                        key,
                        tr_title[key],
                        tcs_title[key]
                    ))

        assert test_pass

    def test_get_titles_should_succeed_when_compare_to_tr_with_namespaces(self, config):
        config.log.info('Get TR Titles data')
        tr_url = '{}?include=namespaces/'.format(config.environment['tr']['base'])
        tr_response = RequestBuilder(tr_url).get()
        tr_response.assert_is_success()
        tr_titles = tr_response.content['titles']

        config.log.info('Get TCS Titles data')
        get_title_response = config.freya.title_registry.get_titles()
        get_title_response.assert_is_success()
        tcs_titles = get_title_response.content['titles']

        test_pass = True

        config.log.info('Compare TR title data to TCS title data')
        for tr_title in tr_titles:
            tcs_title = next(
                (
                    title for title in tcs_titles if title['code'] == tr_title['code']
                ),
                None
            )
            if tcs_title is None:
                continue

            tr_keys = sorted(tr_title.keys())
            tcs_keys = sorted(tcs_title.keys())

            if tr_keys != tcs_keys:
                test_pass = False
                config.log.error('TR {} keys are not the same as TCS\nTR keys: {}\nTCS keys: {}'.format(
                    tr_title['code'],
                    tr_keys,
                    tcs_keys
                ))

            for key in tr_keys:
                if key == 'server_api_key' or key not in tcs_keys:
                    continue
                if type(tr_title[key]) == list:
                    tr_title[key].sort()
                    tcs_title[key].sort()
                if (key != 'type' and tr_title[key] != tcs_title[key]) \
                        or (key == 'type' and tr_title[key] == 'system' and tcs_title[key] != 'service'):
                    test_pass = False
                    config.log.error('TR {} key "{}" value is not the same as TCS\nTR: {}\nTCS: {}'.format(
                        tr_title['code'],
                        key,
                        tr_title[key],
                        tcs_title[key]
                    ))

        assert test_pass

    def test_get_components_should_succeed_when_compare_to_tr(self, config):
        config.log.info('Get TR Components data')
        tr_url = '{}components/'.format(config.environment['tr']['base'])
        tr_response = RequestBuilder(tr_url).get()
        tr_response.assert_is_success()
        tr_components = tr_response.content['resources']

        config.log.info('Get TCS Components data')
        get_components_response = config.freya.title_registry.get_components()
        get_components_response.assert_is_success()
        tcs_components = get_components_response.content['resources']

        test_pass = True

        config.log.info('Compare TR component data to TCS component data')
        for tr_component in tr_components:
            tcs_component = next(
                (
                    component for component in tcs_components
                    if component['title'] == tr_component['title']
                       and component['component'] == tr_component['component']
                ),
                None
            )
            if tcs_component is None:
                continue

            if 'bantypes' in tr_component.keys():
                tr_component['bantypes'].sort()
                tcs_component['bantypes'].sort()

            if tr_component != tcs_component:
                test_pass = False
                config.log.error('TR {} component {} data not same as TCS\nTR: {}\nTCS: {}'.format(
                    tr_component['title'],
                    tr_component['component'],
                    json.dumps(tr_component, indent=4),
                    json.dumps(tcs_component, indent=4)
                ))
        assert test_pass

    def test_get_currencies_should_succeed_when_compare_to_tr(self, config):
        config.log.info('Get TR Currencies data')
        tr_url = '{}currencies/'.format(config.environment['tr']['base'])
        tr_response = RequestBuilder(tr_url).get()
        tr_response.assert_is_success()
        tr_currencies = tr_response.content['data']

        config.log.info('Get TCS Currencies data')
        get_currencies_response = config.freya.title_registry.get_currencies()
        get_currencies_response.assert_is_success()
        tcs_currencies = get_currencies_response.content['data']

        test_pass = True

        config.log.info('Compare TR currency data to TCS currency data')
        for tr_currency in tr_currencies:
            tcs_currency = next(
                (
                    component for component in tcs_currencies
                    if component['title'] == tr_currency['title']
                       and component['code'] == tr_currency['code']
                ),
                None
            )
            if tcs_currency is None:
                continue

            if tr_currency != tcs_currency:
                test_pass = False
                config.log.error('TR {} currency {} data not same in TCS\nTR: {}\nTCS: {}'.format(
                    tr_currency['title'],
                    tr_currency['code'],
                    json.dumps(tr_currency, indent=4),
                    json.dumps(tcs_currency, indent=4)
                ))

        assert test_pass

    def test_get_currencies_virtual_should_succeed_when_compare_to_tr(self, config):
        config.log.info('Get TR Virtual Currencies Map data')
        tr_url = '{}currencies/map/'.format(config.environment['tr']['base'])
        tr_response = RequestBuilder(tr_url).get()
        tr_response.assert_is_success()
        tr_currencies_vc = tr_response.content['data']

        config.log.info('Get TCS Virtual Currencies Map data')
        get_currencies_vc_response = config.freya.title_registry.get_currencies_virtual()
        get_currencies_vc_response.assert_is_success()
        tcs_currencies_vc = get_currencies_vc_response.content['data']

        test_pass = True

        config.log.info('Compare TR VC currencies data to TCS VC currencies data')
        for tr_vc_currencies in tr_currencies_vc:
            tcs_vc_currencies = next(
                (
                    currencies for currencies in tcs_currencies_vc if currencies['title'] == tr_vc_currencies['title']
                ),
                None
            )
            if tcs_vc_currencies is None:
                continue

            def get_local_code(item):
                return item['local_code']

            tr_vc_currencies['currencies'].sort(key=get_local_code)
            tcs_vc_currencies['currencies'].sort(key=get_local_code)

            if tr_vc_currencies != tcs_vc_currencies:
                test_pass = False
                config.log.error('TR {} VC currencies data not same in TCS\nTR: {}\nTCS: {}'.format(
                    tr_vc_currencies['title'],
                    json.dumps(tr_vc_currencies, indent=4),
                    json.dumps(tcs_vc_currencies, indent=4)
                ))

        assert test_pass

    def test_get_currencies_real_should_succeed_when_compare_to_tr(self, config):
        config.log.info('Get TR Real Currencies Map data')
        tr_url = '{}currencies/real/'.format(config.environment['tr']['base'])
        tr_response = RequestBuilder(tr_url).get()
        tr_response.assert_is_success()
        tr_currencies_rm = tr_response.content['data']

        config.log.info('Get TCS Real Currencies Map data')
        get_currencies_rm_response = config.freya.title_registry.get_currencies_real()
        get_currencies_rm_response.assert_is_success()
        tcs_currencies_rm = get_currencies_rm_response.content['data']

        test_pass = True

        config.log.info('Compare TR RM currency data to TCS RM currency data')
        for tr_rm_currency in tr_currencies_rm:
            tcs_rm_currency = next(
                (
                    currency for currency in tcs_currencies_rm if currency['code'] == tr_rm_currency['code']
                ),
                None
            )
            if tcs_rm_currency is None:
                continue

            if tr_rm_currency != tcs_rm_currency:
                test_pass = False
                config.log.error('TR {} data not same in TCS\nTR: {}\nTCS: {}'.format(
                    tr_rm_currency['code'],
                    json.dumps(tr_rm_currency, indent=4),
                    json.dumps(tcs_rm_currency, indent=4)
                ))

        assert test_pass

    def test_get_entitlements_should_succeed_when_compare_to_tr(self, config):
        config.log.info('Get TR Entitlements data')
        tr_url = '{}entitlements/'.format(config.environment['tr']['base'])
        tr_response = RequestBuilder(tr_url).get()
        tr_response.assert_is_success()
        tr_entitlements = tr_response.content['entitlements']

        config.log.info('Get TCS Entitlements data')
        get_entitlements_response = config.freya.title_registry.get_entitlements()
        get_entitlements_response.assert_is_success()
        tcs_entitlements = get_entitlements_response.content['entitlements']

        test_pass = True

        config.log.info('Compare TR entitlement data to TCS entitlement data')
        for tr_entitlement in tr_entitlements:
            tcs_entitlement = next(
                (
                    entitlement for entitlement in tcs_entitlements
                    if entitlement['code'] == tr_entitlement['code']
                       and entitlement['title_code'] == tr_entitlement['title_code']
                ),
                None
            )
            if tcs_entitlement is None:
                continue

            if tr_entitlement != tcs_entitlement:
                test_pass = False
                config.log.error('TR {} data in Title {} not same in TCS\nTR: {}\nTCS: {}'.format(
                    tr_entitlement['code'],
                    tr_entitlement['title_code'],
                    json.dumps(tr_entitlement, indent=4),
                    json.dumps(tcs_entitlement, indent=4)
                ))

        assert test_pass

    def test_get_entitlements_map_should_succeed_when_compare_to_tr(self, config):
        config.log.info('Get TR Entitlements Map data')
        tr_url = '{}entitlements/map/'.format(config.environment['tr']['base'])
        tr_response = RequestBuilder(tr_url).get()
        tr_response.assert_is_success()
        tr_entitlements_map = tr_response.content['data']

        config.log.info('Get TCS Entitlements Map data')
        get_entitlements_map_response = config.freya.title_registry.get_entitlements_map()
        get_entitlements_map_response.assert_is_success()
        tcs_entitlements_map = get_entitlements_map_response.content['data']

        test_pass = True

        config.log.info('Compare TR entitlements map data to TCS entitlements map data')
        for tr_entitlements in tr_entitlements_map:
            tcs_entitlements = next(
                (
                    entitlements for entitlements in tcs_entitlements_map
                    if entitlements['title'] == tr_entitlements['title']
                ),
                None
            )
            if tcs_entitlements is None:
                continue

            def get_local_code(item):
                return item['local_code']

            tr_entitlements['entitlements'].sort(key=get_local_code)
            tcs_entitlements['entitlements'].sort(key=get_local_code)

            if tr_entitlements != tcs_entitlements:
                test_pass = False
                config.log.error('TR {} entitlements map data not same in TCS\nTR: {}\nTCS: {}'.format(
                    tr_entitlements['title'],
                    json.dumps(tr_entitlements, indent=4),
                    json.dumps(tcs_entitlements, indent=4)
                ))

        assert test_pass

    def test_get_namespaces_should_succeed_when_compare_to_tr(self, config):
        config.log.info('Get TR Namespaces data')
        tr_url = '{}namespaces/'.format(config.environment['tr']['base'])
        tr_response = RequestBuilder(tr_url).get()
        tr_response.assert_is_success()
        tr_namespaces = tr_response.content['namespaces']

        config.log.info('Get TR Namespaces data')
        get_namespaces_response = config.freya.title_registry.get_namespaces()
        get_namespaces_response.assert_is_success()
        tcs_namespaces = get_namespaces_response.content['namespaces']

        test_pass = True

        config.log.info('Compare TR namespaces data to TCS namespaces data')
        for tr_namespace in tr_namespaces:
            tcs_namespace = next(
                (
                    namespace for namespace in tcs_namespaces
                    if namespace['namespace'] == tr_namespace['namespace']
                       and namespace['title_id'] == tr_namespace['title_id']
                ),
                None
            )
            if tcs_namespace is None:
                continue

            if tr_namespace != tcs_namespace:
                test_pass = False
                config.log.error('TR {} namespace data not same in TCS\nTR: {}\nTCS: {}'.format(
                    tr_namespace['namespace'],
                    json.dumps(tr_namespace, indent=4),
                    json.dumps(tcs_namespace, indent=4)
                ))

        assert test_pass
