__author__ = """Robert Niederreiter <rnix@squarewave.at>"""
__docformat__ = 'plaintext'

import os
import unittest
import interlude
import zope.app.component
from pprint import pprint
from zope.testing import doctest
from zope.app.testing.placelesssetup import setUp, tearDown
from zope.configuration.xmlconfig import XMLConfig
import logging
logger = logging.getLogger('bda.cache')

optionflags = doctest.NORMALIZE_WHITESPACE | \
              doctest.ELLIPSIS | \
              doctest.REPORT_ONLY_FIRST_FAILURE

TESTFILES = [
    '../nullcache.txt',
    '../fscache.txt',
    '../cachemanager.txt',
]

if os.environ.get('MEMCACHEDBIN', None):
    TESTFILES += ['../memcached.txt',]
else:
    logger.debug('Can not test memcached module. No path to memcached binary '
                 'given in test environment (MEMCACHEDBIN).')

def test_suite():
    setUp()
    XMLConfig('meta.zcml', zope.app.component)()
    return unittest.TestSuite([
        doctest.DocFileSuite(
            file, 
            optionflags=optionflags,
            globs={'interact': interlude.interact,
                   'pprint': pprint},
        ) for file in TESTFILES
    ])
    tearDown()

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite') 