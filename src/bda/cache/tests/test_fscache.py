from bda.cache import FSCache
from bda.cache import FSCacheException
from bda.cache import FSCacheManager
from bda.cache import ICacheManager
from bda.cache.interfaces import IFSCacheProvider
from unittest import mock
import os
import shutil
import tempfile
import time
import unittest


class FSCacheTestCase(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tempdir)
        self.cachedir = os.path.join(self.tempdir, 'cache')
        os.mkdir(self.cachedir)

    def listdir(self, *path):
        return sorted(os.listdir(os.path.join(self.cachedir, *path)))


class TestFSCacheInit(FSCacheTestCase):
    def test_relative_path(self):
        with self.assertRaises(FSCacheException) as cm:
            FSCache('notabspath')
        self.assertEqual(
            str(cm.exception),
            "Cannot initialize cache. 'notabspath' is not an absolute path.",
        )

    def test_missing_directory(self):
        path = os.path.join(self.tempdir, 'missing')
        with self.assertRaises(FSCacheException) as cm:
            FSCache(path)
        self.assertEqual(
            str(cm.exception), f"Cannot initialize cache. Directory '{path}' not exists."
        )

    def test_not_a_directory(self):
        path = os.path.join(self.tempdir, 'file')
        with open(path, 'w') as f:
            f.write('hallo')
        with self.assertRaises(FSCacheException) as cm:
            FSCache(path)
        self.assertEqual(
            str(cm.exception), f"Cannot initialize cache. '{path}' is not a Directory."
        )

    def test_create_missing_directory(self):
        path = os.path.join(self.tempdir, 'a', 'b')
        cache = FSCache(path, createDirIfNotExist=True)
        self.assertTrue(os.path.isdir(path))
        self.assertEqual(cache.cachedir, path)

    def test_create_existing_directory(self):
        cache = FSCache(self.cachedir, createDirIfNotExist=True)
        self.assertEqual(cache.cachedir, self.cachedir)

    def test_defaults(self):
        cache = FSCache(self.cachedir)
        self.assertTrue(IFSCacheProvider.providedBy(cache))
        self.assertEqual(cache.protocol, 2)
        self.assertEqual(cache.size(), 0)


class TestFSCache(FSCacheTestCase):
    def setUp(self):
        super().setUp()
        self.cache = FSCache(self.cachedir)

    def test_dotted_key_is_stored_in_directory_tree(self):
        self.cache['user.section.msg'] = 'message'
        self.assertEqual(self.listdir(), ['user'])
        self.assertEqual(self.listdir('user'), ['section'])
        self.assertEqual(self.listdir('user', 'section'), ['msg.'])
        self.assertEqual(self.cache['user.section.msg'], 'message')

    def test_key_may_be_part_of_another_key(self):
        # Every file gets a trailing dot, thus 'user' is stored at 'user.'
        # next to the directory 'user' containing 'user.section'.
        self.cache['user'] = {'key': 'user'}
        self.cache['user.section'] = {'key': 'user.section'}
        self.assertEqual(self.listdir(), ['user', 'user.'])
        self.assertEqual(self.cache['user'], {'key': 'user'})
        self.assertEqual(self.cache['user.section'], {'key': 'user.section'})

    def test_missing_key(self):
        self.assertIsNone(self.cache['notavailable'])
        self.assertIsNone(self.cache.get('notavailable'))
        self.assertEqual(self.cache.get('notavailable', 'works'), 'works')

    def test_overwrite(self):
        self.cache['user.section.msg'] = 'message'
        self.cache['user.section.msg'] = {'anykey': 'anydata'}
        self.assertEqual(self.cache.get('user.section.msg'), {'anykey': 'anydata'})

    def test_keys_and_values(self):
        self.cache['anythingelse'] = 'anythingelse'
        self.cache['user'] = 'user'
        self.cache['user.section'] = ['user.section']
        self.cache['user.section.msg0'] = {'msg': 0}
        self.cache['user.section.msg1'] = {'msg': 1}
        self.assertEqual(
            sorted(self.cache.keys()),
            [
                'anythingelse',
                'user',
                'user.section',
                'user.section.msg0',
                'user.section.msg1',
            ],
        )
        self.assertCountEqual(
            self.cache.values(),
            ['anythingelse', 'user', ['user.section'], {'msg': 0}, {'msg': 1}],
        )

    def test_delete_removes_empty_directories(self):
        self.cache['user.section'] = 'section'
        self.cache['user.section.msg0'] = 'msg0'
        self.cache['user.section.msg1'] = 'msg1'
        del self.cache['user.section.msg0']
        self.assertEqual(self.listdir('user', 'section'), ['msg1.'])
        del self.cache['user.section.msg1']
        self.assertEqual(self.listdir('user'), ['section.'])
        del self.cache['user.section']
        self.assertEqual(self.listdir(), [])

    def test_delete_removes_empty_directories_recursively(self):
        self.cache['1.2.3.4'] = 'value'
        self.assertEqual(self.listdir('1', '2', '3'), ['4.'])
        del self.cache['1.2.3.4']
        self.assertEqual(self.listdir(), [])

    def test_delete_keeps_non_empty_directories(self):
        self.cache['user.whatever.object'] = 'something'
        self.cache['user.other'] = 'other'
        del self.cache['user.whatever.object']
        self.assertEqual(self.listdir(), ['user'])
        self.assertEqual(self.listdir('user'), ['other.'])

    def test_delete_missing_key(self):
        del self.cache['notavailable']
        del self.cache['not.available']
        self.assertEqual(self.listdir(), [])

    def test_reset(self):
        for key in ['1', '2', '1.1', '1.1.1', '1.2.3.1', '1.2.3.2']:
            self.cache[key] = ['something']
        self.assertEqual(
            sorted(self.cache.keys()), ['1', '1.1', '1.1.1', '1.2.3.1', '1.2.3.2', '2']
        )
        self.cache.reset()
        self.assertEqual(self.cache.keys(), [])


class TestFSCacheManager(FSCacheTestCase):
    def setUp(self):
        super().setUp()
        self.cache = FSCache(self.cachedir)
        self.manager = ICacheManager(self.cache)

    def test_adapter_registered(self):
        self.assertIsInstance(self.manager, FSCacheManager)
        self.assertIs(self.manager.cache, self.cache)
        self.assertEqual(self.manager.timeout, 300)

    def test_set_timeout(self):
        self.manager.setTimeout(10)
        self.assertEqual(self.manager.timeout, 10)

    def test_set_and_get(self):
        self.manager.set('foo', 'bar')
        self.assertEqual(self.manager.get('foo'), 'bar')
        self.assertEqual(list(self.cache['creationmap']), ['foo'])

    def test_set_without_creationtime(self):
        # Items without creation time are considered as timed out.
        self.manager.set('foo', 'bar', set_creationtime=False)
        self.assertEqual(self.cache['foo'], 'bar')
        self.assertIsNone(self.cache['creationmap'])
        self.assertIsNone(self.manager.get('foo'))
        self.assertIsNone(self.cache['foo'])

    def test_get_missing_creationtime(self):
        self.manager.set('foo', 'bar')
        self.manager.set('baz', 'qux', set_creationtime=False)
        self.assertIsNone(self.manager.get('baz'))
        self.assertIsNone(self.cache['baz'])
        self.assertEqual(list(self.cache['creationmap']), ['foo'])

    def test_get_timed_out(self):
        self.manager.set('foo', 'bar')
        with mock.patch('time.time', return_value=time.time() + 301):
            self.assertIsNone(self.manager.get('foo'))
        self.assertIsNone(self.cache['foo'])
        self.assertEqual(self.cache['creationmap'], {})

    def test_get_force_reload(self):
        self.manager.set('foo', 'bar')
        self.assertIsNone(self.manager.get('foo', force_reload=True))
        self.assertIsNone(self.cache['foo'])
        self.assertEqual(self.cache['creationmap'], {})

    def test_get_data(self):
        calls = []

        def square(x):
            calls.append(x)
            return x * x

        self.assertEqual(self.manager.getData(square, '4', args=[4]), 16)
        self.assertEqual(self.manager.getData(square, '4', args=[4]), 16)
        self.assertEqual(calls, [4])
        self.assertEqual(self.manager.getData(square, '4', True, args=[4]), 16)
        self.assertEqual(self.manager.getData(square, '5', kwargs={'x': 5}), 25)
        self.assertEqual(calls, [4, 4, 5])

    def test_rem(self):
        self.manager.set('foo', 'bar')
        self.manager.set('baz', 'qux')
        self.manager.rem('foo')
        self.assertIsNone(self.cache['foo'])
        self.assertEqual(list(self.cache['creationmap']), ['baz'])
        del self.manager['baz']
        self.assertIsNone(self.cache['baz'])
        self.assertEqual(self.cache['creationmap'], {})

    def test_rem_without_creationtime(self):
        self.manager.set('foo', 'bar', set_creationtime=False)
        self.manager.rem('foo')
        self.assertIsNone(self.cache['foo'])
        self.assertIsNone(self.cache['creationmap'])
