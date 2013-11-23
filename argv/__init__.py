from parser import Parser


def parse(argv=None):
    '''Singleton helper: run parse on a completely unconfigured parser'''
    return Parser().parse(argv)
