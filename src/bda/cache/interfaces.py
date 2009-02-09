#
# Copyright 2008, Blue Dynamics Alliance, Austria - http://bluedynamics.com
#
# GNU General Public Licence Version 2 or later

__author__ = """Robert Niederreiter <rnix@squarewave.at>"""
__docformat__ = 'plaintext'

from zope.interface import Interface

class CacheException(Exception): pass

class ICacheVary(Interface):
    """This interface describes an API for manipulating objects inside a cache.
    """
    
    def vary(*args, **kwargs):
        """Manipulate objects inside the cache.
        """

class ICacheManager(Interface):
    """This interface describes the cache manager API
    """
    
    def setTimeout(timeout):
        """Set the timeout for this cache.
        """
    
    def getData(func, key, force_reload=False, args=[], kwargs={}):
        """Return cached data, or call func, cache it's return value and return
        it.
        """
    
    def get(key, force_reload=False):
        """Return item with key or None.
        
        If force_reload is True, try to delete object with key from cache and
        return None.
        """
    
    def set(key, item, set_creationtime=True):
        """Store an item with key to cache.
        """
    
    def rem(key):
        """Remove item with key from cache if exists.
        """

class ICacheProvider(Interface):
    """This interface describes an API for caching objects.
    """
    
    def reset():
        """Reset the cache object.
        
        Remove all objects from cache.
        """
    
    def size():
        """Return the current size of the cache in byte.
        """
        
    def keys():
        """Return the keys of the objects contained in this cache as list.
        """
                
    def values():
        """Return objects contained in this cache as list.
        """
    
    def get(key, default=None):
        """Return object by key or default value if not exist.
        """
    
    def __getitem__(key):
        """Return object by key or None if not exists.
        """
    
    def __setitem__(key, object):
        """Store object to cache by given key.
        """
    
    def __delitem__(key):
        """Delete object by key from cache.
        
        Always return None.
        """

class IFSCacheProvider(ICacheProvider):
    """Marker
    """

class IMemcacheProvider(ICacheProvider):
    """Marker
    """