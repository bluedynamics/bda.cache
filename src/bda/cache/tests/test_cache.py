__author__ = """Robert Niederreiter <rnix@squarewave.at>"""
__docformat__ = 'plaintext'

import os
import unittest
import pprint 
import interlude
import zope.component
from zope.testing import doctest
import logging
logger = logging.getLogger('bda.cache')

optionflags = doctest.NORMALIZE_WHITESPACE | \
              doctest.ELLIPSIS | \
              doctest.REPORT_ONLY_FIRST_FAILURE

TESTFILES = [
    '../nullcache.txt',
    '../fscache.txt',
    '../memcached.txt',
]

if os.environ.get('MEMCACHEDBIN', None):
    TESTFILES += ['../memcached.txt',]
else:
    logger.info('Can not test memcached module. No path to memcached binary '
                'given in test environment (MEMCACHEDBIN).')

def test_suite():
    return unittest.TestSuite([
        doctest.DocFileSuite(
            file, 
            optionflags=optionflags,
            globs={'interact': interlude.interact,
                   'pprint': pprint},
        ) for file in TESTFILES
    ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite') 