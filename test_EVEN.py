from TuringMachine import *
from algo import *

inputStructure({
    'q_START': {
        '0': ('q_ODD', '->'),
        '1': ('q_ODD', '->'),
        '[]': 'q_ACCEPT',
    },
    'q_ODD': {
        '0': ('q_START', '->'),
        '1': ('q_START', '->'),
        '[]': 'q_REJECT',
    },
    'q_ACCEPT': {
        '[]': True,
    },
    'q_REJECT': {
        '[]': False,
    },
}).run('111111000000')
