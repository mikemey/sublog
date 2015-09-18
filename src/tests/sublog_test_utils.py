import difflib

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.test.testcases import TestCase

TEST_FOLDER = '/Users/mmi/github/sublog/assets/test/'
TEST_USER_ID = 't'
TEST_USER_NAME = 'tester'
TEST_USER_PW = 'dad_asf'


def create_test_user(user=TEST_USER_ID, password=TEST_USER_PW):
    try:
        User.objects.get_by_natural_key(user)
    except ObjectDoesNotExist:
        user = User.objects.create_user(user, 'not@set.com', password, first_name=TEST_USER_NAME)
        user.save()


class SublogTestCase(TestCase):
    def read_file_content(self, file_name):
        return open(TEST_FOLDER + file_name).read()

    def compare_contents(self, expected, actual):
        expected = expected.splitlines()
        actual = actual.splitlines()

        diff = difflib.unified_diff(expected, actual)
        diff_msg = '\n'.join(diff)

        self.assertEquals(0, len(diff_msg), "Content differs: \n%s" % diff_msg)

    # HTTP request/responses
    # ==========================
    def login(self, user=TEST_USER_ID, password=TEST_USER_PW):
        create_test_user(user, password)
        next_url = '/somewhere/'
        response = self.client.post(reverse('login'),
                                    {'username': user,
                                     'password': password,
                                     'next': next_url
                                     })
        self.assertRedirects(response, next_url, fetch_redirect_response=False)

    def logout(self, next_url='/'):
        return self.client.post(reverse('logout'), {'next': next_url})

    def get_index_page(self):
        return self.client.get(reverse('index'))

    def get_article_page(self, article_id):
        return self.client.get('/article/%s/' % article_id)

    def get_new_article_page(self):
        return self.client.get('/article/')

    def post_article(self, title, content, follow=True):
        return self.client.post('/article/', data={'title': title, 'content': content}, follow=follow)

    def get_about_me_page(self):
        return self.client.get('/about/')

    def post_comment(self, article_id, title, content, name, email):
        post_data = {
            'title': title,
            'name': name,
            'email': email,
            'content': content
        }
        return self.client.post('/article/%s/comment/' % article_id, data=post_data, follow=True)

    def get_draft(self):
        return self.client.get('/article/draft/')

    def post_draft(self, title, content):
        post_data = {
            'title': title,
            'content': content
        }
        return self.client.post('/article/draft/', data=post_data, follow=True)
