from src.tests import TITLE_1, get_articles
from src.tests.sublog_test_utils import SublogTestCase


class ArticleViewTest(SublogTestCase):
    def setUp(self):
        self.article_section = 'new line\nabc def ghi jkl\n\nmno pqr stu vwx\n'
        self.full_content = self.article_section * 10

        self.login()
        self.article_page = self.post_article(TITLE_1, self.full_content)

    def test_short_version_on_index_page(self):
        filler_len = len('</p><p>') * 7 + len('...') + len('<br />') * 10
        short_length = len(self.article_section * 6) + filler_len

        actual_content = self.assert_content_length(short_length, self.get_index_page())
        self.assertTrue(actual_content.strip().endswith('...</p>'))

    def test_long_version_on_article_page(self):
        full_length = len(self.full_content) + len('<br />') * 17 + len('</p><p>') * 11 + 1
        self.assert_content_length(full_length, self.article_page)

    def assert_content_length(self, expected_length, page):
        article = get_articles(page)[0]
        actual_content = article['content']
        self.assertEquals(expected_length, len(actual_content))
        return actual_content
