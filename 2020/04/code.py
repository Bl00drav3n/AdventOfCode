test_input_part1 = '''ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in'''

test_input_part2_invalid = '''eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007'''

test_input_part2_valid = '''pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719'''

def make_pair(pair):
    return pair.split(':')

def load_entry(entry):
    return {k:v for k, v in [make_pair(pair) for pair in entry.split(' ')]}

def load_passports(input):
    entries = [text.strip().replace('\n', ' ') for text in input.split('\n\n')]
    return [load_entry(entry) for entry in entries]

def is_dec_digit(value):
    return value in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def is_hex_digit(value):
    return is_dec_digit(value) or value in ['a', 'b', 'c', 'd', 'e', 'f']

def is_numeric_dec(value):
    for c in value:
        if not is_dec_digit(c):
            return False
    return True

def is_numeric_hex(value):
    for c in value:
        if not is_hex_digit(c):
            return False
    return True

def scan_for_first_nondigit(value):
    i = 0
    while i < len(value) and is_dec_digit(value[i]):
        i += 1
    return i

def validate_entry_part1(entry, fields_to_check):
    diff = fields_to_check - set(entry.keys())
    return len(diff) == 0

def validate_byr(value):
    ivalue = int(value)
    return ivalue >= 1920 and ivalue <= 2002

def validate_iyr(value):
    ivalue = int(value)
    return ivalue >= 2010 and ivalue <= 2020

def validate_eyr(value):
    ivalue = int(value)
    return ivalue >= 2020 and ivalue <= 2030

def validate_hgt(value):
    p = scan_for_first_nondigit(value)
    if p > 0 and p < len(value) - 1:
        ival = int(value[:p])
        if value[p:] == 'cm':
            return ival >= 150 and ival <= 193
        elif value[p:] == 'in':
            return ival >= 59 and ival <= 76
    return False

def validate_hcl(value):
    if value[0] == '#' and len(value) == 7:
        return is_numeric_hex(value[1:])
    return False

def validate_ecl(value):
    return value in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']

def validate_pid(value):
    return len(value) == 9 and is_numeric_dec(value)

def validate_entry_part2(entry, fields_to_check):
    if validate_entry_part1(entry, fields_to_check):
        return (validate_byr(entry['byr']) and
            validate_iyr(entry['iyr']) and
            validate_eyr(entry['eyr']) and
            validate_hgt(entry['hgt']) and
            validate_hcl(entry['hcl']) and
            validate_ecl(entry['ecl']) and
            validate_pid(entry['pid']))
    return False

def number_of_valid_passports(input, required_fields, validate):
    count = 0
    passports = load_passports(input)
    for p in passports:
        if validate(p, required_fields):
            count += 1
    return count

required_fields = set(['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'])
print("Number of valid passports part1 (TEST):", number_of_valid_passports(test_input_part1, required_fields, validate_entry_part1))
print("Number of valid passports part2 (TEST invalid):", number_of_valid_passports(test_input_part2_invalid, required_fields, validate_entry_part2))
print("Number of valid passports part2 (TEST valid):", number_of_valid_passports(test_input_part2_valid, required_fields, validate_entry_part2))
with open('input.txt') as file:
    file.seek(0)
    print("Number of valid passports part1:", number_of_valid_passports(file.read(), required_fields, validate_entry_part1))
    file.seek(0)
    print("Number of valid passports part2:", number_of_valid_passports(file.read(), required_fields, validate_entry_part2))