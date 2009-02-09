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
from interfaces import CacheException
from interfaces import IMemcacheProvider

class MemcacheException(CacheException): pass

class Memcache(object):
    
    implements(IMemcacheProvider)
    
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