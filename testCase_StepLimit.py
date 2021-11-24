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

from inputStructure import *
from TuringMachine import *

# This is the test file for an infinite TM. This bounces between two states with no final accepting condition. This
# demonstrates the max counter of the code, stating that after 1,000 iterations, the program will force quit and throw
# an error stating the max counter has been reached. This forces the marker to move right and left infinitely

inputStructure({
    'q_START': {
        '1': ('q_1','->'), # If read a 1, move to state q_1 and move marker right
    },
    'q_1': {
        '0': ('q_START','<-'), # If read a 0, move to state q_START, and move marker left
    },
}).run('10')