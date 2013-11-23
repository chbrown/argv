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

License
-------

Copyright (c) 2013 Christopher Brown. `MIT
Licensed <https://raw.github.com/chbrown/argv/master/LICENSE>`__.

.. |Travis CI Build Status| image:: https://travis-ci.org/chbrown/argv.png?branch=master
   :target: https://travis-ci.org/chbrown/argv
