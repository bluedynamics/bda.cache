from bda.cache import ICacheManager
from bda.cache import NullCache
from bda.cache import NullCacheManager
from bda.cache.interfaces import INullCacheProvider
import unittest


class TestNullCache(unittest.TestCase):
    def test_provides_null_cache_provider(self):
        self.assertTrue(INullCacheProvider.providedBy(NullCache()))

    def test_is_always_empty(self):
        provider = NullCache()
        provider['foo'] = object()
        self.assertIsNone(provider['foo'])
        self.assertIsNone(provider.get('foo'))
        self.assertIsNone(provider.get('foo', 'default'))
        self.assertEqual(provider.size(), 0)
        provider.reset()
        del provider['foo']

    def test_keys_not_supported(self):
        with self.assertRaises(NotImplementedError) as cm:
            NullCache().keys()
        self.assertEqual(
            str(cm.exception), "It's not possible to fetch keys from nothing"
        )

    def test_values_not_supported(self):
        with self.assertRaises(NotImplementedError) as cm:
            NullCache().values()
        self.assertEqual(
            str(cm.exception), "It's not possible to fetch values from nothing"
        )


class TestNullCacheManager(unittest.TestCase):
    def test_adapter_registered(self):
        manager = ICacheManager(NullCache())
        self.assertIsInstance(manager, NullCacheManager)

    def test_never_caches(self):
        manager = ICacheManager(NullCache())
        manager.setTimeout(0)
        manager.set('foo', object())
        self.assertIsNone(manager.get('foo'))
        manager.rem('foo')
        del manager['foo']

    def test_get_data_always_calls_function(self):
        calls = []

        def func(*args, **kwargs):
            calls.append((args, kwargs))
            return 'result'

        manager = ICacheManager(NullCache())
        result = manager.getData(func, 'foo', args=[1], kwargs={'a': 2})
        self.assertEqual(result, 'result')
        manager.getData(func, 'foo', args=[1], kwargs={'a': 2})
        self.assertEqual(calls, [((1,), {'a': 2}), ((1,), {'a': 2})])
