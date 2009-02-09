# -*- coding: utf-8 -*-
#
# Copyright (c) 2006-2007 by:
#     Blue Dynamics Alliance Klein & Partner KEG, Austria
#     Squarewave Computing Robert Niederreiter, Austria
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

__author__ = """Robert Niederreiter <rnix@squarewave.at>"""
__docformat__ = 'plaintext'

from zope.interface import Interface

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
        """Return cached data or call func, cache return value and return data.
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
        """Store object to file system by given key.
        """
    
    def __delitem__(key):
        """Delete object by key from cache.
        
        Always return None.
        """
