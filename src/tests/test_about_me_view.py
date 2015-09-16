from src.tests import get_article_id, about_me_content
from src.tests.sublog_test_utils import SublogTestCase
from sublog import settings


class AboutMeViewTest(SublogTestCase):
    def setUp(self):
        self.login()
        self.token = "test_TEST "
        self.title = self.token * 10
        self.content = self.token * 200

        article_id = get_article_id(self.post_article(self.title, self.content))
        settings.ABOUT_ME_ID = article_id

    def test_about_me_content(self):
        amc = about_me_content(self.get_about_me_page())

        self.assertTrue(self.title in amc['title'])
        self.assertTrue(self.content in amc['content'])

    def test_about_me_not_in_index(self):
        index_content = self.get_index_page().content
        self.assertFalse(self.token in index_content)
