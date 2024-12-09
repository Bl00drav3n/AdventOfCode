test_input = '''2333133121414131402'''

class Block:
    def __init__(self):
        self.id = None
        self.pos = 0
        self.size = 0

    def checksum(self):
        return self.id * sum(range(self.pos, self.pos + self.size))

    def print(self):
        print("Block id={}, start={}, size={}".format(self.id, self.pos, self.size))

def read_input(input):
    input = input.strip()
    blocks = []
    index = 0
    block_id = 0
    for i in range(len(input)):
        block = Block()
        blocks.append(block)
        block.pos = index
        block.size = int(input[i])
        index += block.size
        if i % 2 == 0:
            block.id = block_id
            block_id += 1
    return blocks

def part1(input):
    blocks = read_input(input)    
    result = []
    # Kinda busted, wont fix
    while blocks:
        block = blocks.pop(0)
        if block.id == None:
            if blocks:
                free_block = block
                last_block = blocks.pop()
                if last_block.id:
                    assert free_block.id == None, "Expected free block!"
                    assert last_block.id != None, "Expected filled block!"
                    if free_block.size < last_block.size:
                        free_block.id = last_block.id
                        last_block.size -= free_block.size
                        blocks.append(last_block)
                        result.append(free_block)
                    elif free_block.size > last_block.size:
                        last_block.pos = free_block.pos
                        free_block.pos += last_block.size
                        free_block.size -= last_block.size
                        blocks.insert(0, free_block)
                        result.append(last_block)
                    else:
                        last_block.pos = free_block.pos
                        result.append(last_block)
        else:
            result.append(block)
        if blocks and blocks[-1].id == None:
            blocks.pop()

    print("Part 1: {}".format(sum([block.checksum() for block in result])))

def part2(input):
    blocks = read_input(input)

    # Slow because we are lazy and don't track free blocks
    result = []
    while blocks:
        last_block = blocks.pop()
        if last_block.id == None:
            continue
        for block in blocks:
            if block.id == None:
                free_block = block
                if free_block.size >= last_block.size:
                    last_block.pos = free_block.pos
                    free_block.pos += last_block.size
                    free_block.size -= last_block.size
                    break
                
        result.append(last_block)

    print("Part 2: {}".format(sum([block.checksum() for block in result])))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)