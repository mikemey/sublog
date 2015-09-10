import difflib

from django.core.urlresolvers import reverse
from django.test import TestCase

from src.test_utils import get_articles, get_comments

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


def post_article(client, title, content, follow=True):
    return client.post('/article/', data={'title': title, 'content': content}, follow=follow)


class ViewTests(TestCase):
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


class ArticleViewTests(TestCase):
    def index_page(self):
        return self.client.get(reverse('index'))

    def test_index_view_with_no_articles(self):
        index = self.index_page()
        self.assertContains(index, 'No articles yet!')
        self.assertEquals(0, len(get_articles(index)))

    def test_index_view_with_two_articles(self):
        post_article(self.client, TITLE_1, CONTENT_1)
        post_article(self.client, TITLE_2, CONTENT_2)

        articles = get_articles(self.index_page())

        self.assertEquals(TITLE_2, articles[0]['title'])
        self.assertEquals(EXP_CONTENT_2, articles[0]['content'])
        self.assertEquals(TITLE_1, articles[1]['title'])
        self.assertEquals(EXP_CONTENT_1, articles[1]['content'])

    def test_post_article_redirects_to_article(self):
        post_article(self.client, TITLE_1, CONTENT_1)
        post_article(self.client, TITLE_2, CONTENT_2)

        response = post_article(self.client, NEW_TITLE, NEW_CONTENT, False)
        self.assertRedirects(response, '/article/3/')

    def test_post_article_shown_first(self):
        post_article(self.client, TITLE_1, CONTENT_1)
        post_article(self.client, NEW_TITLE, NEW_CONTENT)

        articles = get_articles(self.index_page())
        self.assertEquals(NEW_TITLE, articles[0]['title'])
        self.assertEquals(EXP_NEW_CONTENT, articles[0]['content'])
        self.assertEquals(TITLE_1, articles[1]['title'])
        self.assertEquals(EXP_CONTENT_1, articles[1]['content'])


class CommentsTests(TestCase):
    def article_page(self):
        return self.client.get('/article/1/')

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
        article_page = self.article_page()
        self.assertContains(article_page, 'No comments yet')
        self.assertEquals(0, len(get_comments(article_page)))

    def test_article_has_2_comments(self):
        post_article(self.client, TITLE_1, CONTENT_1)
        self.post_comment("", NEW_CONTENT, USER_NAME_1, 'email_1@ex.com')
        self.post_comment(TITLE_2, CONTENT_2, USER_NAME_2, 'email_2@ex.com')

        comments = get_comments(self.article_page())
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
