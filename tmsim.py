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

import collections
import itertools

# TuringMachine class
class TuringMachine:

    # Default constructor to create initial state
    def __init__(
        self,
        initial_sequence=(),
        *,
        blank_symbol='[]',
        initial_state='q_s',
        initial_head_position=0,
    ):

        self.blank_symbol, self.state, self.head_position = blank_symbol, initial_state, initial_head_position # Sets self vars in accordance to initial vars
        self.tape = collections.defaultdict(lambda: self.blank_symbol, enumerate(initial_sequence)) # Creates tape by inserting blank space at the beginning, then the input string

    # Function to return the current symbol at head_position
    @property
    def symbol(self):
        return self.tape[self.head_position]

    # Function to set the new symbol to current head position
    @symbol.setter
    def symbol(self, new_symbol):
        self.tape[self.head_position] = new_symbol

    # Function to create the configuration in the form of leftHead::Head::rightHead
    @property
    def configuration(self):
        indices = self.tape.keys() # Split tape into array using keys in format [0,1,2..tapeMax]
        left, right = (min(indices), max(indices)) if indices else (0, 0) # Set the lowest and highest index of input string

        leftHead, rightHead = (
            tuple(self.tape[index] for index in range(*r)) for r in ((left, self.head_position), (self.head_position, max(right, self.head_position)+1))
        )

        return leftHead, self.state, rightHead

    # Function to remove blanks from string, and create tape by concatenating all symbols on self.tape 
    @property
    def contents(self):
        indices = self.tape.keys() # Parse the index values from the tape
        left, right = (min(indices), max(indices)) if indices else (0, 0) # Calculate bounds of the tape

        # Function to remove any blank symbols 
        def remove_nulls(iterable):
            return itertools.takewhile(
                lambda symbol: symbol != self.blank_symbol, # If symbol == blank symbol, break loop and return iterable without blank symbols
                itertools.dropwhile(lambda symbol: symbol == self.blank_symbol, iterable) # If symbol == blank symbol, drop it and return
            )
        
        # Concatenate the tape iterable that now doesn't include blank symbols
        return ''.join(remove_nulls(self.tape[index] for index in range(left, right+1)))

    def next(self, transition_function):
        try:
            new_symbol, new_state, head_movement_func = transition_function[self.state, self.symbol]
        except KeyError:
            raise RuntimeError(f'That transition is not defined for state {self.state}')

        self.symbol, self.state = new_symbol, new_state
        self.head_position = head_movement_func(self.head_position)