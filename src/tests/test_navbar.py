from src.tests import get_toc, TITLE_1, CONTENT_1, get_article_id
from src.tests.sublog_test_utils import SublogTestCase
from sublog import settings

TOC_ENTRIES = ['Home', 'New article', 'About me']


class NavbarTests(SublogTestCase):
    def assertAllNavbarEntries(self, response, home_active, new_active, about_active):
        toc = get_toc(response)
        self.assertNavbarEntry('Home', home_active, toc[0])
        self.assertNavbarEntry('New Article', new_active, toc[1])
        self.assertNavbarEntry('About me', about_active, toc[2])

    def assertNavbarEntry(self, expected_label, expected_active, toc_entry):
        self.assertEquals(expected_label, toc_entry['label'])
        self.assertEquals(expected_active, toc_entry['is_active'])

    def test_index_page_highlighted(self):
        index = self.get_index_page()
        self.assertAllNavbarEntries(index, True, False, False)

    def test_new_article_page_highlighted(self):
        self.login()
        new_article_page = self.get_new_article_page()
        self.assertAllNavbarEntries(new_article_page, False, True, False)

    def test_article_page_no_entry_highlighted(self):
        self.login()
        article_page = self.post_article(TITLE_1, CONTENT_1)
        self.assertAllNavbarEntries(article_page, False, False, False)

    def test_about_me_page(self):
        self.login()
        article_id = get_article_id(self.post_article(TITLE_1, CONTENT_1))
        settings.ABOUT_ME_ID = article_id

        about_me = self.get_about_me_page()
        self.assertAllNavbarEntries(about_me, False, False, True)
