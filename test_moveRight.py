from TuringMachine import *
from inputStructure import *

inputStructure({
    'q_s': {
        '0': ('1', '->'),
        '1': ('0', '->'),
        '[]': True,
    }
}).run('001011001')