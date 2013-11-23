from argv.iterables import peekable


def flatten_flags(flags):
    '''Turn argv-type flags strings into names of arguments.

    Guarantees:

    * flags will not contain an '='
    * flags will not be '--'

    Since all output will be single flags, we yield strings, rather than tuples.

    | call | output |
    |:-----|:-------|
    | `flatten_flags('-m')` | `['m']` |
    | `flatten_flags('-czf')` | `['c', 'z', 'f']` |
    | `flatten_flags('--last')` | `['last']` |

    N.b., those lists are actually iterables.
    '''
    if flags.startswith('--'):
        # easy, just remove the '--'
        yield flags[2:]
    else:
        # short flags: yield each thing after the first '-' (handles multiple)
        for letter in flags[1:]:
            yield letter


def flatten_argv(argv):
    '''Turn strings into (is_flag, value) tuples:

    For an argv like this:

        ['-f', 'pets.txt', '-v', 'cut', '-cz', '--lost', '--delete=sam', '--', 'lester', 'jack']

    `flatten_argv` produces a list like:

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
    argv = iter(argv)
    for arg in argv:
        if arg == '--':
            # bleed out argv without breaking, since argv is an iterator
            for arg in argv:
                yield False, arg
        elif arg.startswith('-'):
            # this handles both --last=man.txt and -czf=file.tgz
            # str.partition produces a 3-tuple whether or now the separator is found
            arg, sep, value = arg.partition('=')
            for arg in flatten_flags(arg):
                yield True, arg
            if sep:
                # we don't re-flatten the 'value' from '--arg=value'
                yield False, value
        else:
            yield False, arg


class Argument(object):
    # not much more than a named tuple
    def __init__(self, names, default, boolean, positional):
        # names is a list of strings, which can be anything that doesn't start with a '-'
        self.names = names
        # default can be any value, but defaults to None
        self.default = default
        # boolean is itself a boolean, defaulting to False
        self.boolean = boolean
        # positional is a string if any of the given names were specified without a -x or --flag marker, otherwise None
        self.positional = positional

    def __repr__(self):
        return 'Argument(%(names)r, default=%(default)r, boolean=%(boolean)r, positional=%(positional)r)' % self.__dict__


class Parser(object):
    def __init__(self, arguments=None):
        self.arguments = arguments or []

    def __repr__(self):
        return 'Parser(\n  %s)' % ',\n  '.join(repr(argument) for argument in self.arguments)

    def add(self, *matches, **kw):  # kw=default=None, boolean=False
        '''Add an argument; this is optional, and mostly useful for setting up aliases or setting boolean=True

        Apparently `def add(self, *matches, default=None, boolean=False):` is invalid syntax in Python. Not only is this absolutely ridiculous, but the alternative `def add(self, default=None, boolean=False, *matches):` does not do what you would expect. This syntax works as intended in Python 3.

        If you provide multiple `matches` that are not dash-prefixed, only the first will be used as a positional argument.

        Specifying any positional arguments and then using `boolean=True` is just weird, and their will be no special consideration for boolean=True in that case for the position-enabled argument.
        '''
        # python syntax hack
        default = kw.get('default', None)
        boolean = kw.get('boolean', False)
        del kw
        # do not use kw after this line! It's a hack; it should never have been there in the first place.
        positional = None
        names = []
        for match in matches:
            if match.startswith('--'):
                names.append(match[2:])
            elif match.startswith('-'):
                names.append(match[1:])
            elif positional:
                # positional has already been filled
                names.append(match)
            else:
                # first positional: becomes canonical positional
                positional = match
                names.append(match)

        argument = Argument(names, default, boolean, positional)
        self.arguments.append(argument)

        # chainable
        return self

    def find_argument(self, name):
        for argument in self.arguments:
            if name in argument.names:
                return argument
        # default argument:
        return Argument([], None, False, False)

    def parse(self, args=None):
        '''Parse a list of arguments, returning a dict

        Useful terms:

        * "argument"
        * "value"
        * "boolean"

        Possibilities:

            --verbose            # boolean
            -v                   # boolean
            -f output.txt        # keyval
            -czf me.sig          # combined short flags
            --file output.txt    # keyval
            --file=output.txt    # keyval
            naked.txt            # positional argument
            be.txt nice.txt      # positional arguments
            be.txt nice.txt -v   # positional arguments before boolean flag

        Not possible:

            --files a.txt b.txt  # multiple flagged arguments

        Some things that might be surprising:

        * With an unconfigured parser:

            | input | output (json) |
            |:------|:-------|
            | `-v -c config.json` | `{"v": true, "c": "config.json"}` |
            | `-v input.txt -c config.json` | `{"v": "input.txt", "c": "config.json"}` |

        * But with a sole `parser.add('-v', boolean=True)`:

            | `-v input.txt -c config.json` | `{"v": true, "l": "config.json", "_": ["input.txt"]}` |

            * Or if you have also declared a positional argument with `parser.add('file')`:

                    | `-v input.txt -l config.json` | `{"f": true, "l": "config.json", "file": "input.txt"}` |

        Which is to say, `boolean=True` only says "don't consume the next arg".
        But `boolean=False` arguments can still end up with boolean values if there is no suitable subsequent.
        '''
        opts = dict()
        positions = [argument.positional for argument in self.arguments if argument.positional]

        if args is None:
            import sys
            # skip over the program name with the [1:] slice
            args = sys.argv[1:]

        # arglist is a tuple of (flag?, name) pairs
        arglist = peekable(flatten_argv(args))
        for flag, name in arglist:
            if flag is True:
                argument = self.find_argument(name)

                # .peek will return the default argument iff there are no more entries
                next_flag, next_name = arglist.peek(default=(None, None))
                # next_flag will be None if there are no more items, but True/False if there is a next item

                # if this argument looks for a subsequent (is set as boolean), and the subsequent is not a flag, consume it
                if argument.boolean is False and next_flag is False:
                    opts[name] = next_name
                    # finally, advance our iterator, but since we already have the next values, just discard it
                    arglist.next()
                else:
                    # if there is no next, or the next thing is a flag all the boolean=False's in the world can't save you then
                    opts[name] = True
            else:
                # add positional argument
                if len(positions) > 0:
                    # we pop the positions off from the left
                    position = positions.pop(0)
                    opts[position] = name
                else:
                    # the rest of the args now end up as a list in '_'
                    opts.setdefault('_', []).append(name)

        # propagate aliases and defaults:
        for argument in self.arguments:
            # merge provided value from aliases
            for name in argument.names:
                if name in opts:
                    value = opts[name]
                    # we simply break on the first match.
                    break
            else:
                # if we iterate through all names and fine none in opts, use the default
                value = argument.default

            for name in argument.names:
                opts[name] = value

        return opts
