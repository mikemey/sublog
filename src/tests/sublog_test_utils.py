import difflib

from django.core.urlresolvers import reverse
from django.test.testcases import TestCase

TEST_FOLDER = '/Users/mmi/github/sublog/assets/test/'


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
    def get_index_page(self):
        return self.client.get(reverse('index'))

    def get_article_page(self, article_id):
        return self.client.get('/article/%s/' % article_id)

    def post_article(self, title, content, follow=True):
        return self.client.post('/article/', data={'title': title, 'content': content}, follow=follow)

    def post_comment(self, article_id, title, content, name, email):
        post_data = {
            'title': title,
            'name': name,
            'email': email,
            'content': content
        }
        return self.client.post('/article/%s/comment/' % article_id, data=post_data, follow=True)
