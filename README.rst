Simpler command line argument parsing
-------------------------------------

In the spirit of
```optimist`` <https://github.com/substack/node-optimist>`__: less
magic, more flexibility.

::

    pi install argv

Quickstart
~~~~~~~~~~

Manual specification of arguments, no configuration:

::

    import argv
    argv.parse(['-i', 'input.txt', '-z', '--verbose'])
    >>> {'i': 'input.txt', 'verbose': True, 'z': True}

Uses ``sys.argv`` (without the executable name) if no argument list is
given:

::

    import sys
    sys.argv
    >>> ['/usr/local/bin/bottler', 'exec', 'prog.py', '--debug']
    argv.parse()
    >>> {'_': ['exec', 'prog.py'], 'debug': True}

Configuration:

::

    parser = argv.Parser()
    parser.add('action')
    parser.add('target')
    parser.add('-d', '--debug')
    parser.parse(['exec', 'prog.py', '--debug'])
    >>> {'action': 'exec', 'd': True, 'debug': True, 'target': 'prog.py'}

Testing
-------

Continuous integration:

|Travis CI Build Status|

Or run tests locally:

::

    python setup.py test

Development
-----------

Terminology:
~~~~~~~~~~~~

-  **flag**: a command line argument marked with a double dash or each
   component of a group denoted by a single dash. E.g.,

   -  ``--verbose --logfile logs/app.txt`` has two flags: ``verbose``
      and ``logfile``.
   -  ``-czf archive.tgz app/`` has three flags: ``c``, ``z``, and
      ``f``.

-  **token**: a white-space separated command line item. E.g.,

   -  \`--input= --logfile logs/app.txt

Related libraries
-----------------

-  https://github.com/docopt/docopt
-  http://docs.python.org/2/library/argparse.html
-  http://docs.python.org/2/library/optparse.html (Deprecated)

TODO: write about differences between this library (``argv``) and these
libraries, relative merits of each, opposing philosophies, etc.

License
-------

Copyright (c) 2013 Christopher Brown. `MIT
Licensed <https://raw.github.com/chbrown/argv/master/LICENSE>`__.

.. |Travis CI Build Status| image:: https://travis-ci.org/chbrown/argv.png?branch=master
   :target: https://travis-ci.org/chbrown/argv
