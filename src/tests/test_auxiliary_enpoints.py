from src.tests.sublog_test_utils import SublogTestCase


class AuxiliaryEndpointsTests(SublogTestCase):
    def ping_response(self, user_agent):
        header = {'HTTP_USER_AGENT': user_agent} if user_agent else {}
        return self.client.get('/ping/', **header)

    def test_health_check_accepts_UC_Browser(self):
        user_agent = "UCBrowser1.0.0"
        self.assertEquals('{ "status": "ok" }', self.ping_response(user_agent).content)

    def test_health_check_accepts_curl_user_agent(self):
        user_agent = "curl/7.43.0"
        self.assertEquals('{ "status": "ok" }', self.ping_response(user_agent).content)

    def test_health_check_refuses_no_user_agent(self):
        self.assertEquals(404, self.ping_response(None).status_code)

    def test_health_check_refuses_normal_user_agent(self):
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0"
        self.assertEquals(404, self.ping_response(user_agent).status_code)
