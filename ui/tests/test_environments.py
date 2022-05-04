import pytest
from hamcrest import assert_that, equal_to, has_length, greater_than_or_equal_to

from ui.main.constants import PLATFORM_HEADER_TEXT
from ui.pages import Sidebar, Header, Environments
from selenium.common.exceptions import NoSuchElementException


@pytest.allure.step('Validate elements on the environments page')
def validate_page_and_its_functionality(environments_page, config):
    # validate elements on the page
    assert_that(environments_page.get_environments_title().text, equal_to('Environments'))
    assert_that(environments_page.get_environments_subheading().text, equal_to('{} > {}'.format(
        config.data.TEST_STUDIO.CODE,
        config.data.TEST_TITLE.CODE,
    )))

    wgie_activated_list_response = config.freya.tools_gateway.v2.list_realm_activations(
        config.data.TEST_STUDIO.CODE,
        'wgie',
        title_code=config.data.TEST_TITLE.CODE
    )
    wgie_activated_list_response.assert_success()
    wgie_activated_catalogs = wgie_activated_list_response.content['data']

    assert_that(environments_page.get_realm_box_by_name('wgie'))
    assert_that(environments_page.get_realm_heading_by_name('wgie'))
    assert_that(environments_page.get_realm_status_by_name('wgie'))
    assert_that(
        environments_page.get_realm_last_published_span_by_name('wgie').text,
        equal_to('Last published catalog')
    )
    if len(wgie_activated_catalogs) > 0:
        last_published_wgie_catalog = wgie_activated_catalogs[0]
        wgie_last_published_catalog_span = environments_page.get_realm_last_published_catalog_by_name(
            'wgie',
            last_published_wgie_catalog['catalog_code']
        )
        assert_that(
            wgie_last_published_catalog_span.text,
            equal_to('{} (v.{})'.format(
                last_published_wgie_catalog['catalog_code'],
                last_published_wgie_catalog['version'])
            )
        )
        assert_that(environments_page.get_realm_last_published_catalog_title_by_name(
            'wgie',
            last_published_wgie_catalog['catalog_code']
        ))
    else:
        assert_that(
            environments_page.get_realm_no_published_catalog_by_name('wgie').text,
            equal_to('No published catalogs')
        )

    prv_activated_list_response = config.freya.tools_gateway.v2.list_realm_activations(
        config.data.TEST_STUDIO.CODE,
        'prv',
        title_code=config.data.TEST_TITLE.CODE
    )
    prv_activated_list_response.assert_success()
    prv_activated_catalogs = prv_activated_list_response.content['data']

    assert_that(environments_page.get_realm_box_by_name('prv'))
    assert_that(environments_page.get_realm_heading_by_name('prv'))
    assert_that(environments_page.get_realm_status_by_name('prv'))
    assert_that(environments_page.get_realm_last_published_span_by_name('prv').text, equal_to('Last published catalog'))
    if len(prv_activated_catalogs) > 0:
        last_published_prv_catalog = prv_activated_catalogs[0]
        prv_last_published_catalog_span = environments_page.get_realm_last_published_catalog_by_name(
            'prv',
            last_published_prv_catalog['catalog_code']
        )
        assert_that(
            prv_last_published_catalog_span.text,
            equal_to('{} (v.{})'.format(
                last_published_prv_catalog['catalog_code'],
                last_published_prv_catalog['version'])
            )
        )
        assert_that(environments_page.get_realm_last_published_catalog_title_by_name(
            'prv',
            last_published_prv_catalog['catalog_code']
        ))
    else:
        assert_that(
            environments_page.get_realm_no_published_catalog_by_name('prv').text,
            equal_to('No published catalogs')
        )

    ru_activated_list_response = config.freya.tools_gateway.v2.list_realm_activations(
        config.data.TEST_STUDIO.CODE,
        'ru',
        title_code=config.data.TEST_TITLE.CODE
    )
    ru_activated_list_response.assert_success()
    ru_activated_catalogs = ru_activated_list_response.content['data']

    assert_that(environments_page.get_realm_box_by_name('ru'))
    assert_that(environments_page.get_realm_heading_by_name('ru'))
    assert_that(environments_page.get_realm_status_by_name('ru'))
    assert_that(environments_page.get_realm_last_published_span_by_name('ru').text, equal_to('Last published catalog'))
    if len(ru_activated_catalogs) > 0:
        last_published_ru_catalog = ru_activated_catalogs[0]
        ru_last_published_catalog_span = environments_page.get_realm_last_published_catalog_by_name(
            'ru',
            last_published_ru_catalog['catalog_code']
        )
        assert_that(
            ru_last_published_catalog_span.text,
            equal_to('{} (v.{})'.format(
                last_published_ru_catalog['catalog_code'],
                last_published_ru_catalog['version'])
            )
        )
        assert_that(environments_page.get_realm_last_published_catalog_title_by_name(
            'ru',
            last_published_ru_catalog['catalog_code']
        ))
    else:
        assert_that(
            environments_page.get_realm_no_published_catalog_by_name('ru').text,
            equal_to('No published catalogs')
        )

    na_activated_list_response = config.freya.tools_gateway.v2.list_realm_activations(
        config.data.TEST_STUDIO.CODE,
        'na',
        title_code=config.data.TEST_TITLE.CODE
    )
    na_activated_list_response.assert_success()
    na_activated_catalogs = na_activated_list_response.content['data']

    assert_that(environments_page.get_realm_box_by_name('na'))
    assert_that(environments_page.get_realm_heading_by_name('na'))
    assert_that(environments_page.get_realm_status_by_name('na'))
    assert_that(environments_page.get_realm_last_published_span_by_name('na').text, equal_to('Last published catalog'))
    if len(na_activated_catalogs) > 0:
        last_published_na_catalog = na_activated_catalogs[0]
        na_last_published_catalog_span = environments_page.get_realm_last_published_catalog_by_name(
            'na',
            last_published_na_catalog['catalog_code']
        )
        assert_that(
            na_last_published_catalog_span.text,
            equal_to('{} (v.{})'.format(
                last_published_na_catalog['catalog_code'],
                last_published_na_catalog['version'])
            )
        )
        assert_that(environments_page.get_realm_last_published_catalog_title_by_name(
            'na',
            last_published_na_catalog['catalog_code']
        ))
    else:
        assert_that(
            environments_page.get_realm_no_published_catalog_by_name('na').text,
            equal_to('No published catalogs')
        )

    eu_activated_list_response = config.freya.tools_gateway.v2.list_realm_activations(
        config.data.TEST_STUDIO.CODE,
        'eu',
        title_code=config.data.TEST_TITLE.CODE
    )
    eu_activated_list_response.assert_success()
    eu_activated_catalogs = eu_activated_list_response.content['data']

    assert_that(environments_page.get_realm_box_by_name('eu'))
    assert_that(environments_page.get_realm_heading_by_name('eu'))
    assert_that(environments_page.get_realm_status_by_name('eu'))
    assert_that(environments_page.get_realm_last_published_span_by_name('eu').text, equal_to('Last published catalog'))
    if len(eu_activated_catalogs) > 0:
        last_published_eu_catalog = eu_activated_catalogs[0]
        eu_last_published_catalog_span = environments_page.get_realm_last_published_catalog_by_name(
            'eu',
            last_published_eu_catalog['catalog_code']
        )
        assert_that(
            eu_last_published_catalog_span.text,
            equal_to('{} (v.{})'.format(
                last_published_eu_catalog['catalog_code'],
                last_published_eu_catalog['version'])
            )
        )
        assert_that(environments_page.get_realm_last_published_catalog_title_by_name(
            'eu',
            last_published_eu_catalog['catalog_code']
        ))
    else:
        assert_that(
            environments_page.get_realm_no_published_catalog_by_name('eu').text,
            equal_to('No published catalogs')
        )

    asia_activated_list_response = config.freya.tools_gateway.v2.list_realm_activations(
        config.data.TEST_STUDIO.CODE,
        'asia',
        title_code=config.data.TEST_TITLE.CODE
    )
    asia_activated_list_response.assert_success()
    asia_activated_catalogs = asia_activated_list_response.content['data']

    assert_that(environments_page.get_realm_box_by_name('asia'))
    assert_that(environments_page.get_realm_heading_by_name('asia'))
    assert_that(environments_page.get_realm_status_by_name('asia'))
    assert_that(
        environments_page.get_realm_last_published_span_by_name('asia').text,
        equal_to('Last published catalog')
    )
    if len(asia_activated_catalogs) > 0:
        last_published_asia_catalog = asia_activated_catalogs[0]
        asia_last_published_catalog_span = environments_page.get_realm_last_published_catalog_by_name(
            'asia',
            last_published_asia_catalog['catalog_code']
        )
        assert_that(
            asia_last_published_catalog_span.text,
            equal_to('{} (v.{})'.format(
                last_published_asia_catalog['catalog_code'],
                last_published_asia_catalog['version'])
            )
        )
        assert_that(environments_page.get_realm_last_published_catalog_title_by_name(
            'asia',
            last_published_asia_catalog['catalog_code']
        ))
    else:
        assert_that(
            environments_page.get_realm_no_published_catalog_by_name('asia').text,
            equal_to('No published catalogs')
        )

    # test page functionality
    environments_page.click_realm_heading_by_name('wgie')
    assert_that(environments_page.get_details_heading().text, equal_to('WGIE'))
    assert_that(environments_page.get_details_status())
    assert_that(environments_page.get_details_close_button())
    num_wgie_activated_catalogs = len(wgie_activated_catalogs)
    num_wgie_catalogs_shown = min(num_wgie_activated_catalogs, 15)
    assert_that(
        environments_page.get_details_catalogs_header().text,
        equal_to('Catalogs ({}/{})'.format(num_wgie_catalogs_shown, num_wgie_activated_catalogs))
    )
    assert_that(
        environments_page.get_details_last_published_button().text,
        equal_to('Sort by: Last published')
    )
    assert_that(environments_page.get_details_catalogs_list(), has_length(greater_than_or_equal_to(0)))
    if num_wgie_activated_catalogs > 0:
        last_published_wgie_catalog = wgie_activated_catalogs[0]
        wgie_catalog = environments_page.get_details_catalog(
            last_published_wgie_catalog['catalog_code'],
            last_published_wgie_catalog['version'],
            0
        )
        assert_that(
            wgie_catalog.text,
            equal_to('{} (v.{})'.format(
                last_published_wgie_catalog['catalog_code'],
                last_published_wgie_catalog['version'])
            )
        )
        assert_that(environments_page.get_details_catalog_title(
            last_published_wgie_catalog['catalog_code'],
            last_published_wgie_catalog['version']
        ))
        assert_that(environments_page.get_details_catalog_actions_menu(
            last_published_wgie_catalog['catalog_code'],
            last_published_wgie_catalog['version'],
            0
        ))

    environments_page.click_realm_heading_by_name('prv')
    assert_that(environments_page.get_details_heading().text, equal_to('Preview'))
    assert_that(environments_page.get_details_status())
    assert_that(environments_page.get_details_close_button())
    num_prv_activated_catalogs = len(prv_activated_catalogs)
    num_prv_catalogs_shown = min(num_prv_activated_catalogs, 15)
    assert_that(
        environments_page.get_details_catalogs_header().text,
        equal_to('Catalogs ({}/{})'.format(num_prv_catalogs_shown, num_prv_activated_catalogs))
    )
    assert_that(
        environments_page.get_details_last_published_button().text,
        equal_to('Sort by: Last published')
    )
    assert_that(environments_page.get_details_catalogs_list(), has_length(greater_than_or_equal_to(0)))
    if num_prv_activated_catalogs > 0:
        last_published_prv_catalog = prv_activated_catalogs[0]
        prv_catalog = environments_page.get_details_catalog(
            last_published_prv_catalog['catalog_code'],
            last_published_prv_catalog['version'],
            0
        )
        assert_that(
            prv_catalog.text,
            equal_to('{} (v.{})'.format(
                last_published_prv_catalog['catalog_code'],
                last_published_prv_catalog['version'])
            )
        )
        assert_that(environments_page.get_details_catalog_title(
            last_published_prv_catalog['catalog_code'],
            last_published_prv_catalog['version']
        ))
        assert_that(environments_page.get_details_catalog_actions_menu(
            last_published_prv_catalog['catalog_code'],
            last_published_prv_catalog['version'],
            0
        ))

    environments_page.click_realm_heading_by_name('ru')
    assert_that(environments_page.get_details_heading().text, equal_to('RU'))
    assert_that(environments_page.get_details_status())
    assert_that(environments_page.get_details_close_button())
    num_ru_activated_catalogs = len(ru_activated_catalogs)
    num_ru_catalogs_shown = min(num_ru_activated_catalogs, 15)
    assert_that(
        environments_page.get_details_catalogs_header().text,
        equal_to('Catalogs ({}/{})'.format(num_ru_catalogs_shown, num_ru_activated_catalogs))
    )
    assert_that(
        environments_page.get_details_last_published_button().text,
        equal_to('Sort by: Last published')
    )
    assert_that(environments_page.get_details_catalogs_list(), has_length(greater_than_or_equal_to(0)))
    if num_ru_activated_catalogs > 0:
        last_published_ru_catalog = ru_activated_catalogs[0]
        ru_catalog = environments_page.get_details_catalog(
            last_published_ru_catalog['catalog_code'],
            last_published_ru_catalog['version'],
            0
        )
        assert_that(
            ru_catalog.text,
            equal_to('{} (v.{})'.format(
                last_published_ru_catalog['catalog_code'],
                last_published_ru_catalog['version'])
            )
        )
        assert_that(environments_page.get_details_catalog_title(
            last_published_ru_catalog['catalog_code'],
            last_published_ru_catalog['version']
        ))
        assert_that(environments_page.get_details_catalog_actions_menu(
            last_published_ru_catalog['catalog_code'],
            last_published_ru_catalog['version'],
            0
        ))

    environments_page.click_realm_heading_by_name('na')
    assert_that(environments_page.get_details_heading().text, equal_to('NA'))
    assert_that(environments_page.get_details_status())
    assert_that(environments_page.get_details_close_button())
    num_na_activated_catalogs = len(na_activated_catalogs)
    num_na_catalogs_shown = min(num_na_activated_catalogs, 15)
    assert_that(
        environments_page.get_details_catalogs_header().text,
        equal_to('Catalogs ({}/{})'.format(num_na_catalogs_shown, num_na_activated_catalogs))
    )
    assert_that(
        environments_page.get_details_last_published_button().text,
        equal_to('Sort by: Last published')
    )
    assert_that(environments_page.get_details_catalogs_list(), has_length(greater_than_or_equal_to(0)))
    if num_na_activated_catalogs > 0:
        last_published_na_catalog = na_activated_catalogs[0]
        na_catalog = environments_page.get_details_catalog(
            last_published_na_catalog['catalog_code'],
            last_published_na_catalog['version'],
            0
        )
        assert_that(
            na_catalog.text,
            equal_to('{} (v.{})'.format(
                last_published_na_catalog['catalog_code'],
                last_published_na_catalog['version'])
            )
        )
        assert_that(environments_page.get_details_catalog_title(
            last_published_na_catalog['catalog_code'],
            last_published_na_catalog['version']
        ))
        assert_that(environments_page.get_details_catalog_actions_menu(
            last_published_na_catalog['catalog_code'],
            last_published_na_catalog['version'],
            0
        ))

    environments_page.click_realm_heading_by_name('eu')
    assert_that(environments_page.get_details_heading().text, equal_to('EU'))
    assert_that(environments_page.get_details_status())
    assert_that(environments_page.get_details_close_button())
    num_eu_activated_catalogs = len(eu_activated_catalogs)
    num_eu_catalogs_shown = min(num_eu_activated_catalogs, 15)
    assert_that(
        environments_page.get_details_catalogs_header().text,
        equal_to('Catalogs ({}/{})'.format(num_eu_catalogs_shown, num_eu_activated_catalogs))
    )
    assert_that(
        environments_page.get_details_last_published_button().text,
        equal_to('Sort by: Last published')
    )
    assert_that(environments_page.get_details_catalogs_list(), has_length(greater_than_or_equal_to(0)))
    if num_eu_activated_catalogs > 0:
        last_published_eu_catalog = eu_activated_catalogs[0]
        eu_catalog = environments_page.get_details_catalog(
            last_published_eu_catalog['catalog_code'],
            last_published_eu_catalog['version'],
            0
        )
        assert_that(
            eu_catalog.text,
            equal_to('{} (v.{})'.format(
                last_published_eu_catalog['catalog_code'],
                last_published_eu_catalog['version'])
            )
        )
        assert_that(environments_page.get_details_catalog_title(
            last_published_eu_catalog['catalog_code'],
            last_published_eu_catalog['version']
        ))
        assert_that(environments_page.get_details_catalog_actions_menu(
            last_published_eu_catalog['catalog_code'],
            last_published_eu_catalog['version'],
            0
        ))

    environments_page.click_realm_heading_by_name('asia')
    assert_that(environments_page.get_details_heading().text, equal_to('Asia'))
    assert_that(environments_page.get_details_status())
    assert_that(environments_page.get_details_close_button())
    num_asia_activated_catalogs = len(asia_activated_catalogs)
    num_asia_catalogs_shown = min(num_asia_activated_catalogs, 15)
    assert_that(
        environments_page.get_details_catalogs_header().text,
        equal_to('Catalogs ({}/{})'.format(num_asia_catalogs_shown, num_asia_activated_catalogs))
    )
    assert_that(
        environments_page.get_details_last_published_button().text,
        equal_to('Sort by: Last published')
    )
    assert_that(environments_page.get_details_catalogs_list(), has_length(greater_than_or_equal_to(0)))
    if num_asia_activated_catalogs > 0:
        last_published_asia_catalog = asia_activated_catalogs[0]
        asia_catalog = environments_page.get_details_catalog(
            last_published_asia_catalog['catalog_code'],
            last_published_asia_catalog['version'],
            0
        )
        assert_that(
            asia_catalog.text,
            equal_to('{} (v.{})'.format(
                last_published_asia_catalog['catalog_code'],
                last_published_asia_catalog['version'])
            )
        )
        assert_that(environments_page.get_details_catalog_title(
            last_published_asia_catalog['catalog_code'],
            last_published_asia_catalog['version']
        ))
        assert_that(environments_page.get_details_catalog_actions_menu(
            last_published_asia_catalog['catalog_code'],
            last_published_asia_catalog['version'],
            0
        ))


@pytest.allure.step('Validate elements on the environments sidebar page')
def validate_environments_sidebar_page(sidebar_page):
    # assert_that(sidebar_page.get_dashboard_button().text, equal_to('Dashboard'))
    # assert_that(sidebar_page.get_titles_button().text, equal_to('Titles'))
    assert_that(sidebar_page.get_back_to_titles_button().text, equal_to('< Back to Titles'))
    assert_that(sidebar_page.get_catalogs_button().text, equal_to('Catalogs'))
    assert_that(sidebar_page.get_environments_button().text, equal_to('Environments'))
    assert_that(sidebar_page.get_title_components_button().text, equal_to('Title Components'))
    # assert_that(sidebar_page.get_activity_button().text, equal_to('Activity'))
    # assert_that(sidebar_page.get_users_button().text, equal_to('Users'))
    assert_that(sidebar_page.get_players_button().text, equal_to('Players'))
    # assert_that(sidebar_page.get_reports_button().text, equal_to('Reports'))
    assert_that(sidebar_page.get_panel(), has_length(5))


@pytest.allure.step('Validate elements on the environments header page')
def validate_environments_header_page(header_page):
    assert_that(header_page.get_home_button())

    top_bar_header = header_page.get_top_bar_header()
    assert_that(top_bar_header.text, equal_to(PLATFORM_HEADER_TEXT))

    # assert_that(header_page.get_network_status())
    #
    # assert_that(header_page.get_notification_icon())

    assert_that(header_page.get_settings_icon())

    assert_that(header_page.get_drop_down_menu())

    assert_that(header_page.get_user_icon())

    assert_that(header_page.get_user_id())

    assert_that(header_page.get_logout_button())


@pytest.fixture
def setup(config, browser, steps):
    environments_page = Environments(browser)
    sidebar_page = Sidebar(browser)
    header_page = Header(browser)

    steps.login(config.admin.username, config.admin.password)
    steps.navigate_to_titles_page(config.data.TEST_STUDIO.CODE)
    steps.navigate_to_catalogs_page(config.data.TEST_TITLE.CODE)
    steps.navigate_to_environments_page()

    yield environments_page, sidebar_page, header_page


@pytest.allure.testcase("Validate environments page")
def test_environments_page(setup, config):
    environments_page, _, _ = setup
    validate_page_and_its_functionality(environments_page, config)


@pytest.allure.testcase("Validate environments sidebar page")
@pytest.mark.xfail(reason='PLAT-6175', raises=NoSuchElementException)
def test_environments_sidebar_page(setup):
    _, sidebar_page, _ = setup
    validate_environments_sidebar_page(sidebar_page)


@pytest.allure.testcase("Validate environments header page")
def test_environments_header_page(setup):
    _, _, header_page = setup
    validate_environments_header_page(header_page)
