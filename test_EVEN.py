from tmsim import *

Algorithm({
    'q_even': {
        '0': ('q_odd', '->'),
        '1': ('q_odd', '->'),
        '[]': True,
    },
    'q_odd': {
        '0': ('q_even', '->'),
        '1': ('q_even', '->'),
        '[]': False,
    }
}, initial_state='q_even').run('111111000000')
