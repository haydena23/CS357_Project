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

# This is the input file for testCase_InvertString. Given these specific states, it will rewrite the input of 1's and 0's to the
# inverted form, for example 101 will be rewritten as 010.

inputStructure({
    'q_START': { # This is the starter state
        '1':('0','->'), # Read as "If read 1, rewrite 0, move marker right"
        '0':('1','->'), # Read as "If read 0, rewrite 1, move marker right"
        '[]':'q_ACCEPT', # If read blank space, move to q_ACCEPT
    },
    'q_ACCEPT': { # This is the q_ACCEPT state
        '[]': True, # If the TM makes it to this state and reads the correct ending codition, 
    },              # then the TM will accept it, ending the program stating valid string
    'q_REJECT': { # This is the q_REJECT state
        '[]': False, # If the TM makes it to this state, then the TM will reject it, ending the program stating invalid string
    },
}).run('111000110010') # Here is our test string that we would like to run through this specific TM. The output should be 000111001101