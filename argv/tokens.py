'''
Token: any single argument from a command line call

A lot of class / file for not many lines of code.
'''


def split_flag_token(token):
    '''
    Split a single token from the command line into its individual flags.

    Guarantees:

    * flags will not contain an '='
    * flags will not be '--'

    Since all output will be single flags, we yield strings, rather than tuples.

    | call | output |
    |:-----|:-------|
    | `split_token('-m')` | `['m']` |
    | `split_token('-czf')` | `['c', 'z', 'f']` |
    | `split_token('--last')` | `['last']` |

    N.b., those lists are actually iterables.
    '''
    if token.startswith('--'):
        # easy, just remove the '--'
        yield token[2:]
    else:
        # short flags: yield each thing after the first '-' (handles multiple)
        for letter in token[1:]:
            yield letter
