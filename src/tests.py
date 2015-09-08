import difflib

from django.core.urlresolvers import reverse

from django.test import TestCase

from src.models import Article
from src.test_utils import get_articles, get_comments
from views import parse_comment_post


class ViewTests(TestCase):
    def test_content_of_comment_correctly_passed(self):
        test_content = """before 1 newline
before 2 newlines

before 3 newlines


and one more line
end"""

        expected_content = """before 1 newline

before 2 newlines

before 3 newlines


and one more line

end"""

        post_data = {'name': 'whatever',
                     'email': 'bla@blu.com',
                     'title': 'bla@blu.com',
                     'content': test_content}

        parse_result = parse_comment_post(Article(), post_data)
        self.assertIsNone(parse_result.error_message)
        self.assertEquals(parse_result.comment.content.raw, expected_content,
                          self.compareMessage(parse_result.comment.content.raw, expected_content))

    def compareMessage(self, actual, expected):
        expected = expected.splitlines()
        actual = actual.splitlines()

        diff = difflib.unified_diff(expected, actual)
        diff_msg = ''.join(diff)

        self.assertTrue(diff_msg.__len__() == 0, "Content differs: \n%s" % diff_msg)


# =======================================================
# Test create articles:
# =======================================================

def create_article(title, content):
    return Article.objects.create(title=title, content=content)


TITLE_1 = 'title 1'
CONTENT_1 = 'content 1'
TITLE_2 = 'title 2'
CONTENT_2 = 'content 2'
NEW_TITLE = 'new title'
NEW_CONTENT = 'new content'


class ArticleViewTests(TestCase):
    def index_page(self):
        return self.client.get(reverse('index'))

    def test_index_view_with_no_articles(self):
        index = self.index_page()
        self.assertContains(index, 'No articles yet!')
        self.assertEqual(0, len(get_articles(index)))

    def test_index_view_with_two_articles(self):
        create_article(TITLE_1, CONTENT_1)
        create_article(TITLE_2, CONTENT_2)

        articles = get_articles(self.index_page())

        self.assertEqual(TITLE_2, articles[0]['title'])
        self.assertEqual(CONTENT_2, articles[0]['content'])
        self.assertEqual(TITLE_1, articles[1]['title'])
        self.assertEqual(CONTENT_1, articles[1]['content'])

    def test_post_article_shown_first(self):
        create_article(TITLE_1, CONTENT_1)

        response = self.client.post('/article/',
                                    data={'title': NEW_TITLE, 'content': NEW_CONTENT},
                                    follow=False)

        self.assertRedirects(response, '/article/2/')

        articles = get_articles(self.index_page())
        self.assertEqual(NEW_TITLE, articles[0]['title'])
        self.assertEqual(NEW_CONTENT, articles[0]['content'])
        self.assertEqual(TITLE_1, articles[1]['title'])
        self.assertEqual(CONTENT_1, articles[1]['content'])


USER_NAME_1 = 'user 1'
USER_NAME_2 = 'user 2'


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
        response = self.client.post('/article/1/comment/',
                                    data=post_data,
                                    follow=False)
        self.assertRedirects(response, '/article/1/#comments')

    def test_article_has_no_comments(self):
        create_article(TITLE_1, CONTENT_1)
        article_page = self.article_page()
        self.assertContains(article_page, 'No comments yet')
        self.assertEqual(0, len(get_comments(article_page)))

    def test_article_has_2_comments(self):
        create_article(TITLE_1, CONTENT_1)
        self.post_comment("", NEW_CONTENT, USER_NAME_1, 'email_1@ex.com')
        self.post_comment(TITLE_2, CONTENT_2, USER_NAME_2, 'email_2@ex.com')

        comments = get_comments(self.article_page())
        self.assert_comment(comments[0], TITLE_2, USER_NAME_2, CONTENT_2)
        self.assert_comment(comments[1], "-- no title --", USER_NAME_1, NEW_CONTENT)

    def assert_comment(self, comment, title, name, content):
        self.assertEqual(title, comment['title'])
        self.assertEqual(name, comment['name'])
        self.assertEqual(content, comment['content'])
