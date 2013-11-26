

def parse(argv=None):
    '''Singleton helper: run parse on a completely unconfigured parser'''
    from argv.parsers.inferential import InferentialParser

    return InferentialParser().parse(argv)
