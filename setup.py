#
# Copyright 2008, Blue Dynamics Alliance, Austria - http://bluedynamics.com
#
# GNU General Public Licence Version 2 or later

__author__ = """Robert Niederreiter <rnix@squarewave.at>"""
__docformat__ = "plaintext"

from setuptools import find_packages
from setuptools import setup

import os


version = "1.3.0.dev0"
shortdesc = "Simple caching infrastructure."
longdesc = open(os.path.join(os.path.dirname(__file__), "README.rst")).read()

setup(
    name="bda.cache",
    version=version,
    description=shortdesc,
    long_description=longdesc,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Zope2",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    keywords="caching memcached fscache zope zca",
    author="Robert Niederreiter",
    author_email="rnix@squarewave.at",
    url="https://svn.plone.org/svn/collective/bda.cache",
    license="GPL: GNU General Public Licence",
    packages=find_packages("src"),
    package_dir={"": "src"},
    namespace_packages=["bda"],
    include_package_data=True,
    zip_safe=False,
    install_requires=["setuptools", "python-memcached", "zope.component"],
    extras_require={
        "libmc": ["libmc"],
        "pylibmc": ["pylibmc"],
        "test": ["interlude", "zope.testing"],
    },
    entry_points="""
      """,
)
