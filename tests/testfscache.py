"""
Test for the fscache module.
"""

__author__ = """Robert Niederreiter <robertn@bluedynamics.com>"""
__docformat__ = 'plaintext'


import doctest
import unittest
from interactive import interact

suite = doctest.DocFileSuite(
        '../docs/testfscache.txt',
        optionflags=doctest.ELLIPSIS + doctest.REPORT_ONLY_FIRST_FAILURE, 
        globs={'interact': interact})

unittest.TextTestRunner().run(suite)