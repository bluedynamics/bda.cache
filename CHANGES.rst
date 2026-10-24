Changes
-------

2.0.0 (unreleased)
~~~~~~~~~~~~~~~~~~

- Fix the client library selection in ``bda.cache.memcached`` if both
  ``libmc`` and ``pylibmc`` are installed. ``pylibmc.Client`` was initialized
  with the ``libmc`` arguments. ``libmc`` is preferred now, as intended.
  [rnix]

- Drop the Python 2 remnants: the ``six`` imports in ``bda.cache.fscache``
  and ``bda.cache.memcached`` (``six`` never was a declared dependency),
  ``class X(object)`` and the ``IOError`` alias. Remove the unreachable code
  in ``FSCache.__delitem__`` and the unused ``ICacheProvider`` import in
  ``bda.cache.memcached``. Behaviour unchanged.
  [rnix]

- Convert the doctests to unittest tests and use pytest as test runner. The
  memcached tests use a fake client and no longer need a running memcached
  server. Drop the ``interlude`` and ``zope.testing`` test dependencies.
  [rnix]

- Sort the imports with ruff (one per line, ``from`` imports first, no
  sections) and format the code with ``ruff format`` (90 characters per line,
  single quotes).
  [rnix]

- Add ``Makefile`` (mxmake) with ``qa.ruff``, ``qa.test`` and ``qa.coverage``
  domains, pin the ruff configuration in ``pyproject.toml`` and add a GitHub
  Actions test workflow.
  [rnix]

- Refactor package layout to use ``pyproject.toml`` and implicit namespace
  packages.
  [rnix]

- Drop Python 2 support. Python >= 3.10 is required.
  [rnix]


1.3.0 (2019-02-05)
~~~~~~~~~~~~~~~~~~

- Python 3 comaptibility [reinhardt]

- Code style (black/isort) [jensens]

1.2.0 (2017-10-19)
~~~~~~~~~~~~~~~~~~

- Change to use libmc or pylibmc when available

- Add option to require with bda.cache[pylibmc] or bda.cache[libmc]


1.1.2 (2009-02-10)
~~~~~~~~~~~~~~~~~~

- remove legacy code


1.1.1 (2009-02-10)
~~~~~~~~~~~~~~~~~~

- bugfix in zcml configuration.


1.1 (2009-02-09)
~~~~~~~~~~~~~~~~

- Cache Managers are now adapters.

- Implement memcached server support

- deprecate the default CacheManager

- Fix tests for FSCache


1.0
~~~

- Initial work

