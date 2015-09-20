from src.tests import *
from src.tests.sublog_test_utils import SublogTestCase, MailSendMock


class CommentsTests(SublogTestCase):
    def setUp(self):
        self.login()

    def test_article_has_no_comments(self):
        article_page = self.post_article(TITLE_1, CONTENT_1)
        self.assertContains(article_page, 'No comments yet')
        self.assertEquals(0, len(get_comments(article_page)))

    def test_article_has_2_comments(self):
        article_id = get_article_id(self.post_article(TITLE_1, CONTENT_1))
        self.post_comment(article_id, "", NEW_CONTENT, USER_NAME_1, 'email_1@ex.com')
        self.post_comment(article_id, TITLE_2, CONTENT_2, USER_NAME_2, 'email_2@ex.com')

        comments = get_comments(self.get_article_page(article_id))
        self.assert_comment(comments[0], TITLE_2, USER_NAME_2, EXP_CONTENT_2)
        self.assert_comment(comments[1], "-- no title --", USER_NAME_1, EXP_NEW_CONTENT)

    def assert_comment(self, comment, title, name, content):
        self.assertEquals(title, comment['title'])
        self.assertEquals(name, comment['name'])
        self.assertEquals(content, comment['content'])

    def test_mail_sent_when_commented(self):
        first_name = 'my name'
        article_title = 'some new title'
        email_subj = """New comment on article '%s'""" % article_title
        email_dest = 'lalal@lolo.com'
        commenter = 'some commenter'
        mail_mock = MailSendMock()

        self.login('blu_bdi_blu', 'some_pw', email_dest, first_name)
        article_id = get_article_id(self.post_article(article_title, CONTENT_1))

        expected_content = self.read_file_content('test_sent_mail_content.html')
        expected_content = expected_content.replace('{article_id}', article_id)

        self.post_comment(article_id, TITLE_1, CONTENT_2, commenter, 'bla@blu.com', mail_mock)

        self.assertTrue(email_dest, mail_mock.get_destination())
        self.assertTrue(email_subj, mail_mock.get_subject())
        self.compare_contents(expected_content, mail_mock.get_content())
