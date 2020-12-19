test_input1 = '''0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
'''

test_input2 = '''42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
'''

class StringStream:
    def __init__(self, data):
        self.data = data
        self.pos = 0
    
    def peek(self):
        return self.data[self.pos]

    def seek(self, pos):
        if pos < 0:
            pos = 0
        elif pos >= len(self.data):
            pos = len(self.data)
        self.pos = pos

    def tell(self):
        return self.pos

    def read_character(self):
        if not self.good():
            return None
        ret = self.data[self.pos]
        self.pos += 1
        return ret

    def good(self):
        return self.pos >= 0 and self.pos < len(self.data)

    def eos(self):
        return self.pos == len(self.data)

    def __repr__(self):
        if self.good():
            return self.data[self.pos:]
        else:
            return ""

def parse_rule_number(token):
    return token[:token.find(':')]

def parse_rules(input):
    rules = {}
    for line in input.splitlines():
        rule_nr, rule = tuple([elem.strip() for elem in line.split(':')])
        rules[rule_nr] = [subrule.strip().split(' ') for subrule in rule.split('|')]
    return rules

def read_input(input):
    rules_str, messages = tuple(input.split('\n\n'))
    rules = parse_rules(rules_str)
    return rules, messages.splitlines()

def parse(rules, rule_nr, stream):
    # TODO(rav3n): This does not work for part2
    # The problem is, we can't differentiate between a message ending in [*a] and [*aa], where
    # [*a] means a string of a's and [*aa] means a string of a's ending with an extra a.
    pos = stream.tell()
    for subrule in rules[rule_nr]:
        error = False
        for elem in subrule:
            '''
            if stream.data == 'babbbbaabbbbbabbbbbbaabaaabaaa':
                print(stream, rule_nr, rules[rule_nr], subrule, elem)
                stream = stream
            '''
            if not stream.good():
                # NOTE(rav3n): This is where we go kaboom
                break
            if elem[0] == '"':
                error = stream.peek() != elem.split('"')[1]
                if not error:
                    stream.read_character()
            else:
                error = parse(rules, elem, stream) == False
            if error:
                stream.seek(pos)
                break
        if not error:
            return True
    return False

def parse_message(rules, message):
    stream = StringStream(message)
    return parse(rules, '0', stream) and stream.eos()
    
def check_input(rules, messages):
    return [(message, parse_message(rules, message)) for message in messages]

def print_results(results):
    [print('message: {} - {}'.format(message, 'valid' if result else 'invalid')) for (message, result) in results]

def patch(rules):
    rules['8'] = [['42'], ['42', '8']]
    rules['11'] = [['42', '31'], ['42', '11', '31']]
    return rules

def part1(input):
    results = check_input(*read_input(input))
    #print_results(results)
    print('Number of valid messages: {}'.format(len([result for result in results if result[1]])))

def part2(input):
    rules, messages = read_input(input)
    results = check_input(patch(rules), messages)
    #print_results(results)
    print('Number of valid messages (patched): {}'.format(len([result for result in results if result[1]])))

part1(test_input1)
part1(test_input2)
part2(test_input2)
with open('input.txt') as file:
    input = file.read()
    part1(input)
    part2(input)