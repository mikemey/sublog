import json

from src.tests import TITLE_1, CONTENT_1, TITLE_2, CONTENT_2
from src.tests.sublog_test_utils import SublogTestCase
from src.views import DRAFT_CACHE


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

    def test_get_draft_not_allowed_for_anon(self):
        draft_response = self.get_draft()
        self.assertEquals(403, draft_response.status_code)

    def test_post_draft_not_allowed_for_anon(self):
        draft_response = self.post_draft(TITLE_1, CONTENT_1)
        self.assertEquals(403, draft_response.status_code)

    def test_post_draft_is_stored(self):
        DRAFT_CACHE.invalidate()
        self.login()
        self.assert_draft('', '')
        draft_response = self.post_draft(TITLE_1, CONTENT_1)
        self.assertEquals(201, draft_response.status_code)

        self.assert_draft(TITLE_1, CONTENT_1)

    def test_post_draft_is_deleted_after_post_article(self):
        DRAFT_CACHE.invalidate()
        self.login()
        self.post_draft(TITLE_1, CONTENT_1)
        self.post_article(TITLE_2, CONTENT_2)

        self.assert_draft('', '')

    def assert_draft(self, title, content):
        draft_response = self.get_draft()
        data = json.loads(draft_response.content)
        self.assertEquals(title, data.get('title'))
        self.assertEquals(content, data.get('content'))
