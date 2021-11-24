# Using Python 3.9
#
# Authors:
#   Tony Hayden
#   Jennifer Brana
#
# Version: 1.0
# 11/22/21
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
    'q_START': { # This is the state q_START
        '0': ('q_ODD', '->'), # This line says "If read input 0, move to state q_ODD, and move the marker right"
        '1': ('q_ODD', '->'), # This line says "If read input 1, move to state q_ODD, and move the marker right"
        '[]': 'q_ACCEPT', # If read in a blank space, then string is of even length, and move to q_ACCEPT
    },
    'q_ODD': { # This is the state q_ODD
        '0': ('q_START', '->'), # This line says "If read input 0, move to state q_START, and move the marker right"
        '1': ('q_START', '->'), # This line says "If read input 1, move to state q_START, and move the marker right"
        '[]': 'q_REJECT', # If read in a blank space, then string is of odd length, and move to q_REJECT
    },
    'q_ACCEPT': { # This is the q_ACCEPT state, and giving the satisfactory conditions for the TM, returns True saying it accepts
        '[]': True, # For this TM, it will only move to q_ACCEPT if the TM is correct and read in a space, therefore it reads the space again
    },
    'q_REJECT': { # This is the q_REJECT state
        '[]': False, # If the TM makes it to this state, then the TM will reject it, ending the program stating false
    },
}).run('111111000000') # Here is our test string that we would like to run through this specific TM.