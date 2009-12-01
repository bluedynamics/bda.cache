# Copyright 2009, Blue Dynamics Alliance, Austria - http://bluedynamics.com
# GNU General Public Licence Version 2 or later

from zope.interface import implements
from zope.component import adapts
from zope.component import provideAdapter
from interfaces import ICacheManager
from interfaces import ICacheProvider
from interfaces import INullCacheProvider

class NullCache(object):
    """Dummy implementation which does nothing and can be used as fallback. 
    """
    
    implements(INullCacheProvider)
    
    def __init__(self):
        pass
    
    def reset(self):
        pass
    
    def size(self):
        return 0

    def keys(self):
        raise NotImplementedError, \
              "It's not possible to fetch keys from nothing"
                
    def values(self):
        raise NotImplementedError, \
              "It's not possible to fetch values from nothing"
    
    def get(self, key, default=None):
        return None
    
    def __getitem__(self, key):
        return None
    
    def __setitem__(self, key, object):
        pass
    
    def __delitem__(self, key):
        pass

class NullCacheManager(object):
    
    implements(ICacheManager)
    adapts(INullCacheProvider)
    
    def __init__(self, context):
        pass
    
    def setTimeout(self, timeout):
        pass
    
    def getData(self, func, key, force_reload=False, args=[], kwargs={}):
        return func(*args, **kwargs)
    
    def get(self, key, force_reload=False):
        return None
    
    def set(self, key, item):
        pass
    
    def rem(self, key):
        pass
    
    def __delitem__(self, key):
        pass
    
provideAdapter(NullCacheManager)