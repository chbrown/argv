from argv.testing import expect
from argv.parsers.boolean import BooleanParser


def test_BooleanParser_without_default():
    parser = BooleanParser()
    parser.add('--verbose', boolean=True)

    expect(dict(verbose=True), 'arguments defined as boolean should show up as boolean').\
        eq(parser.parse(['--verbose']))

    expect(dict(verbose=None), 'missing boolean arguments should not get values unless a default is specified').\
        eq(parser.parse([]))


def test_BooleanParser_with_default():
    parser = BooleanParser()
    parser.add('--verbose', boolean=True, default=False)

    expect(dict(verbose=False), 'default value should fill in when a boolean arguments is missing').\
        eq(parser.parse([]))


def test_BooleanParser_with_aliases():
    parser = BooleanParser()
    parser.add('-v', '--verbose', boolean=True)

    expect(dict(v=True, verbose=True),
        'aliased values should be propagated to all names, even if the short option is used').\
        eq(parser.parse(['-v'])).\
        eq(parser.parse(['--verbose']))


def test_BooleanParser_with_positional_arguments():
    parser = BooleanParser()
    parser.add('first')
    parser.add('--flatten', boolean=True)
    parser.add('last')

    expect(dict(first='a.txt', last='z.txt', flatten=True),
        'a flag marked as boolean should not consume adjacent tokens').\
        eq(parser.parse(['--flatten', 'a.txt', 'z.txt']))
        # eq(parser.parse(['a.txt', '--flatten', 'z.txt'])).\
        # eq(parser.parse(['a.txt', 'z.txt', '--flatten']))
