import bitstring
import functools

test_input = '''9C0141080250320F1802104A08'''
version_sum = 0

operators = [
    sum,                                                     # 0
    lambda z: functools.reduce(lambda x, y: x * y, [1] + z), # 1
    min,                                                     # 2
    max,                                                     # 3
    lambda x: x[0],                                          # 4
    lambda x: int(x[0] > x[1]),                              # 5
    lambda x: int(x[0] < x[1]),                              # 6
    lambda x: int(x[0] == x[1])                              # 7
]

def read_header(stream):
    return stream.readlist('uint:3, uint:3')

def read_literal(stream):
    n = 0
    while True:
        prefix, group = stream.readlist('uint:1, uint:4')
        n = (n << 4) + group
        if not prefix:
            break
    return n

def read_packet(stream):
    global version_sum
    version, id = read_header(stream)
    version_sum += version
    packets = []
    if id == 4:
        # literal
        packets.append(read_literal(stream))
    else:
        # operator
        length_type_id = stream.read('uint:1')
        packets = []
        if length_type_id:
            count = stream.read('uint:11')
            packets = [read_packet(stream) for i in range(count)]
        else:
            length = stream.read('uint:15')
            sub_stream = bitstring.BitStream(bin=stream.read('bin:{}'.format(length)))
            while sub_stream.pos + 8 < sub_stream.len:
                packets.append(read_packet(sub_stream))
    return operators[id](packets)

def part1(input):
    global version_sum
    version_sum = 0
    stream = bitstring.BitStream(hex=input.strip())
    read_packet(stream)
    print("Part 1: The sum of version numbers of all packets is {}".format(version_sum))

def part2(input):
    stream = bitstring.BitStream(hex=input.strip())
    print("Part 2: The BITS expression evaluates to {}".format(read_packet(stream)))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)