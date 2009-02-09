#
# Copyright 2009, Blue Dynamics Alliance, Austria - http://bluedynamics.com
#
# GNU General Public Licence Version 2 or later

__author__ = """Robert Niederreiter <rnix@squarewave.at>"""
__docformat__ = 'plaintext'

from interfaces import ICacheProvider
from interfaces import ICacheManager

from fscache import FSCache
from fscache import FSCacheException

from cachemanager import CacheManager