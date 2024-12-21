test_input = '''
029A
980A
179A
456A
379A
'''

import math
import time

B_A     = 10
B_LEFT  = 11
B_RIGHT = 12
B_UP    = 13
B_DOWN  = 14

class Keypad:

    def get_input_direction(dx, dy):
        # Helper to determine which button to press on the upper layer's keypad
        # to move to the next button on the current keypad
        if dy == 0:
            if dx == 1: return B_RIGHT
            elif dx == -1: return B_LEFT
        elif dx == 0:
            if dy == 1: return B_DOWN
            elif dy == -1: return B_UP
        return None
    
    def __init__(self, layout, cursor_id):
        self.buttons = set()
        self.button_hashmap = {}
        self.button_pos = {}
        self.from_to_seq = {}

        self.process_layout(layout)

        # State of the keypad is tracked with this variable!
        self.cursor = self.button_hashmap[cursor_id]
        
    def process_layout(self, layout):
        # Read buttons and positions
        for y in range(len(layout)):
            for x in range(len(layout[y])):
                button_id = layout[y][x]
                if button_id != None:
                    b = Button(button_id)
                    self.buttons.add(b)
                    self.button_hashmap[b.id] = b
                    self.button_pos[b] = (x, y)
        
        # Set adjacencies for each button
        for button in self.buttons:
            pos = self.button_pos[button]
            for other_button in filter(lambda b: b != button, self.buttons):
                other_pos = self.button_pos[other_button]
                dx = other_pos[0] - pos[0]
                dy = other_pos[1] - pos[1]
                input_direction_id = Keypad.get_input_direction(dx, dy)
                if input_direction_id:
                    button.set_adjacent(other_button, input_direction_id)
        
        # Find the minimal paths from each button to each other button
        for button in self.buttons:
            hashmap = {}
            self.from_to_seq[button.id] = hashmap
            for other_button in self.buttons:
                stack = [(button, set(), [])]
                sequences = []
                while stack:
                    b, visited, path = stack.pop()
                    if not b in visited:
                        visited.add(b)
                        if b == other_button:
                            sequences.append(path)
                        for adj_button, direction_id in b.adj.items():
                            next_visited = visited.copy()
                            next_path = path.copy()
                            next_path.append(direction_id)
                            stack.append((adj_button, next_visited, next_path))
                min_length = len(min(sequences, key=len))
                hashmap[other_button.id] = list(filter(lambda s: len(s) == min_length, sequences))

    def input(self, button_id):
        # This may or may not be a sensible thing to do. We will just do it and fix it once it breaks.
        sequences = [s + [B_A] for s in self.from_to_seq[self.cursor.id][button_id]]
        # This is a state that we probably have to keep track of. But every sequence
        # ends with a press on A. :thinking_face:
        self.cursor.id = button_id
        return sequences
    
    def get_input_sequences(self, sequence):
        # Given an input sequence for a keypad, generate all output sequences
        subsequences = None
        for i in range(len(sequence)):
            new_sequences = self.input(sequence[i])
            if not subsequences:
                subsequences = [s for s in new_sequences]
            else:
                next_sequences = [None] * len(new_sequences) * len(subsequences)
                for j in range(len(subsequences)):
                    for k in range(len(new_sequences)):
                        next_sequences[j * len(new_sequences) + k] = list(subsequences[j]) + new_sequences[k]
                subsequences = next_sequences
        return subsequences

class Button:
    def __init__(self, button_id):
        self.id = button_id
        self.adj = {} # Neighbors

    def __repr__(self):
        mappings = { B_A: 'A', B_LEFT: '<', B_RIGHT: '>', B_UP: '^', B_DOWN: 'v' }
        return mappings[self.id] if self.id in mappings else str(self.id)
    
    def set_adjacent(self, button, input_direction_id):
        self.adj[button] = input_direction_id

def get_min_sequence_length(keypads, starting_sequence):
    # Finds the length of sequences with minimal length for a given starting sequence
    sequences = [starting_sequence]
    for keypad in keypads:
        next_seq = []
        for s in sequences:
            next_seq += keypad.get_input_sequences(s)
        sequences = next_seq
    return len(min(sequences, key=len))

def get_number_from_input(input):
    # Strip leading zeroes and return the number-part
    number = 0
    input = input.copy()
    while input[0] == 0:
        input.pop(0)
    for n in input:
        if n < 10:
            number *= 10
            number += n
    return number

def create_keypads(num_directional_layers):
    numeric_keypad_layout = [
        [   7, 8,   9],
        [   4, 5,   6],
        [   1, 2,   3],
        [None, 0, B_A],
    ]
    directional_keypad_layout = [
        [  None,   B_UP,     B_A],
        [B_LEFT, B_DOWN, B_RIGHT]
    ]
    
    numeric_keypad = Keypad(layout=numeric_keypad_layout, cursor_id=B_A)
    directional_keypads = [Keypad(layout=directional_keypad_layout, cursor_id=B_A) for _ in range(num_directional_layers)]

    keypads = [numeric_keypad] + directional_keypads
    return keypads

def find_complexity_slowly(keypads, input):
    # The bruteforce way, we try every sequence and check which ones are the shortest. (Very slow and memory intensive!)
    print("Processing {}...".format(input))
    input_sequence = [int(s) if s.isdigit() else B_A for s in input]
    minlen = get_min_sequence_length(keypads, input_sequence)
    number = get_number_from_input(input_sequence)
    complexity = number * minlen
    print("Complexity of {}.".format(complexity))
    return complexity

def find_complexity_efficiently(keypads, input):
    return 0

def print_time_diff(start, end):
    print("Time: {:.3f} sec".format((end - start)/1e9))

def part1(input):
    start = time.time_ns()
    keypads = create_keypads(num_directional_layers=2)

    total_complexity = 0
    for line in input.strip().split('\n'):
        total_complexity += find_complexity_slowly(keypads, line)
    end = time.time_ns()
    
    print("Part 1: The sum of the complexities is {}." .format(total_complexity))
    print_time_diff(start, end)

def part2(input):
    # TODO: How do we actually process this heccery to find the lengths without going through all possible sequences?
    keypads = create_keypads(num_directional_layers=25)

    total_complexity = 0
    for line in input.strip().split('\n'):
        total_complexity += find_complexity_efficiently(keypads, line)

    start = time.time_ns()
    end = time.time_ns()
    print("Part 2: TODO" .format())
    print_time_diff(start, end)

print('---TEST---')
part1(test_input)
part2(test_input)

with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)