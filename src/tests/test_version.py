from src.tests import get_version, TITLE_1, CONTENT_1, NEW_TITLE, NEW_CONTENT
from src.tests.sublog_test_utils import SublogTestCase
from sublog import settings

test_version = 'tv1.0'
settings.SU_VERSION = test_version


class VersionTests(SublogTestCase):
    def test_version_on_index_page(self):
        index = self.get_index_page()
        self.assertEquals(test_version, get_version(index))

    def test_version_on_article_page(self):
        self.post_article(self.client, TITLE_1, CONTENT_1)
        article_page = self.get_article_page(1)
        self.assertEquals(test_version, get_version(article_page))

    def test_version_after_posting_article_redirect(self):
        new_article = self.post_article(self.client, NEW_TITLE, NEW_CONTENT)
        self.assertEquals(test_version, get_version(new_article))
