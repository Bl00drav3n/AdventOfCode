import time
import sys
import math
from typing import no_type_check_decorator
test_input = '''[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]'''

def isregular(n):
    return isinstance(n, int)

class node:
    def __init__(self, parent):
        self.parent = parent
        self.values = [None, None]

    def tolist(self):
        a = self.values[0] if isregular(self.values[0]) else self.values[0].tolist()
        b = self.values[1] if isregular(self.values[1]) else self.values[1].tolist()
        return [a, b]
    
    def remove(self, n):
        if n == self.values[0]:
            self.values[0] = 0
        elif n == self.values[1]:
            self.values[1] = 0
        else:
            sys.exit('Error removing node from tree')

    def findfirstbydepth(self, depth):
        if isregular(self.values[0]) and isregular(self.values[1]) and depth <= 0:
            return self

        n = None
        if not isregular(self.values[0]):
            n = self.values[0].findfirstbydepth(depth - 1)
        if n:
            return n

        if not isregular(self.values[1]):
            n = self.values[1].findfirstbydepth(depth - 1)
        return n if n else None
            
        
    def findfirstlargeregular(self):
        n = None
        if isregular(self.values[0]):
            if self.values[0] > 9:
                return self
        else:
            n = self.values[0].findfirstlargeregular()
        if n:
            return n
        if isregular(self.values[1]):
            if self.values[1] > 9:
                return self
        else:
            n = self.values[1].findfirstlargeregular()
        return n if n else None
   
    def findclosestleftregular(self):
        return self if isregular(self.values[0]) else self.values[0].findclosestleftregular()

    def findclosestrightregular(self):
        return self if isregular(self.values[1]) else self.values[1].findclosestrightregular()
    
    def maxdepth(self):
        depth_a = 0 if isregular(self.values[0]) else 1 + self.values[0].maxdepth()
        depth_b = 0 if isregular(self.values[1]) else 1 + self.values[1].maxdepth()
        return max(depth_a, depth_b)

    def maxregular(self):
        a = self.values[0] if isregular(self.values[0]) else self.values[0].maxregular()
        b = self.values[1] if isregular(self.values[1]) else self.values[1].maxregular()
        return max(a, b)

    def magnitude(self):
        a = 3 * (self.values[0] if isregular(self.values[0]) else self.values[0].magnitude())
        b = 2 * (self.values[1] if isregular(self.values[1]) else self.values[1].magnitude())
        return a + b

class tree:
    def __init__(self, number):
        self.root = node(None)
        self.parse(self.root, number)
        self.normalize()
        #print('new tree:      ', self.tostring(), self.maxdepth(), self.maxregular())

    def parse(self, parent, n):
        if isregular(n[0]):
            parent.values[0] = n[0]
        else:
            parent.values[0] = node(parent)
            self.parse(parent.values[0], n[0])
        if isregular(n[1]):
            parent.values[1] = n[1]
        else:
            parent.values[1] = node(parent)
            self.parse(parent.values[1], n[1])
                   
    def tolist(self):
        return self.root.tolist()

    def tostring(self):
        return str(self.tolist()).replace(' ', '')

    def magnitude(self):
        return self.root.magnitude()

    def add(self, other):
        result = tree([self.tolist(), other.tolist()])
        #print('after addition:', result.tostring(), result.maxdepth(), result.maxregular())
        return result

    def maxdepth(self):
        return self.root.maxdepth()

    def maxregular(self):
        return self.root.maxregular()

    def findfirstexplodable(self):
        return self.root.findfirstbydepth(4)

    def findfirstsplittable(self):
        return self.root.findfirstlargeregular()

    def normalize(self):
        #hashes = set()
        while True:
            '''
            hash = str(self.tolist())
            if hash in hashes:
                print('Dupe!')
            else:
                hashes.add(hash)
            '''
            n = self.findfirstexplodable()
            if n:
                self.explode(n)
                #print('after explode: ', self.tostring(), self.maxdepth(), self.maxregular())
                continue
            m = self.findfirstsplittable()
            if m:
                self.split(m)
                #print('after split:   ', self.tostring(), self.maxdepth(), self.maxregular())
            if not m and not n:
                break

    def explode(self, n):
        if not isregular(n.values[0]) or not isregular(n.values[1]):
            sys.exit('We are trying to explode something that is not a leaf!')
        
        # LHS
        p = n.parent
        m = n
        while p:
            if isregular(p.values[0]):
                p.values[0] += n.values[0]
                break
            elif p.values[0] != m:
                r = p.values[0].findclosestrightregular()
                if isregular(r.values[1]):
                    r.values[1] += n.values[0]
                elif isregular(r.values[0]):
                    r.values[0] += n.values[0]
                else:
                    sys.exit('Invalid tree structure')
                break
            m = p
            p = p.parent
        
        # RHS
        p = n.parent
        m = n
        while p:
            if isregular(p.values[1]):
                p.values[1] += n.values[1]
                break
            elif p.values[1] != m:
                r = p.values[1].findclosestleftregular()
                if isregular(r.values[0]):
                    r.values[0] += n.values[1]
                elif isregular(r.values[1]):
                    r.values[1] += n.values[1]
                else:
                    sys.exit('Invalid tree structure')
                break
            m = p
            p = p.parent
        
        # Replace with regular 0
        n.parent.remove(n)

    def split(self, n):
        if isregular(n.values[0]) and n.values[0] > 9:
            snode = node(n)
            snode.values = [int(math.floor(n.values[0] / 2)), int(math.ceil(n.values[0] / 2))]
            n.values[0] = snode
        elif isregular(n.values[1]) and n.values[1] > 9:
            snode = node(n)
            snode.values = [int(math.floor(n.values[1] / 2)), int(math.ceil(n.values[1] / 2))]
            n.values[1] = snode
        else:
            sys.exit("Invalid split")            

def part1(input):
    t0 = time.time_ns()
    numbers = [tree(eval(line)) for line in input.strip().split('\n')]
    s = numbers.pop(0)
    while numbers:
        s = s.add(numbers.pop(0))
    mag = s.magnitude()
    t1 = time.time_ns()
    print("Part 1: The magnitude of the final sum is {} ({}ms)".format(mag, (t1 - t0) / 1e6))

def part2(input):
    t0 = time.time_ns()
    numbers = [tree(eval(line)) for line in input.strip().split('\n')]
    magmax = 0
    for i, a in enumerate(numbers):
        for j, b in enumerate(numbers):
            if i != j:
                magmax = max(magmax, a.add(b).magnitude())
    t1 = time.time_ns()
    print("Part 2: Ther largest magnitude of any sum of two numbers is {} ({}ms)".format(magmax, (t1 - t0) / 1e6))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)