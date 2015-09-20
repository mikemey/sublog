from django.template.context import Context

from src.service.mail_gen import render_email_body
from src.tests.sublog_test_utils import SublogTestCase


class TestMailGen(SublogTestCase):
    def test_create_mail(self):
        ctx = Context({
            'user_name': 'Test_user name',
            'commenter': 'some anon user',
            'title': 'Test article title',
            'article_id': '3',
        })
        email = render_email_body(ctx)

        expected_content = self.read_file_content('test_render_mail_content.html')
        self.compare_contents(expected_content, email)
