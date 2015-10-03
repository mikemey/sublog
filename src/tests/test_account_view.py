from src.tests import get_user_name, get_user_first_name, get_user_email
from src.tests.sublog_test_utils import SublogTestCase, create_test_user

USER_NAME_1 = 'user_1'
USER_MAIL_1 = 'mail1@bla.com'
USER_FIRST_1 = 'firstname_1'
USER_NAME_2 = 'user_2'
USER_MAIL_2 = 'mail2@bla.com'
USER_FIRST_2 = 'firstname_2'


class AccountViewTest(SublogTestCase):
    def setUp(self):
        create_test_user(USER_NAME_1, 'pwd', USER_MAIL_1, USER_FIRST_1)
        create_test_user(USER_NAME_2, 'pwd', USER_MAIL_2, USER_FIRST_2)

    def test_account_data(self):
        self.login(USER_NAME_1)
        account_page = self.get_account_page()
        self.assertEquals(USER_NAME_1, get_user_name(account_page))
        self.assertEquals(USER_FIRST_1, get_user_first_name(account_page))
        self.assertEquals(USER_MAIL_1, get_user_email(account_page))

    def test_email_notification(self):
        self.fail('not yet implemented')
