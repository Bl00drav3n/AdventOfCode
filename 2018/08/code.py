class Node():
    def __init__(self):
        self.children = []
        self.metadata = None
    
    def add_child(self, node):
        self.children.append(node)

    def get_subtree_sum(self):
        s = sum(self.metadata)
        for child in self.children:
            s += child.get_subtree_sum()
        return s

    def get_value(self):
        if not self.children:
            return sum(self.metadata)
        else:
            s = 0
            for meta in self.metadata:
                if meta > 0 and meta <= len(self.children):
                    s += self.children[meta - 1].get_value()
            return s

class DataStream():
    def __init__(self, data):
        self.data = data
        self.at = 0

    def reset(self):
        self.at = 0
    
    def read_header(self):
        result = int(self.data[self.at]), int(self.data[self.at + 1])
        self.at += 2
        return result

    def read_count(self, count):
        result = list(map(int, self.data[self.at:self.at + count]))
        self.at += count
        return result
    
    def read(self):
        node = Node()
        child_count, meta_count = self.read_header()
        for i in range(0, child_count):
            node.add_child(self.read())
        node.metadata = self.read_count(meta_count)
        return node

with open('input.txt', "r") as f:
    data = f.read()
    #data = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"
    stream = DataStream(data.split(' '))
    root = stream.read()
    print(root.get_subtree_sum())
    print(root.get_value())