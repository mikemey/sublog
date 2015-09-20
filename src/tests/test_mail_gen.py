from src.service.mail_gen import render_email_body, with_context_from
from src.tests.sublog_test_utils import SublogTestCase


class TestMailGen(SublogTestCase):
    def test_create_mail(self):
        ctx = {
            'username': 'Test_user name',
            'commenter': 'some anon user',
            'title': 'Test article title',
            'article_id': '3',
        }
        email = render_email_body(ctx)

        expected_content = self.read_file_content('test_render_mail_content.html')
        self.compare_contents(expected_content, email)

    def test_create_context(self):
        test_id = 234
        test_title = 'article test title 123'
        test_user_name = 'bla_234'
        test_commenter_name = 'commenter name'

        art = MicroMock(id=test_id, title=test_title, author=MicroMock(username=test_user_name, first_name=''))
        comment = MicroMock(user_name=test_commenter_name)

        ctx = with_context_from(art, comment)
        self.assertEquals(test_id, ctx.get('article_id'))
        self.assertEquals(test_user_name, ctx.get('username'))
        self.assertEquals(test_commenter_name, ctx.get('commenter'))
        self.assertEquals(test_title, ctx.get('title'))


class MicroMock(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
