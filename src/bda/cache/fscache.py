# Copyright 2009, Blue Dynamics Alliance, Austria - http://bluedynamics.com
# GNU General Public Licence Version 2 or later
"""
Module fscache.

This module provides fuctionallity for caching objects on the filesystem.

Therefor it uses cPickle if available, otherwise pickle.

This module was originally designed for very simple caching tasks like caching
mail headers in a MUA or similar. It is NOT a cache manager.

If you find this module useful and you have some improvements or bugfixes,
please contact the author.

This module is tested on linux with python 2.4. If you are running in troubles
when using another operating system or python version, please contact the 
author.
"""

try:
    import cPickle as pickle
except:
    import pickle


import os
import time
import logging

from zope.interface import implements
from zope.component import adapts
from zope.component import provideAdapter

from interfaces import ICacheManager
from interfaces import ICacheProvider
from interfaces import CacheException

from interfaces import IFSCacheProvider

logger = logging.getLogger('bda.cache.cachemanager')

class FSCacheException(CacheException): pass

class FSCache(object):
    """Class FsCache.
    
    Simple object caching.
    
    This class is accessible like a dictionary. For example:
        
    cache = FsCache('var/cache/mycache')
    cache['foo.bar'] = obj
    obj = ['foo.bar']
    obj = cache.get('foo.bar', False)
    del cache['foo.bar']
    
    The key for objects must ALWAYS be a string, it results directly in a
    file path.
    
    By convention, if the key is seperated by a dot like in the example above,
    the files created on your filesystem are placed in a directory tree, so
    the file for the key given in this example is placed at 'foo/bar.'.
    
    Take care of your keys, things like 'foo..bar', 'foo.',  '.foo' or using 
    path seperators like '/' and '\\' will end up in strange results and cause
    inconsistent data.
    
    On the other hand, it is no problem to store an object with key 'foo',
    since every file gets a trailing '.', so key 'foo' ends up in a file with
    the name 'foo.' while 'foo.bar' is sored at 'foo/bar.'.
    """
    
    implements(IFSCacheProvider)
    
    def __init__(self, cachedir, protocol=2, createDirIfNotExist=False):
        """Create the cache object.
        
        * basedir - the directory you want to store the cached objects.
        * protocol - the protocol you want to use for pickling. defaults to 2.
        
        Raise an FSCacheException when given basedir is invalid. Does not check
        if there is read/write access on this directory. Keep this in mind.
        
        Read the documentation of the module pickle to know about the 
        limitations on object pickling.
        """
        if not os.path.isabs(cachedir):
            errmsg = 'Cannot initialize cache. \'%s\' is not an absolute path.'
            raise FSCacheException(errmsg % cachedir)
        if not os.path.exists(cachedir) and not createDirIfNotExist:
            errmsg = 'Cannot initialize cache. Directory \'%s\' not exists.'
            raise FSCacheException(errmsg % cachedir)
        if createDirIfNotExist:
            self._createDirIfNotExist(cachedir)
        if not os.path.isdir(cachedir):
            errmsg = 'Cannot initialize cache. \'%s\' is not a Directory.'
            raise FSCacheException(errmsg % cachedir)
        self.cachedir = cachedir
        self.protocol = protocol
    
    def reset(self):
        for key in self.keys():
            del self[key]
    
    def size(self):
        # XXX
        return 0
        
    def keys(self):
        return self._readkeys([])
                
    def values(self):
        values = []
        for key in self.keys():
            values.append(self[key])
        return values
    
    def get(self, key, default=None):
        return self._getitem(key, default)
    
    def __getitem__(self, key):
        return self._getitem(key)
    
    def __setitem__(self, key, object):
        """Read the class documentation how keys must look like.
        """
        objpath = key.split('.')
        objlen = len(objpath)
        pt = 1
        path = self.cachedir
        while pt < objlen:
            path = os.path.join(self.cachedir, *[f for f in objpath[:pt]])
            exists = os.path.exists(path)
            if not exists:
                os.mkdir(path)
            pt += 1
        path = os.path.join(path, '%s.' % objpath[-1])  
        file = open(path, 'wb')
        pickle.dump(object, file, self.protocol)
        file.close()
    
    def __delitem__(self, key):
        path = key.split('.')
        path[-1] = '%s.' % path[-1]
        try:
            os.remove(os.path.join(self.cachedir, *path))
        except OSError:
            return None
        pt = len(path) - 1
        while pt > 0:
            previous = path[:pt]
            if not previous:
                return None
            curpath = os.path.join(self.cachedir, *previous)
            contents = os.listdir(curpath)
            if not contents:
                os.rmdir(curpath)
            else:
                break
            pt -= 1
        return None
    
    def _getitem(self, key, default=None):
        path = '%s.' % os.path.join(self.cachedir, *key.split('.'))
        try:
            file = open(path, 'rb')
        except IOError:
            return default
        obj = pickle.load(file)
        file.close()
        return obj
    
    def _readkeys(self, keys, path=[]):
        entries = os.listdir(os.path.join(self.cachedir, *path))
        for entry in entries:
            if entry[-1] == '.':
                key = ''
                for part in path:
                    key = '%s%s.' % (key, part)
                keys.append('%s%s' % (key, entry[:len(entry) - 1]))
            else:
                self._readkeys(keys, path + [entry])
        return keys
    
    def _createDirIfNotExist(self, cachedir):
        if os.path.exists(cachedir):
            return
        path = cachedir.split(os.path.sep)
        for i in range(len(path)):
            if not os.path.exists(os.path.sep.join(path[:i + 1])) and path[i]:
                os.mkdir(os.path.sep.join(path[:i + 1]))

class FSCacheManager(object):
    
    implements(ICacheManager)
    adapts(IFSCacheProvider)
    
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
    
    def __delitem__(self, key):
        self.rem(key)
    
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

provideAdapter(FSCacheManager)