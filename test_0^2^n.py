# { 0^(2^n) | n >= 0 }

from tmsim import *
import math

Algorithm({
    'q_s': {
        '[]': False,
        '0': ('@', 'q_check_single', '->'),
    },
    'q_check_single': {
        '[]': True,
        '0': 'q_odd',
    },
    'q_even': {
        '[]': ('q_verify', '<-'),
        '0': ('q_odd', '->'),
        '#': '->',
    },
    'q_odd': {
        '[]': False,
        '0': ('#', 'q_even', '->'),
        '#': '->',
    },
    'q_verify': {
        '0': 'q_back',
        '#': '<-',
        '@': True,
    },
    'q_back': {
        '0': '<-',
        '#': '<-',
        '@': ('q_odd', '->'),
    },
}).run('000')
