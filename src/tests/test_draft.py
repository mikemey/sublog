import json

from src.tests import TITLE_1, CONTENT_1, TITLE_2, CONTENT_2
from src.tests.sublog_test_utils import SublogTestCase
from src.views import DRAFT_CACHE


class DraftTests(SublogTestCase):
    def setUp(self):
        DRAFT_CACHE.data = {}

    def test_get_draft_not_allowed_for_anon(self):
        draft_response = self.get_draft()
        self.assertEquals(403, draft_response.status_code)

    def test_post_draft_not_allowed_for_anon(self):
        draft_response = self.post_draft(TITLE_1, CONTENT_1)
        self.assertEquals(403, draft_response.status_code)

    def test_post_draft_is_stored(self):
        self.login()
        self.assert_draft('', '')
        draft_response = self.post_draft(TITLE_1, CONTENT_1)
        self.assertEquals(201, draft_response.status_code)

        self.assert_draft(TITLE_1, CONTENT_1)

    def test_post_draft_is_deleted_after_post_article(self):
        self.login()
        self.post_draft(TITLE_1, CONTENT_1)
        self.post_article(TITLE_2, CONTENT_2)

        self.assert_draft('', '')

    def test_post_draft_is_stored_for_one_user_only(self):
        self.login('first user', '1st pw')
        self.post_draft(TITLE_1, CONTENT_1)
        self.logout()

        self.login('second user', '2nd pw')
        self.assert_draft('', '')
        self.post_draft(TITLE_2, CONTENT_2)
        self.assert_draft(TITLE_2, CONTENT_2)
        self.post_article(TITLE_2, CONTENT_2)
        self.logout()

        self.login('first user', '1st pw')
        self.assert_draft(TITLE_1, CONTENT_1)

    def assert_draft(self, title, content):
        draft_response = self.get_draft()
        data = json.loads(draft_response.content)
        self.assertEquals(title, data.get('title'))
        self.assertEquals(content, data.get('content'))
