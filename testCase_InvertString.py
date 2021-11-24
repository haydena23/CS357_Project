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

# This is the input file for testCase_EVEN. Given these specific states, it tests whether or not the input string is of even length.
# If the string is of even length, it returns true. If it is not, then it returns false. This is done by evaluating the tape, and in one
# pass through, bouncing back and forth between two states for even or odd length, much similar to a DFA.

inputStructure({
    'q_START': {
        '1':('0','->'),
        '0':('1','->'),
        '[]':'q_ACCEPT',
    },
    'q_ACCEPT': { # This is the q_ACCEPT state
        '[]': True, # If the TM makes it to this state, then the TM will accept it, ending the program stating valid string
    },
    'q_REJECT': { # This is the q_REJECT state
        '[]': False, # If the TM makes it to this state, then the TM will reject it, ending the program stating invalid string
    },
}).run('111000110010') # Here is our test string that we would like to run through this specific TM. The output should be 000111001101