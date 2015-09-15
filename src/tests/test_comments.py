from src.tests import *
from src.tests.sublog_test_utils import SublogTestCase


class CommentsTests(SublogTestCase):
    def setUp(self):
        self.login()

    def test_article_has_no_comments(self):
        article_page = self.post_article(TITLE_1, CONTENT_1)
        self.assertContains(article_page, 'No comments yet')
        self.assertEquals(0, len(get_comments(article_page)))

    def test_article_has_2_comments(self):
        self.post_article(self.client, TITLE_1, CONTENT_1)
        self.post_comment(1, "", NEW_CONTENT, USER_NAME_1, 'email_1@ex.com')
        self.post_comment(1, TITLE_2, CONTENT_2, USER_NAME_2, 'email_2@ex.com')

        comments = get_comments(self.get_article_page(1))
        self.assert_comment(comments[0], TITLE_2, USER_NAME_2, EXP_CONTENT_2)
        self.assert_comment(comments[1], "-- no title --", USER_NAME_1, EXP_NEW_CONTENT)

    def assert_comment(self, comment, title, name, content):
        self.assertEquals(title, comment['title'])
        self.assertEquals(name, comment['name'])
        self.assertEquals(content, comment['content'])
