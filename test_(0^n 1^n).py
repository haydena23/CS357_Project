from TuringMachine import *
from algo import *

Algorithm({
    'q_START': {
        '[]': True,
        '0': ('X', 'q_1', '->'),
        '1': False,
        'Y': ('q_c', '->'),
    },
    'q_1': {
        '0': '->',
        'Y': '->',
        '1': ('Y', 'q_b', '<-'),
        '[]': False,
    },
    'q_b': {
        '0': '<-',
        'X': ('q_START', '->'),
        'Y': '<-',
    },
    'q_c': {
        'Y': '->',
        '0': False,
        '1': False,
        '[]': True,
    }
}).run('00001111')
