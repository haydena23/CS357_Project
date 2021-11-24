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

# This is the test file for the TM that solves 0^N 1^N for N >= 0. It reads in a character, marks the character with a new one,
# and then moves on. After it has marked all of the characters, it checks validates itself, and then moves to the q_ACCEPT state.

inputStructure({
    'q_START': { 
        '[]': 'q_ACCEPT', # If blank, move to q_ACCEPT
        '0': ('Y', 'q_1', '->'), # If read 0, write Y, move to state q_1, and then move the marker right
        '1': 'q_REJECT', # If read 1, move to state q_REJECT
        'X': ('q_3', '->'), # If read X, move to state q_3, then move the marker right
    },
    'q_1': {
        '0': '->', # If read 0, move the marker right
        'X': '->', # If read X, move the marker right
        '1': ('X', 'q_2', '<-'), # If read 1, write X, move to state q_2, and then move the marker left
        '[]': 'q_REJECT', # If read blank space, move to q_REJECT
    },
    'q_2': {
        '0': '<-', # If read 0, move the marker right
        'Y': ('q_START', '->'), # If read Y, move to state q_START, and then move the marker right
        'X': '<-', # If read X, move the marker left
    },
    'q_3': { # This is state q_3, which iterates through the entire string if all chars are X. If so, move to the accept state
        'X': '->', # If read X, move the marker right
        '0': 'q_REJECT', # If read 0, move to state q_REJECT
        '1': 'q_REJECT', # If read 1, move to state q_REJECT
        '[]': 'q_ACCEPT', # If read blank space, move to q_ACCEPT
    },
    'q_ACCEPT': { # This is the q_ACCEPT state, and giving the satisfactory conditions for the TM, returns True saying it accepts
        '[]': True, # For this TM, it will only move to q_ACCEPT if the TM is correct and read in a space, therefore it reads the space again
    },
    'q_REJECT': { # This is the q_REJECT state
        '[]': False, # If the TM makes it to this state, then the TM will reject it, ending the program stating false
    },
}).run('00001111')
