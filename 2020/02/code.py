import io

test_input = io.StringIO('''1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc''')

def get_entries(iobuffer):
    iobuffer.seek(0)
    return [input.strip().split(': ') for input in iobuffer.readlines()]

def get_policy(entry):
    return entry[0]

def get_password(entry):
    return entry[1]

def get_valid_password_count(input, validate):
    entries = get_entries(input)
    return len([entry for entry in entries if validate(entry)])

def validate_entry_part1(entry):
    policy = get_policy(entry)
    password = get_password(entry)
    policy_letter_limits, policy_letter = tuple(policy.split(' '))
    policy_letter_limit_bounds = [int(x) for x in policy_letter_limits.split('-')]
    letter_count = password.count(policy_letter)
    return letter_count >= policy_letter_limit_bounds[0] and letter_count <= policy_letter_limit_bounds[1]

def validate_entry_part2(entry):
    policy = get_policy(entry)
    password = get_password(entry)
    policy_letter_positions, policy_letter = tuple(policy.split(' '))
    policy_letter_positions = [int(x)-1 for x in policy_letter_positions.split('-')]
    return (password[policy_letter_positions[0]] == policy_letter) ^ (password[policy_letter_positions[1]] == policy_letter)

print('Valid test passwords 1:', get_valid_password_count(test_input, validate_entry_part1))
print('Valid test passwords 2:', get_valid_password_count(test_input, validate_entry_part2))
with open('input.txt') as file:
    print('Valid passwords 1:', get_valid_password_count(file, validate_entry_part1))
    print('Valid passwords 2:', get_valid_password_count(file, validate_entry_part2))