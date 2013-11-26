from argv.testing import expect


def test_split_flag_token():
    from argv.tokens import split_flag_token

    expect(['m'], 'short-flag should produce just a single letter').\
        eq(list(split_flag_token('-m')))

    expect(['c', 'z', 'f'], 'combined short-flags should produce multiple letters').\
        eq(list(split_flag_token('-czf')))

    expect(['last'], 'double-dash prefix should produce a single list with one element').\
        eq(list(split_flag_token('--last')))
