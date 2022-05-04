import requests

from integration.main.services import Freya

sgrd_freya = Freya(
    'http://platform.sgrd.ix.wgcrowd.io/',
    'ead79acd-d282-49ea-b9d3-2739eabdd00e',
    session=requests.Session(),
    test_domains={}
)

login_response = sgrd_freya.tools_gateway.login.auth_login('admin', '111111')
login_response.assert_is_success()
