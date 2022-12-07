test_input = '''$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
'''

TYPE_DIR  = 0
TYPE_FILE = 1

# pretty disgusting imo
class node:
    def __init__(self, parent, name, type=TYPE_DIR, size=0):
        self.parent = parent
        self.type = type
        self.name = name
        self.size = size
        self.total_size = 0
        self.children = {}

    def update_total_size(self):
        if self.type == TYPE_DIR:
            for child in self.children.values():
                child.update_total_size()
                self.total_size += child.total_size
        elif self.type == TYPE_FILE:
            self.total_size = self.size

    def add_child(self, other):
        self.children[other.name] = other
        return other

    # waste of time but fun
    def ls(self, depth=0):
        print('  ' * depth + '- ' + self.name, end=' ')
        if self.type == TYPE_DIR:
            print('(dir)')
        elif self.type == TYPE_FILE:
            print('(file, size={})'.format(self.size))
        directories = sorted([name for name, item in self.children.items() if item.type == TYPE_DIR])
        files = sorted([name for name, item in self.children.items() if item.type == TYPE_FILE])
        for dir in directories:
            self.children[dir].ls(depth + 1)
        for file in files:
            self.children[file].ls(depth + 1)

    # also waste of time, but also fun
    def print(self):
        print('/')
        if self.type == TYPE_DIR:
            if self.parent:
                self.parent.print()
                print(self.name, end='')
        else:
            print(self.name, end='')

    # I guess
    def filtered(self, limit):
        accum = 0
        if self.type == TYPE_DIR:
            if self.total_size <= limit:
                accum += self.total_size
            for child in self.children.values():
                accum += child.filtered(limit)
        return accum

    # Why not
    def find_max_limit(self, limit):
        n = None
        if self.type == TYPE_DIR and self.total_size >= limit:
            n = self
            for child in self.children.values():
                m = child.find_max_limit(limit)
                if m and m.total_size < n.total_size:
                    n = m
        return n

# Dont ask me
class filesystem:
    def __init__(self):
        self.root = node(None, '/')
        self.cur = self.root

    def update_total_size(self):
        self.root.update_total_size()

    def list(self):
        self.root.ls()

    def cd(self, dir):
        if dir == '/':
            self.cur = self.root
        elif dir == '..':
            self.cur = self.cur.parent
        else:
            self.cur = self.add_directory(dir)

    def add_directory(self, name):
        return self.cur.add_child(node(self.cur, name))

    def add_file(self, size, name):
        return self.cur.add_child(node(self.cur, name,TYPE_FILE, size))

    def filter_directory_size(self, size):
        return self.root.filtered(size)
    
    def find_optimal(self, fs_size, min_free_space):
        free_space = fs_size - self.root.total_size
        return self.root.find_max_limit(min_free_space - free_space)

# Why no coroutines? Start using it ffs
def parse_output(fs, line, lines):
    while line and not line[0] == '$':
        parts = line.split()
        if parts[0] == 'dir':
            # skip
            pass
        else:
            fs.add_file(int(parts[0]), parts[1])
        line = next(lines, None)
    return line

#TeriFrown
def parse_cmd(fs, line, lines):
    parts = line.split()
    cmd = parts[1]
    if cmd == 'cd':
        fs.cd(parts[2])
        return next(lines, None)
    elif cmd == 'ls':
        line = next(lines, None)
        return parse_output(fs, line, lines)

def parse(lines):
    fs = filesystem()
    line = next(lines, None)
    while line:
        if line[0] == '$':
            line = parse_cmd(fs, line, lines)
    return fs

def part1(input):
    fs = parse(iter(input.strip().split('\n')))
    fs.list()
    fs.update_total_size()
    result = fs.filter_directory_size(100000)
    print("Part 1: {}".format(result))

def part2(input):
    fs = parse(iter(input.strip().split('\n')))
    fs.update_total_size()
    result = fs.find_optimal(70000000, 30000000)
    print("Part 2: {}".format(result.total_size))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)

# N E X T