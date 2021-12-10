import functools

test_input = '''[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]'''

def chunk_mappings():
    return { '(':')', '[':']', '{':'}', '<':'>' }

def parse_chunk(src, at, stack):
    chunks = chunk_mappings()
    if at == len(src):
        return 0

    c = src[at]
    if c in chunks.keys():
        stack.append(c)
    else:
        top = stack[-1]
        if c == chunks[top]:
            stack.pop()
        else:
            return c
    return parse_chunk(src, at + 1, stack)

def get_syntax_error_score(src):
    stack = []
    scores = {0:0, ')':3, ']':57, '}':1197, '>':25137}
    return scores[parse_chunk(src, 0, stack)]

def get_autocomplete_score(src):
    stack = []
    chunks = chunk_mappings()
    scores = {')':1, ']':2, '}':3, '>':4}
    if parse_chunk(src, 0, stack) != 0:
        print("ERROR: input is corrupted!")
    stack.reverse()
    return functools.reduce(lambda x, y: y + 5 * x, [scores[chunks[entry]] for entry in stack])
    
def part1(input):
    score = sum([get_syntax_error_score(line) for line in input.split('\n')])
    print("Part 1: The total synatx error score is {}".format(score))

def part2(input):
    lines = [line for line in input.split('\n') if get_syntax_error_score(line) == 0]
    scores = sorted([get_autocomplete_score(line) for line in lines])
    print("Part 2: The middle score is {}".format(scores[len(scores) // 2]))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read().strip()
    print('---INPUT---')
    part1(input)
    part2(input)