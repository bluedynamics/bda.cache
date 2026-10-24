from bda.cache import ICacheManager
from bda.cache import Memcached
from bda.cache import memcached
from bda.cache import MemcachedException
from bda.cache import MemcachedManager
from bda.cache.interfaces import IMemcachedProvider
from unittest import mock
import importlib.util
import sys
import types
import unittest
import zlib


SERVERS = ['127.0.0.1:11211']


class FakeClient:
    """In-memory replacement for ``memcache.Client``.

    Keeps the tests independent of a running memcached server.
    """

    stats = [
        ('127.0.0.1:11211 (1)', {'bytes': '40'}),
        ('127.0.0.1:11212 (1)', {'bytes': '25'}),
    ]

    def __init__(self, servers):
        self.servers = servers
        self.data = {}
        self.expiration_times = {}

    def get(self, key):
        return self.data.get(key)

    def set(self, key, value, time=0):
        self.data[key] = value
        self.expiration_times[key] = time

    def delete(self, key):
        self.data.pop(key, None)

    def flush_all(self):
        self.data.clear()

    def get_stats(self):
        return self.stats


def patch_python_memcached(testcase):
    patcher = mock.patch.multiple(
        memcached, Client=FakeClient, LIBMC=False, PYLIBMC=False
    )
    patcher.start()
    testcase.addCleanup(patcher.stop)


class TestMemcached(unittest.TestCase):
    def setUp(self):
        patch_python_memcached(self)
        self.provider = Memcached(SERVERS)
        self.client = self.provider._client

    def test_init(self):
        self.assertTrue(IMemcachedProvider.providedBy(self.provider))
        self.assertIsInstance(self.client, FakeClient)
        self.assertEqual(self.client.servers, SERVERS)
        self.assertEqual(self.provider.timeout, 0)

    def test_set_and_get(self):
        self.assertIsNone(self.provider['somekey'])
        self.assertEqual(self.provider.get('somekey', 'default'), 'default')
        self.provider['somekey'] = 'somevalue'
        self.assertEqual(self.provider['somekey'], 'somevalue')
        self.assertEqual(self.provider.get('somekey', 'default'), 'somevalue')

    def test_timeout_is_passed_as_expiration_time(self):
        self.provider['1'] = 1
        self.provider.timeout = 2
        self.provider['2'] = 2
        self.assertEqual(self.client.expiration_times, {'1': 0, '2': 2})

    def test_delete(self):
        self.provider['somekey'] = 'somevalue'
        del self.provider['somekey']
        self.assertIsNone(self.provider['somekey'])

    def test_reset(self):
        self.provider['1'] = 'Eins'
        self.provider['2'] = 'Zwei'
        self.provider.reset()
        self.assertEqual((self.provider['1'], self.provider['2']), (None, None))

    def test_size_sums_up_bytes_of_all_servers(self):
        self.assertEqual(self.provider.size(), 65)

    def test_keys_not_supported(self):
        with self.assertRaises(MemcachedException) as cm:
            self.provider.keys()
        self.assertEqual(
            str(cm.exception), "It's not possible to fetch keys from memcached"
        )

    def test_values_not_supported(self):
        with self.assertRaises(MemcachedException) as cm:
            self.provider.values()
        self.assertEqual(
            str(cm.exception), "It's not possible to fetch values from memcached"
        )


class TestMemcachedManager(unittest.TestCase):
    def setUp(self):
        patch_python_memcached(self)
        self.provider = Memcached(SERVERS)
        self.manager = ICacheManager(self.provider)

    def test_adapter_registered(self):
        self.assertIsInstance(self.manager, MemcachedManager)
        self.assertIs(self.manager.cache, self.provider)

    def test_set_timeout(self):
        self.manager.setTimeout(10)
        self.assertEqual(self.provider.timeout, 10)

    def test_set_and_get(self):
        self.manager.set('AnotherKey', 'AnotherValue')
        self.assertEqual(self.manager.get('AnotherKey'), 'AnotherValue')

    def test_get_force_reload(self):
        self.manager.set('AnotherKey', 'AnotherValue')
        self.assertIsNone(self.manager.get('AnotherKey', True))
        self.assertIsNone(self.manager.get('AnotherKey'))

    def test_get_data(self):
        calls = []

        def square(x):
            calls.append(x)
            return x * x

        self.assertEqual(self.manager.getData(square, '4', args=[4]), 16)
        self.assertEqual(self.manager.getData(square, '4', args=[4]), 16)
        self.assertEqual(calls, [4])
        self.assertEqual(self.manager.getData(square, '4', True, args=[4]), 16)
        self.assertEqual(self.manager.getData(square, '5', True, kwargs={'x': 5}), 25)
        self.assertEqual(calls, [4, 4, 5])
        self.assertEqual(self.manager.get('5'), 25)

    def test_delete(self):
        self.manager.set('5', 25)
        del self.manager['5']
        self.assertIsNone(self.manager.get('5'))

    def test_rem(self):
        self.manager.set('5', 25)
        self.manager.rem('5')
        self.assertIsNone(self.manager.get('5'))


def fake_module(name):
    module = types.ModuleType(name)
    module.Client = mock.Mock(name=f'{name}.Client')
    return module


def load_memcached_module(**modules):
    """Load a fresh copy of ``bda.cache.memcached``.

    The client library is selected at import time, the given ``modules``
    replace the installed ones meanwhile, ``None`` means not installed. The
    copy is not added to ``sys.modules`` and does not register its adapter.
    """
    spec = importlib.util.find_spec('bda.cache.memcached')
    module = importlib.util.module_from_spec(spec)
    with (
        mock.patch.dict(sys.modules, modules),
        mock.patch('zope.component.provideAdapter') as provide_adapter,
    ):
        spec.loader.exec_module(module)
    provide_adapter.assert_called_once_with(module.MemcachedManager)
    return module


class TestClientLibrarySelection(unittest.TestCase):
    def test_python_memcached(self):
        memcache = fake_module('memcache')
        module = load_memcached_module(libmc=None, pylibmc=None, memcache=memcache)
        self.assertFalse(module.LIBMC)
        self.assertFalse(module.PYLIBMC)
        provider = module.Memcached(SERVERS)
        memcache.Client.assert_called_once_with(SERVERS)
        provider['key'] = 'value'
        provider._client.set.assert_called_once_with('key', 'value', time=0)

    def test_libmc(self):
        libmc = fake_module('libmc')
        module = load_memcached_module(libmc=libmc, pylibmc=None)
        self.assertTrue(module.LIBMC)
        self.assertFalse(module.PYLIBMC)
        provider = module.Memcached(SERVERS)
        libmc.Client.assert_called_once_with(SERVERS, comp_threshold=10240, noreply=True)
        provider['key'] = 'value'
        provider._client.set.assert_called_once_with('key', 'value', time=0)

    def test_pylibmc(self):
        pylibmc = fake_module('pylibmc')
        module = load_memcached_module(libmc=None, pylibmc=pylibmc)
        self.assertFalse(module.LIBMC)
        self.assertTrue(module.PYLIBMC)
        provider = module.Memcached(SERVERS)
        pylibmc.Client.assert_called_once_with(SERVERS)
        provider['key'] = 'value'
        provider._client.set.assert_called_once_with(
            'key',
            'value',
            time=0,
            min_compress_len=1024000,
            compress_level=zlib.Z_BEST_SPEED,
        )

    def test_libmc_is_preferred_over_pylibmc(self):
        libmc = fake_module('libmc')
        pylibmc = fake_module('pylibmc')
        module = load_memcached_module(libmc=libmc, pylibmc=pylibmc)
        provider = module.Memcached(SERVERS)
        libmc.Client.assert_called_once_with(SERVERS, comp_threshold=10240, noreply=True)
        pylibmc.Client.assert_not_called()
        provider['key'] = 'value'
        provider._client.set.assert_called_once_with('key', 'value', time=0)
