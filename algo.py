from tmsim import *
from termcolor import colored

## Algorithm class defining the input file
class Algorithm:

    # Create initial object for TM data
    def __init__(
        self,
        funcdict,
        *,
        blank_symbol='[]',
        initial_state='q_s',
        states=(True, False),
        symbols=(),
        arrows={
            '<-': lambda x: x-1,
            '->': lambda x: x+1,
        },
        empty_word_representation='ε',
        symbols_representations={'[]': '□'},
    ):
        # Set init vars
        self.blank_symbol, self.initial_state = blank_symbol, initial_state
        self.empty_word_representation, self.symbols_representations = empty_word_representation, symbols_representations

        states = set(funcdict.keys()).union(states) # Create set of all states in TM
        symbols = set(symbol for values in funcdict.values() for symbol in values.keys()).union(symbols) # Creates set of tape alphabet

        # Check all combinations of states, symbols and arrows
        for (label1, set1), (label2, set2) in itertools.combinations({'states': states, 'symbols': symbols, 'arrows': arrows}.items(), 2):
            if not set1.isdisjoint(set2):
                raise ValueError(f'Sets of {label1} and {label2} are not disjoint')


        self.states_max_length = max(len(str(state)) for state in states) # Calculates the largest string of all state names as int

        # Function to parse information for each transition
        def parse(old_state, old_symbol, value):
            if not isinstance(value, tuple):
                value = (value,) # If value isn't a tuple, set it to a tuple

            new_symbol, new_state, new_arrow = None, None, None
            for K in value: # Depending on what temp var K is, store it in respective var
                if K in arrows:
                    new_arrow = K
                elif K in states:
                    new_state = K
                elif K in symbols:
                    new_symbol = K
                else:
                    raise ValueError(f'Not a valid transition') # If not a valid transition, error

            # Set new values from parsed data, then return values
            symbol = new_symbol if new_symbol is not None else old_symbol
            state = new_state if new_state is not None else old_state
            head_movement_function = arrows[new_arrow] if new_arrow else lambda x: x
            return symbol, state, head_movement_function

        self.transition_function = {
            (state, symbol): parse(state, symbol, value)
            for state, symbols_to_values in funcdict.items()
            for symbol, value in symbols_to_values.items()
        }

    def form_seq(self, sequence, *, replace_empty_word=True):
        if not sequence and replace_empty_word and self.empty_word_representation is not None:
            return self.empty_word_representation
        return ''.join((str(self.symbols_representations.get(symbol, symbol)) for symbol in sequence))

    # Function to define how to format the output of the program
    def format_configuration(self, configuration):
        leftHead, state, (symbol, *rightHead) = configuration
        return ''.join((
            f'({state})'.ljust(self.states_max_length+5), # Display current state, then buffer of max state string length+OFFSET
            self.form_seq(leftHead, replace_empty_word=False), # Display left side of current head
            colored(self.form_seq((symbol,)), attrs=['underline']), # Underline current head position
            self.form_seq(rightHead, replace_empty_word=False) # Display right side of current head
        ))

    ## Definition of run to execute the program
    def run(
        self,
        initial_sequence,
        *,
        final_states={
            True: True,
            False: False,
            'q_y': True,
            'q_n': False
        },
        run_limit=1_000,
        raise_on_exceed=True,
    ):

        # Below is the main driver of the code

        tm = TuringMachine(initial_sequence, blank_symbol=self.blank_symbol, initial_state=self.initial_state)
        print(self.format_configuration(tm.configuration)) # Print the initial configuration
        for step in itertools.count(): # Step through the turing machine
            tm.step(self.transition_function) # Call step function
            print(self.format_configuration(tm.configuration)) # Print the configuration

            # If we are in the final state, return the final state and tape contents and end program
            if tm.state in final_states:
                return final_states[tm.state], tm.tape_contents

            # Set step count to ensure that we don't get into an infinite loop or a TM that takes way too long
            if run_limit is not None and step > run_limit:
                if raise_on_exceed:
                    raise RuntimeError(f'Step limit of {run_limit} exceeded')
                else:
                    return None