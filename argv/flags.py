from argv.tokens import split_flag_token


def parse_tokens(tokens):
    '''Read tokens strings into (is_flag, value) tuples:

    For this value of `tokens`:

        ['-f', 'pets.txt', '-v', 'cut', '-cz', '--lost', '--delete=sam', '--', 'lester', 'jack']

    `flatten(tokens)` yields an iterable:

        [
            (True,  'f'),
            (False, 'pets.txt'),
            (True,  'v'),
            (False, 'cut'),
            (True,  'c'),
            (True,  'z'),
            (True,  'lost'),
            (True,  'delete'),
            (False, 'sam'),
            (False, 'lester'),
            (False, 'jack'),
        ]

    Todo:

        ensure that 'verbose' in '--verbose -- a b c' is treated as a boolean even if not marked as one.
    '''
    # one pass max
    tokens = iter(tokens)
    for token in tokens:
        if token == '--':
            # bleed out tokens without breaking, since tokens is an iterator
            for token in tokens:
                yield False, token
        elif token.startswith('-'):
            # this handles both --last=man.txt and -czf=file.tgz
            # str.partition produces a 3-tuple whether or not the separator is found
            token, sep, value = token.partition('=')
            for flag in split_flag_token(token):
                yield True, flag

            if sep:
                # we don't re-flatten the 'value' from '--token=value'
                yield False, value
        else:
            yield False, token
