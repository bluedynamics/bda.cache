#
# Copyright 2008, Blue Dynamics Alliance, Austria - http://bluedynamics.com
#
# GNU General Public Licence Version 2 or later

__author__ = """Robert Niederreiter <rnix@squarewave.at>"""
__docformat__ = 'plaintext'

import logging
logger = logging.getLogger('bda.cache.cachemanager')

import time
from zope.interface import implements
from zope.component import adapts

from interfaces import ICacheManager
from interfaces import ICacheProvider

class CacheManager(object):
    """XXX: call this FSCacheManager.
    """
    
    implements(ICacheManager)
    adapts(ICacheProvider)
    
    def __init__(self, context):
        self.timeout = 300 # defaults to 300 seconds
        self.cache = context
    
    def setTimeout(self, timeout):
        self.timeout = timeout
    
    def getData(self, func, key, force_reload=False, args=[], kwargs={}):
        #from_cache = True
        ret = self.get(key, force_reload)
        if ret is None:
            #from_cache = False
            ret = func(*args, **kwargs)
            self.set(key, ret)
        return ret
    
    def get(self, key, force_reload=False):
        if force_reload or self._isTimedOut(key):
            del self.cache[key]
            creationmap = self.cache.get('creationmap', None)
            if creationmap is not None and creationmap.has_key(key):
                del creationmap[key]
                self.cache['creationmap'] = creationmap
            return None
        return self.cache.get(key, None)
    
    def set(self, key, item, set_creationtime=True):
        self.cache[key] = item
        if not set_creationtime:
            return
        creationmap = self.cache.get('creationmap', None)
        if not creationmap:
            creationmap = dict()
        creationmap[key] = time.time()
        self.cache['creationmap'] = creationmap
    
    def rem(self, key):
        del self.cache[key]
        creationmap = self.cache.get('creationmap', None)
        if creationmap is not None and creationmap.has_key(key):
            del creationmap[key]
            self.cache['creationmap'] = creationmap
    
    def _isTimedOut(self, key):
        """Return wether the item with key is timed out or not.
        """
        cur = time.time()
        creationmap = self.cache.get('creationmap', None)
        if not creationmap:
            return True
        creationtime = creationmap.get(key, None)
        if not creationtime or creationtime + self.timeout < cur:
            return True
        return False 

FSCacheManager = CacheManager

class MemcacheManager(object):
    
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