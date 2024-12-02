import math

class Node:
    def __init__(self, order):
        self.order = order
        self.values = []
        self.keys = []
        self.next = None
        self.parent = None
        self.isLeaf = False

    def leaf_search(self, value):
        current = self

        while not current.isLeaf:
            temp = current.values

            for i in range(len(temp)):
                if value == temp[i]:
                    current = current.keys[i+1]
                    break
                elif value < temp[i]:
                    current = current.keys[i]
                    break
                elif i + 1 == len(current.values):
                    current = current.keys[i+1]
                    break

        return current

    def insert_at_leaf(self, leaf, value, key):
        if self.values:
            temp = self.values
            for i in range(len(temp)):
                if value == temp[i]:
                    self.keys[i].append(key)
                    break
                elif value < temp[i]:
                    self.values = self.values[:i] + [value] + self.values[i:]
                    self.keys = self.keys[:i] + [[key]] + self.keys[i:]
                    break
                elif i + 1 == len(temp):
                    self.values.append(value)
                    self.keys.append([key])
                    break
        else:
            self.values = [value]
            self.keys = [[key]]



class BPlusTree:
    def __init__(self, order):
        self.root = Node(order)
        self.root.isLeaf = True

    def search(self, value):
        current = self.root

        while not current.isLeaf:
            temp = current.values
            for i in range(len(temp)):
                if value == temp[i]:
                    current = current.keys[i+1]
                    break
                elif value < temp[i]:
                    current = current.keys[i]
                    break
                elif i + 1 == len(current.values):
                    current = current.keys[i+1]
                    break
        return current

    def insert(self, value, key):
        value = str(value)
        old_node = self.search(value)
        old_node.insert_at_leaf(old_node, value, key)

        # If the node needs to be split
        if (len(old_node.values) == old_node.order):
            node1 = Node(old_node.order)
            node1.isLeaf = True
            node1.parent = old_node.parent

            mid = int(math.ceil(old_node.order / 2)) - 1
            node1.values = old_node.values[mid + 1:]
            node1.keys = old_node.keys[mid + 1:]
            node1.next = node1.next

            old_node.values = old_node.values[:mid + 1]
            old_node.keys = old_node.keys[:mid + 1]
            old_node.next = node1
            self.insert_in_parent(old_node, node1.values[0], node1)

    def remove(self, value):
        pass

    def update(self, key, value):
        pass
