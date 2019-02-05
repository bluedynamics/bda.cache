# Copyright 2009, Blue Dynamics Alliance, Austria - http://bluedynamics.com
# GNU General Public Licence Version 2 or later
"""
Module memcache.

This module provides fuctionallity for caching objects in a memcache server.
"""

from bda.cache.interfaces import CacheException
from bda.cache.interfaces import ICacheManager
from bda.cache.interfaces import ICacheProvider
from bda.cache.interfaces import IMemcachedProvider
from zope.component import adapter
from zope.component import provideAdapter
from zope.interface import implementer


try:
    from libmc import Client
    import six.moves.cPickle

    LIBMC = True
except ImportError:
    LIBMC = False
try:
    from pylibmc import Client
    import zlib

    PYLIBMC = True
except ImportError:
    PYLIBMC = False

if not (LIBMC or PYLIBMC):
    from memcache import Client


class MemcachedException(CacheException):
    pass


@implementer(IMemcachedProvider)
class Memcached(object):
    def __init__(self, servers):
        """Initialize memcached.
        @param servers: an array of servers. Servers can be passed in two forms:
            1. Strings of the form host:port (implies a default weight of 1).
            2. Tuples of the form (host:port, weight) (weight as integer)
        """
        if LIBMC:
            self._client = Client(servers, comp_threshold=10240, noreply=True)
        else:
            self._client = Client(servers)
        self.timeout = 0

    def reset(self):
        self._client.flush_all()

    def size(self):
        bytes = 0
        stats = self._client.get_stats()
        for name, stat in stats:
            bytes += int(stat["bytes"])
        return bytes

    def keys(self):
        raise MemcachedException(
            "It's not possible to fetch keys from memcached"
        )

    def values(self):
        raise MemcachedException(
            "It's not possible to fetch values from memcached"
        )

    def get(self, key, default=None):
        value = self._client.get(key)
        if value is not None:
            return value
        return default

    def __getitem__(self, key):
        return self._client.get(key)

    def __setitem__(self, key, object):
        if PYLIBMC and not LIBMC:
            self._client.set(
                key,
                object,
                time=self.timeout,
                min_compress_len=1024000,
                compress_level=zlib.Z_BEST_SPEED,
            )
        else:
            self._client.set(key, object, time=self.timeout)

    def __delitem__(self, key):
        self._client.delete(key)


@implementer(ICacheManager)
@adapter(IMemcachedProvider)
class MemcachedManager(object):
    def __init__(self, context):
        self.cache = context

    def setTimeout(self, timeout):
        self.cache.timeout = timeout

    def getData(self, func, key, force_reload=False, args=[], kwargs={}):
        ret = self.get(key, force_reload)
        if ret is None:
            ret = func(*args, **kwargs)
            self.set(key, ret)
        return ret

    def get(self, key, force_reload=False):
        if force_reload:
            del self.cache[key]
            return None
        return self.cache.get(key, None)

    def set(self, key, item):
        self.cache[key] = item

    def rem(self, key):
        """deprecated, use __delitem___"""
        del self.cache[key]

    def __delitem__(self, key):
        del self.cache[key]


provideAdapter(MemcachedManager)
