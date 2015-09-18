import django

from django.test.utils import setup_test_environment

from src.service.mail_gen import generate_mail_content
from src.tests.sublog_test_utils import SublogTestCase

setup_test_environment()
django.setup()


class TestMailGen(SublogTestCase):
    def test_create_mail(self):
        user_name = 'Test_user name'
        commenter = 'some anon user'
        title = 'Test article title'

        email = generate_mail_content(user_name, commenter, title)

        expected_content = self.read_file_content('test_mail_content.html')
        self.compare_contents(expected_content, email)
