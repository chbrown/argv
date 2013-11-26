from argv.iterables import peekable
from argv.flags import parse_tokens


class InferentialParser(object):
    def __repr__(self):
        return '%s()' % self.__class__.__name__

    def parse(self, args=None):
        '''Parse a list of arguments, returning a dict.

        Flags are only boolean if they are not followed by a non-flag argument.

        All positional arguments not associable with a flag will be added to the return dictionary's `['_']` field.
        '''
        opts = dict()

        if args is None:
            import sys
            # skip over the program name with the [1:] slice
            args = sys.argv[1:]

        # arglist is a tuple of (is_flag, name) pairs
        arglist = peekable(parse_tokens(args))
        for is_flag, name in arglist:
            if is_flag is True:
                # .peek will return the default argument iff there are no more entries
                next_is_flag, next_name = arglist.peek(default=(None, None))
                # next_is_flag will be None if there are no more items, but True/False if there is a next item

                # if this argument looks for a subsequent (is set as boolean),
                #   and the subsequent is not a flag, consume it
                if next_is_flag is False:
                    opts[name] = next_name
                    # finally, advance our iterator, but since we already have the next values, just discard it
                    arglist.next()
                else:
                    # if there is no next thing, or the next thing is a flag,
                    #   all the boolean=False's in the world can't save you then
                    opts[name] = True
            else:
                # add positional argument
                opts.setdefault('_', []).append(name)

        return opts
