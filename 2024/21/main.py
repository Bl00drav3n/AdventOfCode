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
    def __init__(self, layout, cursor_id):
        self.buttons = set()
        self.button_hashmap = {}
        self.button_pos = {}
        self.from_to_seq = {}

        self.process_layout(layout)
        self.cursor = self.button_hashmap[cursor_id]
        
    def process_layout(self, layout):
        for y in range(len(layout)):
            for x in range(len(layout[y])):
                button_id = layout[y][x]
                if button_id != None:
                    b = Button(button_id)
                    self.buttons.add(b)
                    self.button_hashmap[b.id] = b
                    self.button_pos[b] = (x, y)
        for button in self.buttons:
            pos = self.button_pos[button]
            for other_button in filter(lambda b: b != button, self.buttons):
                other_pos = self.button_pos[other_button]
                dx = other_pos[0] - pos[0]
                dy = other_pos[1] - pos[1]
                input_direction_id = Keypad.get_input_direction(dx, dy)
                if input_direction_id:
                    button.set_adjacent(other_button, input_direction_id)
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

    def get_input_direction(dx, dy):
        if dy == 0:
            if dx == 1: return B_RIGHT
            elif dx == -1: return B_LEFT
        elif dx == 0:
            if dy == 1: return B_DOWN
            elif dy == -1: return B_UP
        return None

    def input(self, button_id):
        # This may or may not be a sensible thing to do.
        sequences = [s + [B_A] for s in self.from_to_seq[self.cursor.id][button_id]]
        # This is a state that we probably have to keep track of
        self.cursor.id = button_id
        return sequences

class Button:
    def __init__(self, button_id):
        self.id = button_id
        self.adj = {}

    def __repr__(self):
        mappings = { B_A: 'A', B_LEFT: '<', B_RIGHT: '>', B_UP: '^', B_DOWN: 'v' }
        return mappings[self.id] if self.id in mappings else str(self.id)
    
    def set_adjacent(self, button, input_direction_id):
        self.adj[button] = input_direction_id

def get_input_sequences(keypad, sequence):
    subsequences = None
    for i in range(len(sequence)):
        new_sequences = keypad.input(sequence[i])
        if not subsequences:
            subsequences = [s for s in new_sequences]
        else:
            next_sequences = [None] * len(new_sequences) * len(subsequences)
            for j in range(len(subsequences)):
                for k in range(len(new_sequences)):
                    next_sequences[j * len(new_sequences) + k] = list(subsequences[j]) + new_sequences[k]
            subsequences = next_sequences
    return subsequences

def print_time_diff(start, end):
    print("Time: {:.3f} sec".format((end - start)/1e9))

def part1(input):
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
    directional_keypads = [Keypad(layout=directional_keypad_layout, cursor_id=B_A) for _ in range(3)]

    keypads = []
    keypads.append(numeric_keypad)
    keypads.append(directional_keypads[0])
    keypads.append(directional_keypads[1])
    keypads.append(directional_keypads[2])

    # TODO: How do we actually process this heccery to find the lengths?

    start = time.time_ns()
    end = time.time_ns()
    print("Part 1: " .format())
    print_time_diff(start, end)

def part2(input):
    start = time.time_ns()
    end = time.time_ns()
    print("Part 2: " .format())
    print_time_diff(start, end)

print('---TEST---')
part1(test_input)
part2(test_input)

with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)