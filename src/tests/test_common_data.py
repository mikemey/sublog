from django.core.urlresolvers import reverse

from src.tests import get_version, TITLE_1, CONTENT_1, NEW_TITLE, NEW_CONTENT, get_error_message, get_user_name
from src.tests.sublog_test_utils import SublogTestCase, TEST_USER_NAME
from sublog import settings

test_version = 'tv1.0'
settings.SU_VERSION = test_version


class CommonDataTests(SublogTestCase):
    def test_version_on_index_page(self):
        index = self.get_index_page()
        self.assertEquals(test_version, get_version(index))

    def test_version_on_article_page(self):
        self.login()
        self.post_article(TITLE_1, CONTENT_1)
        article_page = self.get_article_page(1)
        self.assertEquals(test_version, get_version(article_page))

    def test_version_after_posting_article_redirect(self):
        new_article = self.post_article(NEW_TITLE, NEW_CONTENT)
        self.assertEquals(test_version, get_version(new_article))

    def test_user_name_shown(self):
        self.login()
        expected_line = 'Logged in: %s' % TEST_USER_NAME
        self.assertEquals(expected_line, get_user_name(self.get_index_page()))

    def test_no_user_line_when_anonymous(self):
        self.assertIsNone(get_user_name(self.get_index_page()))

    def test_logout_redirects_to_next_url(self):
        self.login()
        self.post_article(TITLE_1, CONTENT_1)
        logout_target = '/another_endpoint'
        redirect_page = self.logout(logout_target)
        self.assertRedirects(redirect_page, logout_target, fetch_redirect_response=False)

    def test_invalid_login_shows_error_message(self):
        login_page = self.client.get('/login/')
        self.assertIsNone(get_error_message(login_page))

        login_page = self.client.post(reverse('login'),
                                      {'username': 'some',
                                       'password': 'error'
                                       })
        self.assertEquals(200, login_page.status_code)
        self.assertEquals('Please enter a correct username and/or password.', get_error_message(login_page))
