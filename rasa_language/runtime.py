from parser import parse
import sys
from collections import ChainMap

def eval(x, env=None):
    """
    Avalia expressão.
    """

    if env is None:
        env = {} 
    print('___________>', x)

    head, *args = x
    print('aaaa', head, args)

    if head == 'blocks':
        env['blocks'] = args
    
    elif head == 'block':
        return {'block': args}
        
    return env

test = sys.stdin.read()
print(parse(test))
