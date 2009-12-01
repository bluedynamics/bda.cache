# Copyright 2009, Blue Dynamics Alliance, Austria - http://bluedynamics.com
# GNU General Public Licence Version 2 or later

from zope.interface import Interface

class CacheException(Exception): pass

class ICacheVary(Interface):
    """This interface describes an API for manipulating objects inside a cache.
    """
    
    def vary(*args, **kwargs):
        """Manipulate objects inside the cache.
        """

class ICacheManager(Interface):
    """Interface for read/write operations on ICacheProvider implementing
    objects.
    """
    
    def setTimeout(timeout):
        """Set cache timeout in seconds.
        """
    
    def getData(func, key, force_reload=False, args=[], kwargs={}):
        """Convenience to read and cache results at once.
        
        * Tries to read result from cache.
        * If no result, call given functions with *args ang **kwargs
        * If function called, store returned value to cache
        * Return result
        """
    
    def get(key, force_reload=False):
        """Return item with key or None.
        
        If force_reload is True, try to delete object with key from cache and
        return None.
        """
    
    def set(key, item, set_creationtime=True):
        """Store an item with key to cache.
        
        XXX: get rid of ``set_creationtime``
        """
    
    def rem(key):
        """Remove item with key from cache if exists.
        
        Legacy. Replaced by ``__delitem__``
        """
    
    def __delitem__(key):
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

class INullCacheProvider(ICacheProvider):
    """Marker
    """

class IFSCacheProvider(ICacheProvider):
    """Marker
    """

class IMemcachedProvider(ICacheProvider):
    """Marker
    """