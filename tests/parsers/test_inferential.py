from argv.testing import expect
from argv.parsers.boolean import InferentialParser


def test_InferentialParser():
    parser = InferentialParser()

    expect(dict(verbose=True), 'arguments without subsequent non-flag argument should be parsed as boolean').\
        eq(parser.parse(['--verbose']))

    expect(dict(), 'no arguments should produce an empty dict').\
        eq(parser.parse([]))

    expect(dict(input='a.txt', fill=True, _=['b.txt']), 'flags should consume subsequent non-flag arguments').\
        eq(parser.parse(['--input', 'a.txt', 'b.txt', '--fill']))
