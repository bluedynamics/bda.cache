General Caching API
===================

This package is designed to be used by applications which require different
kinds of caching flavour. This is abstracted due to the interfaces
``ICacheProvider`` and  ``ICacheManager``. ICacheProvider takes care of the
concrete cache implementation, ICacheManager is the read/write interface.

The convention is to adapt a concrete ICacheProvider implementation.

  >>> from bda.cache import ICacheManager
  >>> from bda.cache import Memcached
  
  >>> provider = Memcached(['127.0.0.1:11211'])
  >>> manager = ICacheManager(provider)

We can ask the manager for data inside the cache

  >>> data = manager.get('somekey', force_reload=False)

If ``force_reload`` is set to True, try to delete data with key from cache and
return None.

We're also able to manipulate the cache's data (some restrictions my result out
of backend not providing them)

  >>> manager.set('somekey', object())

There exist a convenience to use some API's and cache it's results all at once.

  >>> data = manager.getData(func, key, force_reload=False, args=[], kwargs={})

First the data for ``key`` is looked up inside the cache provider. If not found
there or if ``force_reload`` is set to True, call given ``func`` . The return
value of this function will be stored in the cache provider. ``args`` and
``kwargs`` are passed as parameters to given function if it's call is required.

You might ask why all this is done due to 2 seperate interfaces...

Some usecase might require different cache providers i.e. for different payload
size. This way you can implement any other cache provider usage as well due to
the cache manager interface.


Dependencies
------------

  * zope.interface
  * zope.component
  * bda.cache.fscache.FSCache recommends that availability of ``cpickle``
  * bda.cache.memcached.Memcached requires ``python-memcached``


Notes
-----

If you're interessted to contribute; Feel free but keep in mind that this code
is planned to be released under a BSD like licence in future.


Changes
-------

  * 1.1.2 (rnix, 2009-02-10)
      * remove legacy code

  * 1.1.1 (rnix, 2009-02-10)
      * bugfix in zcml configuration.

  * 1.1 (rnix, 2009-02-09):
      * Cache Managers are now adapters.
      * Implement memcached server support
      * deprecate the default CacheManager
      * Fix tests for FSCache
  
  * <= 1.0 (rnix):
      * Initial work
