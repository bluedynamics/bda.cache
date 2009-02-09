#
# Copyright 2009, Blue Dynamics Alliance, Austria - http://bluedynamics.com
#
# GNU General Public Licence Version 2 or later

__author__ = """Robert Niederreiter <rnix@squarewave.at>"""
__docformat__ = 'plaintext'

from interfaces import ICacheProvider
from interfaces import ICacheManager

from nullcache import NullCache
from nullcache import NullCacheManager

from fscache import FSCache
from fscache import FSCacheManager
from fscache import FSCacheException

from memcached import Memcached
from memcached import MemcachedManager
from memcached import MemcachedException

# XXX: remove me, some shit left in BlueWebMail
from cachemanager import CacheManager