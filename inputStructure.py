from TuringMachine import *
from termcolor import colored

## Algorithm class defining the input file
class inputStructure:
    # Create initial object for TM data
    def __init__(self,function,*,blankChar='[]',startState='q_START',states=(True, False),chars=(),arrows={'<-': lambda marker: marker-1,'->': lambda marker: marker+1,},rename={'[]': '$'},):
        # Set init vars
        self.blankChar = blankChar
        self.startState = startState
        self.rename = rename
        states = set(function.keys()).union(states) # Create set of all states in TM
        chars = set(char for values in function.values() for char in values.keys()).union(chars) # Creates set of tape alphabet
        self.statesMaxLength = max(len(str(state)) for state in states) # Calculates the largest string of all state names as int

        # Function to parse information for each transition
        def stripData(oldState, oldChar, value):
            newChar, newState, newArrow = None, None, None
            for decider in value: # Depending on what temp var decider is, store it in respective var
                if decider in arrows:
                    newArrow = decider
                elif decider in states:
                    newState = decider
                elif decider in chars:
                    newChar = decider
                else:
                    raise ValueError("Not a valid transition in the state") # If not a valid transition, error
            # Set new values from parsed data, then return values
            char = newChar if newChar is not None else oldChar
            state = newState if newState is not None else oldState
            markerMove = arrows[newArrow] if newArrow else lambda marker: marker
            return char, state, markerMove
        # Function to parse a single transition
        self.transition = {
            (state, char): stripData(state, char, val) for state, Char_Val in function.items() for char, val in Char_Val.items()
        }
    def tapeSection(self, section):
        return ''.join((str(self.rename.get(char, char)) for char in section))
    # Function to define how to format the output of the program
    def createConfig(self, config): # Takes in self and configuration as a tuple
        leftHead, state, (char, *rightHead) = config # Sets vars based off of configuration tuple
        return "".join((
            f'({state})'.ljust(self.statesMaxLength+5), # Display current state, then buffer of max state string length+OFFSET
            self.tapeSection(leftHead), # Display left side of current head
            colored(self.tapeSection((char,)), attrs=['underline']), # Underline current head position
            self.tapeSection(rightHead) # Display right side of current head
        ))
    # Main driver of the program
    def run(self,starter,*,fstates={'q_ACCEPT': True,'q_REJECT': False,}, max_steps=1_000,):
        tm = TuringMachine(starter, blankChar=self.blankChar, startState=self.startState)
        print("\nTuring machine configurations")
        print("=============================\n")
        print(self.createConfig(tm.config)) # Print the initial configuration
        for nextCounter in itertools.count(): # Step through the turing machine until max_steps is reached
            tm.next(self.transition) # Call next transition function
            print(self.createConfig(tm.config)) # Print the configuration
            # Check to see if we are in the final state, return the final state and tape contents and end program
            if tm.state in fstates:
                return fstates[tm.state], tm.contents # If so, return the final state and the current tape
            # Set step count to ensure that we don't get into an infinite loop or a TM that takes way too long
            if nextCounter > max_steps:
                raise RuntimeError("Max counter reached")