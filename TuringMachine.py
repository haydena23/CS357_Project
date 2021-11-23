# Using Python 3.9
#
# Authors:
#   Tony Hayden
#   Jennifer Brana
# Version: 1.0
# 11/22/21
#
# Notes:
#   This program requires the termcolor module. To import this module, go to the terminal of this file
#   and type "python -m pip install termcolor" without the "", and then restart. That should install the
#   module. This module is being used to underline the head pointer on the tape.
#
# Resources used:
#   Introducing Python: Modern Computing in Simple Packages, 2nd Edition (Bill Lubanovic)

import itertools
import collections

class TuringMachine:
    # Default constructor to create initial state
    def __init__(self,startTape=(),*,blankChar='[]',startState='q_START',marker=0,):
        # Sets self vars in accordance to initial vars
        self.blankChar = blankChar
        self.state = startState
        self.marker = marker
        # Creates tape by inserting blank space at the beginning, then the input string
        self.tape = collections.defaultdict(lambda: self.blankChar, enumerate(startTape)) 
    # Function to return the current char at head_position
    @property
    def char(self):
        return self.tape[self.marker]
    # Function to set the new char to current head position
    @char.setter
    def char(self, newChar):
        self.tape[self.marker] = newChar
    # Function to create the configuration in the form of leftHead::Head::rightHead
    @property
    def config(self):
        idx = self.tape.keys() # Split tape into array using keys in format [0,1,2..tapeMax]
        leftBound = min(idx)
        rightBound = max(idx)
        leftHead, rightHead = (
            tuple(self.tape[index] for index in range(*r)) for r in ((leftBound, self.marker), (self.marker, max(rightBound, self.marker)+1))
        )
        return leftHead, self.state, rightHead
    # Function to remove blanks from string, and create tape by concatenating all chars on self.tape 
    @property
    def contents(self):
        idx = self.tape.keys() # Parse the index values from the tape
        leftBound = min(idx) # Calculate bounds of the tape
        rightBound = max(idx)
        # Function to remove any blank chars 
        def remove_nulls(listToIterate):
            return itertools.takewhile(
                lambda char: char != self.blankChar, # If char == blank char, break loop and return iterable without blank chars
                itertools.dropwhile(lambda char: char == self.blankChar, listToIterate) # If char == blank char, drop it and return
            )
        # Concatenate the tape iterable that now doesn't include blank chars
        return "".join(remove_nulls(self.tape[idx] for idx in range(leftBound,rightBound+1)))
    def next(self, transition):
        try: # Try to move to next valid trasition
            NewChar, NewState, markerMove = transition[self.state,self.char]
        except KeyError: # If not valid, throw error
            raise RuntimeError(f'That transition is not defined')
        self.char = NewChar
        self.state = NewState
        self.marker = markerMove(self.marker)