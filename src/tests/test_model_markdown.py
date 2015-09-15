from src.tests import TITLE_1, get_article_id, get_articles, get_comments
from src.tests.sublog_test_utils import SublogTestCase


class ModelMarkdownTests(SublogTestCase):
    def setUp(self):
        self.input = self.read_file_content('full_markdown_input.md')
        self.expected = self.read_file_content('full_markdown_expected.html')

        self.login()
        self.article_page = self.post_article(TITLE_1, self.input)
        self.article_id = get_article_id(self.article_page)

    def test_article_markdown(self):
        actual = get_articles(self.article_page)[0]['content']
        self.compare_contents(self.expected, actual)

    def test_comment_markdown(self):
        comment = self.post_comment(self.article_id, TITLE_1, self.input, 'hello', 'lala@lulu.com')
        actual = get_comments(comment)[0]['content']
        self.compare_contents(self.expected, actual)
