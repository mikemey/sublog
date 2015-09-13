import difflib

from django.core.urlresolvers import reverse
from django.test import TestCase

from src.test_utils import get_articles, get_comments, get_version
from sublog import settings

TEST_FOLDER = 'assets/test/'

TITLE_1 = 'title 1'
CONTENT_1 = 'content 1'
EXP_CONTENT_1 = '<p>content 1</p>'

TITLE_2 = 'title 2'
CONTENT_2 = 'content 2'
EXP_CONTENT_2 = '<p>content 2</p>'

NEW_TITLE = 'new title'
NEW_CONTENT = 'new content'
EXP_NEW_CONTENT = '<p>new content</p>'

USER_NAME_1 = 'user 1'
USER_NAME_2 = 'user 2'


def test_file_content(file_name):
    return open(TEST_FOLDER + file_name).read()


def compare_contents(test, expected, actual):
    expected = expected.splitlines()
    actual = actual.splitlines()

    diff = difflib.unified_diff(expected, actual)
    diff_msg = ''.join(diff)

    test.assertEquals(0, len(diff_msg), "Content differs: \n%s" % diff_msg)


def get_index_page(client):
    return client.get(reverse('index'))


def get_article_page(client, article_id):
    return client.get('/article/%s/' % article_id)


def post_article(client, title, content, follow=True):
    return client.post('/article/', data={'title': title, 'content': content}, follow=follow)


class AuxiliaryEndpointsTests(TestCase):
    def ping_response(self, user_agent):
        header = {'HTTP_USER_AGENT': user_agent} if user_agent else {}
        return self.client.get('/ping/', **header)

    def test_health_check_accepts_UC_Browser(self):
        user_agent = "UCBrowser1.0.0"
        self.assertEquals('{ "status": "ok" }', self.ping_response(user_agent).content)

    def test_health_check_accepts_curl_user_agent(self):
        user_agent = "curl/7.43.0"
        self.assertEquals('{ "status": "ok" }', self.ping_response(user_agent).content)

    def test_health_check_refuses_no_user_agent(self):
        self.assertEquals(404, self.ping_response(None).status_code)

    def test_health_check_refuses_normal_user_agent(self):
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0"
        self.assertEquals(404, self.ping_response(user_agent).status_code)


class IndexViewTests(TestCase):
    def test_index_view_with_no_articles(self):
        index = get_index_page(self.client)
        self.assertContains(index, 'No articles yet!')
        self.assertEquals(0, len(get_articles(index)))

    def test_index_view_with_two_articles(self):
        post_article(self.client, TITLE_1, CONTENT_1)
        post_article(self.client, TITLE_2, CONTENT_2)

        articles = get_articles(get_index_page(self.client))

        self.assertEquals(TITLE_2, articles[0]['title'])
        self.assertEquals(EXP_CONTENT_2, articles[0]['content'])
        self.assertEquals(TITLE_1, articles[1]['title'])
        self.assertEquals(EXP_CONTENT_1, articles[1]['content'])

    def test_post_article_response_code(self):
        response = post_article(self.client, NEW_TITLE, NEW_CONTENT, False)
        self.assertEquals(302, response.status_code)

    def test_post_article_redirects_to_article(self):
        post_article(self.client, TITLE_1, CONTENT_1)
        post_article(self.client, TITLE_2, CONTENT_2)

        response = post_article(self.client, NEW_TITLE, NEW_CONTENT, False)
        self.assertRedirects(response, '/article/3/')

    def test_post_article_shown_first(self):
        post_article(self.client, TITLE_1, CONTENT_1)
        post_article(self.client, NEW_TITLE, NEW_CONTENT)

        articles = get_articles(get_index_page(self.client))
        self.assertEquals(NEW_TITLE, articles[0]['title'])
        self.assertEquals(EXP_NEW_CONTENT, articles[0]['content'])
        self.assertEquals(TITLE_1, articles[1]['title'])
        self.assertEquals(EXP_CONTENT_1, articles[1]['content'])


class ArticleViewTest(TestCase):
    def setUp(self):
        self.article_section = 'new line\nabc def ghi jkl\n\nmno pqr stu vwx\n'
        self.full_content = self.article_section * 10
        self.article_page = post_article(self.client, TITLE_1, self.full_content)

    def test_short_version_on_index_page(self):
        short_length = len(self.article_section * 6) + len('</p><p>') * 6 + len('...') + 1
        actual_content = self.assert_content_length(short_length, get_index_page(self.client))
        self.assertTrue(actual_content.strip().endswith('...</p>'))

    def test_long_version_on_article_page(self):
        full_length = len(self.full_content) + len('</p><p>') * 10 - 4
        self.assert_content_length(full_length, self.article_page)

    def assert_content_length(self, expected_length, page):
        article = get_articles(page)[0]
        actual_content = article['content']
        self.assertEquals(expected_length, len(actual_content))
        return actual_content


class CommentsTests(TestCase):
    def post_comment(self, title, content, name, email):
        post_data = {
            'title': title,
            'name': name,
            'email': email,
            'content': content
        }
        response = self.client.post('/article/1/comment/', data=post_data)
        self.assertRedirects(response, '/article/1/#comments')

    def test_article_has_no_comments(self):
        post_article(self.client, TITLE_1, CONTENT_1)
        article_page = get_article_page(self.client, 1)
        self.assertContains(article_page, 'No comments yet')
        self.assertEquals(0, len(get_comments(article_page)))

    def test_article_has_2_comments(self):
        post_article(self.client, TITLE_1, CONTENT_1)
        self.post_comment("", NEW_CONTENT, USER_NAME_1, 'email_1@ex.com')
        self.post_comment(TITLE_2, CONTENT_2, USER_NAME_2, 'email_2@ex.com')

        comments = get_comments(get_article_page(self.client, 1))
        self.assert_comment(comments[0], TITLE_2, USER_NAME_2, CONTENT_2)
        self.assert_comment(comments[1], "-- no title --", USER_NAME_1, NEW_CONTENT)

    def assert_comment(self, comment, title, name, content):
        self.assertEquals(title, comment['title'])
        self.assertEquals(name, comment['name'])
        self.assertEquals(content, comment['content'])


class PreviewMarkdownTests(TestCase):
    def markdown_response(self, post_data=None):
        response = self.client.post('/markdown/', data=post_data, content_type='text/markdown')
        self.assertEquals(200, response.status_code)
        self.assertEquals('text/html', response['Content-Type'])
        return response.content

    def test_empty_markdown(self):
        response = self.markdown_response('')
        self.assertEquals(0, len(response))

    def test_minimal_markdown(self):
        response = self.markdown_response('**bold**')
        self.assertEquals("<p><strong>bold</strong></p>", response)

    def test_escapes_html(self):
        response = self.markdown_response('<h2>huge</h2>')
        self.assertEquals("<p>&lt;h2&gt;huge&lt;/h2&gt;</p>", response)

    def test_full_markdown(self):
        input_content = test_file_content('full_markdown_input.md')
        expected = test_file_content('full_markdown_expected.html')
        compare_contents(self, expected, self.markdown_response(input_content))


test_version = 'tv1.0'
settings.SU_VERSION = test_version


class VersionTests(TestCase):
    def test_version_on_index_page(self):
        index = get_index_page(self.client)
        self.assertEquals(test_version, get_version(index))

    def test_version_on_article_page(self):
        post_article(self.client, TITLE_1, CONTENT_1)
        article_page = get_article_page(self.client, 1)
        self.assertEquals(test_version, get_version(article_page))

    def test_version_after_posting_article_redirect(self):
        new_article = post_article(self.client, NEW_TITLE, NEW_CONTENT)
        self.assertEquals(test_version, get_version(new_article))
