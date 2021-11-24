# Using Python 3.9
#
# Authors:
#   Tony Hayden
#   Jennifer Brana
#
# Version: 1.0
# 11/23/21
#                                               IMPORTANT 
#############################################################################################################
#   This program requires the termcolor module. To import this module, go to the terminal of this file      #
#   and type "python -m pip install termcolor" without the "", and then restart. That should install the    #
#   module. This module is being used to underline the head pointer on the tape.                            #
#############################################################################################################
#
# Resources used:
#   Introducing Python: Modern Computing in Simple Packages, 2nd Edition (Bill Lubanovic)

from TuringMachine import *
from inputStructure import *

# This is the input file for testCase_InvertString. It demonstrates the throwing of an error given incorrect transitions in the
# state. If the state tries to move to another state that isn't in the program, or it doesn't have a proper exit out of the state,
# it will throw an error. This is because our TM is deterministic. It reads the input "Bad_Input", and in the start state q_START,
# it does not find a valid transition reading in the "B" from the input. The program then throws an error.

inputStructure({
    'q_START': { # This is the q_START state
        '0': ('1', 'q_INVALID_INPUT', '->'), # Reads "If input of 0, write 1, move to state q_INVALID_INPUT, move marker right"
        '1': ('0', 'q_INVALID_INPUT', '->'), # Reads "If input of 1, write 0, move to state q_INVALID_INPUT, move marker right"
    },
    'q_ACCEPT': { # This is the q_ACCEPT state
        '[]': True, # If the TM makes it to this state and reads the correct ending codition, 
    },              # then the TM will accept it, ending the program stating valid string
    'q_REJECT': { # This is the q_REJECT state
        '[]': False, # If the TM makes it to this state, then the TM will reject it, ending the program stating invalid string
    },
}).run('Bad_Input')