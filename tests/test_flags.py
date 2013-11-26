from argv.testing import expect


def test_parse_tokens():
    from argv.flags import parse_tokens

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
        eq(list(parse_tokens(sys_argv)))
