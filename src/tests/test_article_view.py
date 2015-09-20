from src.tests import TITLE_1, get_articles, get_article_id, CONTENT_1, get_previous_link, get_next_link
from src.tests.sublog_test_utils import SublogTestCase
from sublog import settings


class ArticleViewTest(SublogTestCase):
    def setUp(self):
        settings.ABOUT_ME_ID = 0

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

    def test_both_previous_next_links(self):
        prev_title = 'previous article title'
        next_title = 'next article title'
        ids = self.create_articles([prev_title, 'whatever', next_title])

        self.assert_link(ids[1], ids[0], prev_title, get_previous_link)
        self.assert_link(ids[1], ids[2], next_title, get_next_link)

    def test_no_previous_link(self):
        first_article_id = get_article_id(self.article_page)
        next_title = 'next article title'
        ids = self.create_articles([next_title])

        self.assert_no_link(first_article_id, get_previous_link)
        self.assert_link(first_article_id, ids[0], next_title, get_next_link)

    def test_no_next_link(self):
        prev_title = 'previous article title'
        ids = self.create_articles([prev_title, 'whatever'])

        self.assert_link(ids[1], ids[0], prev_title, get_previous_link)
        self.assert_no_link(ids[1], get_next_link)

    def create_articles(self, titles):
        ids = []
        for title in titles:
            ids.append(get_article_id(self.post_article(title, CONTENT_1)))
        return ids

    def assert_link(self, cur_article_id, expected_id, expected_label, get_link_func):
        expected_href = "/article/%s/" % expected_id

        link = get_link_func(self.get_article_page(cur_article_id))
        self.assertEquals(expected_href, link['href'])
        self.assertEquals(expected_label, link['label'])

    def assert_no_link(self, cur_article_id, get_link_func):
        link = get_link_func(self.get_article_page(cur_article_id))
        self.assertIsNone(link)
