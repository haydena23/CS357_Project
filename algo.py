from TuringMachine import *
from termcolor import colored

## Algorithm class defining the input file
class Algorithm:
    # Create initial object for TM data
    def __init__(
        self,
        function,
        *,
        blank='[]',
        startState='q_s',
        states=(True, False),
        chars=(),
        arrows={'<-': lambda marker: marker-1,'->': lambda marker: marker+1,},
        rename={'[]': '⬚'},
        ):
        # Set init vars
        self.blank, self.startState = blank, startState
        self.rename = rename
        states = set(function.keys()).union(states) # Create set of all states in TM
        chars = set(char for values in function.values() for char in values.keys()).union(chars) # Creates set of tape alphabet
        # Check all combinations of states, chars and arrows
        for (label1, set1), (label2, set2) in itertools.combinations({'states': states, 'symbols': chars, 'arrows': arrows}.items(), 2):
            if not set1.isdisjoint(set2):
                raise ValueError(f'Sets of {label1} and {label2} arent disjoint')
        self.states_max_length = max(len(str(state)) for state in states) # Calculates the largest string of all state names as int
        # Function to parse information for each transition
        def parse(old_state, old_char, value):
            if not isinstance(value, tuple):
                value = (value,) # If value isn't a tuple var, set it to a tuple
            new_char, new_state, new_arrow = None, None, None
            for decider in value: # Depending on what temp var decider is, store it in respective var
                if decider in arrows:
                    new_arrow = decider
                elif decider in states:
                    new_state = decider
                elif decider in chars:
                    new_char = decider
                else:
                    raise ValueError(f'Not a valid transition in the state') # If not a valid transition, error
            # Set new values from parsed data, then return values
            char = new_char if new_char is not None else old_char
            state = new_state if new_state is not None else old_state
            markerMove = arrows[new_arrow] if new_arrow else lambda marker: marker
            return char, state, markerMove
        # Function to parse a single transition
        self.transition = {
            (state, char): parse(state, char, val) for state, Char_Val in function.items() for char, val in Char_Val.items()
        }
    def create_section(self, section):
        return ''.join((str(self.rename.get(char, char)) for char in section))
    # Function to define how to format the output of the program
    def create_config(self, config): # Takes in self and configuration as a tuple
        leftHead, state, (char, *rightHead) = config # Sets vars based off of configuration tuple
        return ''.join((
            f'({state})'.ljust(self.states_max_length+5), # Display current state, then buffer of max state string length+OFFSET
            self.create_section(leftHead), # Display left side of current head
            colored(self.create_section((char,)), attrs=['underline']), # Underline current head position
            self.create_section(rightHead) # Display right side of current head
        ))
    ## Definition of run to execute the program
    def run(self,starter,*,fstates={True: True,False: False,}, max_steps=1_000,):
        # Below is the main driver of the code
        tm = TuringMachine(starter, blank=self.blank, startState=self.startState)
        print("\nTuring machine configurations")
        print("=============================\n")
        print(self.create_config(tm.config)) # Print the initial configuration
        for nextCounter in itertools.count(): # Step through the turing machine until max_steps is reached
            tm.next(self.transition) # Call next transition function
            print(self.create_config(tm.config)) # Print the configuration
            # Check to see if we are in the final state, return the final state and tape contents and end program
            if tm.state in fstates:
                return fstates[tm.state], tm.contents # If so, return the final state and the current tape
            # Set step count to ensure that we don't get into an infinite loop or a TM that takes way too long
            if nextCounter > max_steps:
                raise RuntimeError(f'Error: Step limit reached')