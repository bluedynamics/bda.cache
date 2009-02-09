#
# Copyright 2008, Blue Dynamics Alliance, Austria - http://bluedynamics.com
#
# GNU General Public Licence Version 2 or later

__author__ = """Robert Niederreiter <rnix@squarewave.at>"""
__docformat__ = 'plaintext'

"""
Module memcache.

This module provides fuctionallity for caching objects in a memcache server.
"""

from zope.interface import implements
from zope.component import adapts

from interfaces import ICacheManager
from interfaces import ICacheProvider
from interfaces import CacheException

from interfaces import IMemcachedProvider

class MemcachedException(CacheException): pass

class Memcached(object):
    
    implements(IMemcachedProvider)
    
    def __init__(self, foo):
        pass
    
    def reset(self):
        pass
    
    def size(self):
        pass
        
    def keys(self):
        pass
                
    def values(self):
        pass
    
    def get(self, key, default=None):
        pass
    
    def __getitem__(self, key):
        pass
    
    def __setitem__(self, key, object):
        pass
    
    def __delitem__(self, key):
        pass

class MemcachedManager(object):
    
    implements(ICacheManager)
    adapts(ICacheProvider)
    
    def __init__(self, context):
        self.cache = context
    
    def setTimeout(self, timeout):
        pass # XXX: write log entry ?
    
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
        del self.cache[key]