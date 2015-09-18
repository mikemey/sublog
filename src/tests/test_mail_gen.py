from src.service.mail_gen import mail_content
from src.tests.sublog_test_utils import SublogTestCase


class TestMailGen(SublogTestCase):
    def test_create_mail(self):
        user_name = 'Test_user name'
        commenter = 'some anon user'
        title = 'Test article title'
        article_id = '3'

        email = mail_content(article_id, user_name, commenter, title)

        expected_content = self.read_file_content('test_mail_content.html')
        self.compare_contents(expected_content, email)
