class expect(object):
    def __init__(self, expected, description=None):
        self.expected = expected
        prologue = (description + '\n  ') if description else ''
        self.message = prologue + 'we expected %r but got %%r' % expected

    def eq(self, produced):
        assert produced == self.expected, self.message % produced
        return self
