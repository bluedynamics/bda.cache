#
# Copyright 2008, Blue Dynamics Alliance, Austria - http://bluedynamics.com
#
# GNU General Public Licence Version 2 or later

__author__ = """Robert Niederreiter <rnix@squarewave.at>"""
__docformat__ = 'plaintext'

from setuptools import setup, find_packages
import sys, os

version = '1.1'
shortdesc = "Simple caching infrastructure."
longdesc = open(os.path.join(os.path.dirname(__file__), 'README.txt')).read()

setup(name='bda.cache',
      version=version,
      description=shortdesc,
      long_description=longdesc,
      classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Web Environment',
            'Framework :: Zope2',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content',            
      ], # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Robert Niederreiter',
      author_email='rnix@squarewave.at',
      url='https://svn.plone.org/svn/collective/bda.cache',
      license='General Public Licence',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['bda'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',  
          'python-memcached',
          'zope.app.component',
      ],
      extras_require={
          'test': [
              'interlude',
              'zope.app.testing',
          ]
      },
      entry_points="""
      """,
      )