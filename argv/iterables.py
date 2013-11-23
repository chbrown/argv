import itertools


class peekable(object):
    def __init__(self, iterable):
        self.pointer = iterable

    def __iter__(self):
        return self

    def next(self):
        return self.pointer.next()

    def peek(self, default=None):
        '''Returns `default` is there is no subsequent item'''
        try:
            result = self.pointer.next()
            # immediately push it back onto the front of the iterable
            self.pointer = itertools.chain([result], self.pointer)
            return result
        except StopIteration:
            # nothing to put back; iterating doesn't change anything past the end
            return default
