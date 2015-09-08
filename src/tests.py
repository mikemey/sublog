import difflib

from django.test import TestCase

from src.models import Article
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
