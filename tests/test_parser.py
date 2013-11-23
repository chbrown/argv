import argv
from argv.parser import flatten_flags, flatten_argv


class expect(object):
    def __init__(self, expected, description=None):
        self.expected = expected
        prologue = (description + '\n  ') if description else ''
        self.message = prologue + 'we expected %r but got %%r' % expected

    def eq(self, produced):
        assert produced == self.expected, self.message % produced
        return self


def test_argv_Parser():
    # boolean without default
    parser = argv.Parser()
    parser.add('--verbose', boolean=True)

    expect(dict(verbose=True), 'arguments defined as boolean should show up as boolean').\
        eq(parser.parse(['--verbose']))

    expect(dict(verbose=None), 'missing boolean arguments should not get values unless a default is specified').\
        eq(parser.parse([]))

    # boolean with default
    parser = argv.Parser()
    parser.add('--verbose', boolean=True, default=False)

    expect(dict(verbose=False), 'default value should fill in when a boolean arguments is missing').\
        eq(parser.parse([]))

    # aliases
    parser = argv.Parser()
    parser.add('-v', '--verbose', boolean=True)

    expect(dict(v=True, verbose=True), 'aliased values should be propagated to all names, even if the short option is used').\
        eq(parser.parse(['-v'])).\
        eq(parser.parse(['--verbose']))

    # positional
    parser = argv.Parser()
    parser.add('first')
    parser.add('--flatten', boolean=True)
    parser.add('last')

    expect(dict(first='a.txt', last='z.txt', flatten=True),
        'aliased values should be propagated to all names, even if the short option is used').\
        eq(parser.parse(['--flatten', 'a.txt', 'z.txt']))
        # eq(parser.parse(['a.txt', '--flatten', 'z.txt'])).\
        # eq(parser.parse(['a.txt', 'z.txt', '--flatten']))


def test_argv_helpers():
    # flatten_flags
    expect(['m'], 'short-flag should produce just a single letter').\
        eq(list(flatten_flags('-m')))

    expect(['c', 'z', 'f'], 'combined short-flags should produce multiple letters').\
        eq(list(flatten_flags('-czf')))

    expect(['last'], 'double-dash prefix should produce a single list of the whole thing').\
        eq(list(flatten_flags('--last')))

    # flatten_argv
    sys_argv = ['-f', 'pets.txt', '-v', 'cut', '-cz', '--lost', '--delete=sam', '--', 'lester', 'jack']
    flattened = [
        (True, 'f'),
        (False, 'pets.txt'),
        (True, 'v'),
        (False, 'cut'),
        (True, 'c'),
        (True, 'z'),
        (True, 'lost'),
        (True, 'delete'),
        (False, 'sam'),
        (False, 'lester'),
        (False, 'jack'),
    ]
    expect(flattened, 'flatten_argv should produce expected output').\
        eq(list(flatten_argv(sys_argv)))
