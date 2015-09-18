from src.tests.sublog_test_utils import SublogTestCase
from src.service.sycache import SyCache


class DraftTests(SublogTestCase):
    def test_get_not_existing_key(self):
        sychache = SyCache()
        self.assertIsNone(sychache.get('some key'))

    def test_get_default_for_non_existing_key(self):
        test_default = {'data': 'test'}
        sychache = SyCache(test_default)
        self.assertEquals(test_default, sychache.get('some key'))

    def test_get_different_values_for_different_keys(self):
        sychache = SyCache()
        sychache.set('key1', 'data1')
        sychache.set('key2', 'data2')

        self.assertEquals('data1', sychache.get('key1'))
        self.assertEquals('data2', sychache.get('key2'))
        self.assertIsNone(sychache.get('key3'))

    def test_invalidate_one_key(self):
        sychache = SyCache('def')
        sychache.set('key1', 'data1')
        sychache.set('key2', 'data2')

        sychache.invalidate('key1')
        self.assertEquals('def', sychache.get('key1'))
        self.assertEquals('data2', sychache.get('key2'))
