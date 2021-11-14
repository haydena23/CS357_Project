import collections
import itertools
from termcolor import colored

## TuringMachine class
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
        # Set self vars based off of intial state
        self.blank_symbol, self.state, self.head_position = blank_symbol, initial_state, initial_head_position
        self.tape = collections.defaultdict(lambda: self.blank_symbol, enumerate(initial_sequence))

    # Function to return the current symbol at head_position
    @property
    def symbol(self):
        return self.tape[self.head_position]

    # Function to set the new symbol to current head position
    @symbol.setter
    def symbol(self, new_symbol):
        self.tape[self.head_position] = new_symbol

    # 
    @property
    def configuration(self):
        indices = self.tape.keys() # Split tape into array using keys in format [0,1,2..tapeMax]
        left, right = (min(indices), max(indices)) if indices else (0, 0) # Set the lowest and highest index of input string
        # Sets alpha as tape string
        alpha, beta = (
            tuple(self.tape[index] for index in range(*r))
            for r in ((left, self.head_position), (self.head_position, max(right, self.head_position)+1))
        )
        return alpha, self.state, beta

    # Function to remove blanks from string, and create tape by concatenating all symbols on self.tape 
    @property
    def tape_contents(self):
        indices = self.tape.keys()
        left, right = (min(indices), max(indices)) if indices else (0, 0)

        # Function to remove any blank symbols 
        def strip_blanks(iterable):
            return itertools.takewhile(
                lambda symbol: symbol != self.blank_symbol,
                itertools.dropwhile(lambda symbol: symbol == self.blank_symbol, iterable)
            )
        
        # Remove all blanks from symbols in tape, then concatenate all symbols from left edge to the right edge+1 to include one blank
        return ''.join(strip_blanks(self.tape[index] for index in range(left, right+1)))

    def step(self, transition_function):
        try:
            new_symbol, new_state, head_movement_func = transition_function[self.state, self.symbol]
        except KeyError:
            raise RuntimeError(f'Transition function not defined for state {self.state} and symbol {self.symbol}')

        self.symbol, self.state = new_symbol, new_state
        # yield self.configuration # after symbol change but before head movement
        self.head_position = head_movement_func(self.head_position)


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
        def parse_value(old_state, old_symbol, value):
            if not isinstance(value, tuple):
                value = (value,)

            new_symbol, new_state, new_arrow = None, None, None
            for v in value:
                if v in arrows:
                    new_arrow = v
                elif v in states:
                    new_state = v
                elif v in symbols:
                    new_symbol = v
                else:
                    raise ValueError(f'Invalid transition function value {v} for state {old_state} and symbol {old_symbol}')

            symbol = new_symbol if new_symbol is not None else old_symbol
            state = new_state if new_state is not None else old_state
            head_movement_func = arrows[new_arrow] if new_arrow else lambda x: x
            return symbol, state, head_movement_func

        self.transition_function = {
            (state, symbol): parse_value(state, symbol, value)
            for state, symbols_to_values in funcdict.items()
            for symbol, value in symbols_to_values.items()
        }

    def format_sequence(self, sequence, *, replace_empty_word=True):
        if not sequence and replace_empty_word and self.empty_word_representation is not None:
            return self.empty_word_representation
        return ''.join((str(self.symbols_representations.get(symbol, symbol)) for symbol in sequence))

    # Function to define how to format the output of the program
    def format_configuration(self, configuration):
        alpha, state, (symbol, *beta) = configuration
        return ''.join((
            colored(f'<{state}>'.ljust(self.states_max_length+5)), # Display current state, then buffer of max state string length+OFFSET
            self.format_sequence(alpha, replace_empty_word=False), # Display left side of current head
            colored(self.format_sequence((symbol,)), attrs=['underline']), # Underline current head position
            self.format_sequence(beta, replace_empty_word=False) # Display right side of current head
        ))

    ## Run function
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
        step_limit=1_000_000,
        raise_on_exceed=True,
    ):

        tm = TuringMachine(initial_sequence, blank_symbol=self.blank_symbol, initial_state=self.initial_state)
        print(self.format_configuration(tm.configuration)) # Print the initial configuration
        for step in itertools.count(): # Step through the turing machine
            tm.step(self.transition_function)
            print(self.format_configuration(tm.configuration))

            if tm.state in final_states:
                return final_states[tm.state], tm.tape_contents

            # Set step count to ensure that we don't get into an infinite loop
            if step_limit is not None and step > step_limit:
                if raise_on_exceed:
                    raise RuntimeError(f'Step limit of {step_limit} exceeded')
                else:
                    return None