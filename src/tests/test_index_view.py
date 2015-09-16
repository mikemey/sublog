from src.tests import *
from src.tests.sublog_test_utils import SublogTestCase
from sublog import settings


class IndexViewTests(SublogTestCase):
    def setUp(self):
        self.login()
        settings.ABOUT_ME_ID = 0

    def test_index_view_with_no_articles(self):
        index = self.get_index_page()
        self.assertContains(index, 'No articles yet!')
        self.assertEquals(0, len(get_articles(index)))

    def test_index_view_shows_max_articles(self):
        max_articles = settings.ARTICLES_VISIBLE
        for i in range(max_articles + 1):
            self.post_article('t_' + str(i), 'c_' + str(i))

        articles = get_articles(self.get_index_page())
        self.assertEquals(max_articles, len(articles))
        for i in range(max_articles, 0, -1):
            self.assertEquals('t_' + str(i), articles[max_articles - i]['title'])
            self.assertTrue('c_' + str(i) in articles[max_articles - i]['content'])

    def test_post_article_response_code(self):
        response = self.post_article(NEW_TITLE, NEW_CONTENT, False)
        self.assertEquals(302, response.status_code)

    def test_post_article_redirects_to_article(self):
        self.post_article(TITLE_1, CONTENT_1)
        self.post_article(TITLE_2, CONTENT_2)

        response = self.post_article(NEW_TITLE, NEW_CONTENT, False)
        self.assertRedirects(response, '/article/3/')

    def test_post_article_shown_first(self):
        self.post_article(TITLE_1, CONTENT_1)
        self.post_article(NEW_TITLE, NEW_CONTENT)

        articles = get_articles(self.get_index_page())
        self.assertEquals(NEW_TITLE, articles[0]['title'])
        self.assertEquals(EXP_NEW_CONTENT, articles[0]['content'])
        self.assertEquals(TITLE_1, articles[1]['title'])
        self.assertEquals(EXP_CONTENT_1, articles[1]['content'])
