# Copyright 2009, Blue Dynamics Alliance, Austria - http://bluedynamics.com
# GNU General Public Licence Version 2 or later
"""
Module memcache.

This module provides fuctionallity for caching objects in a memcache server.
"""

from zope.interface import implements
from zope.component import adapts
from zope.component import provideAdapter
from interfaces import ICacheManager
from interfaces import ICacheProvider
from interfaces import CacheException
from interfaces import IMemcachedProvider
from memcache import Client 

class MemcachedException(CacheException): pass

class Memcached(object):
    
    implements(IMemcachedProvider)
    
    def __init__(self, servers):
        """Initialize memcached.
        @param servers: an array of servers. Servers can be passed in two forms:
            1. Strings of the form host:port (implies a default weight of 1).
            2. Tuples of the form (host:port, weight) (weight as integer)
        """
        self._client = Client(servers)
        self.timeout = 0
          
    def reset(self):
        self._client.flush_all()
    
    def size(self):
        bytes = 0
        stats = self._client.get_stats()
        for name, stat in stats:
            bytes+=int(stat['bytes'])
        return bytes

    def keys(self):
        raise MemcachedException, \
              "It's not possible to fetch keys from memcached"
                
    def values(self):
        raise MemcachedException, \
              "It's not possible to fetch values from memcached"
    
    def get(self, key, default=None):
        value = self._client.get(key)
        if value is not None:
            return value 
        return default
    
    def __getitem__(self, key):
        return self._client.get(key)
    
    def __setitem__(self, key, object):
        self._client.set(key, object, time=self.timeout)
    
    def __delitem__(self, key):
        self._client.delete(key)

class MemcachedManager(object):
    
    implements(ICacheManager)
    adapts(IMemcachedProvider)
    
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