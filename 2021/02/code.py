test_input = '''forward 5
down 5
forward 8
up 3
down 8
forward 2'''

PART1 = 1
PART2 = 2

POSH = 0
DEPTH = 1
AIM = 2

commands_part1 = {
    'down': lambda t, val: (t[POSH], t[DEPTH] + val),
    'up': lambda t, val: (t[POSH], t[DEPTH] - val),
    'forward': lambda t, val: (t[POSH] + val, t[DEPTH])
}

commands_part2 = {
    'down': lambda t, val: (t[POSH], t[DEPTH], t[AIM] + val),
    'up': lambda t, val: (t[POSH], t[DEPTH], t[AIM] - val),
    'forward': lambda t, val: (t[POSH] + val, t[DEPTH] + t[AIM] * val, t[AIM])
}

def update_pos(ins, pos, part):
    cmd, val = ins.split(' ')
    commands = commands_part1 if part == PART1 else commands_part2

    if cmd in commands:
        return commands[cmd](pos, int(val))
    else:
        print("Invalid command", cmd)

def travel(input, part):
    pos = (0, 0, 0)
    for ins in input:
        pos = update_pos(ins, pos, part)
    return pos

def part(input, part_nr):
    if not (part_nr == PART1 or part_nr == PART2):
        print("part_nr must be {} or {}".format(PART1, PART2))
        return

    dest = travel(input, part_nr)
    print("Part {}: The product of the final horizontal position and the final depth is {}.".format(part_nr, dest[POSH] * dest[DEPTH]))

print("--- TEST ---")
part(test_input.split('\n'), PART1)
part(test_input.split('\n'), PART2)
with open('input.txt') as f:
    print("\n--- INPUT ---")
    lines = f.readlines()
    part(lines, PART1)
    part(lines, PART2)