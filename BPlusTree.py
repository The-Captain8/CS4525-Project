import math
from datetime import datetime


class Node:
    def __init__(self, order):
        self.order = order
        self.values = []
        self.keys = []
        self.next = None
        self.parent = None
        self.isLeaf = False

    def insert_at_leaf(self, leaf, value, key):
        if self.values:
            temp = self.keys
            for i in range(len(temp)):
                if key == temp[i]:
                    self.keys[i].append(key)
                    break
                elif key < temp[i]:
                    self.values = self.values[:i] + [value] + self.values[i:]
                    self.keys = self.keys[:i] + [key] + self.keys[i:]
                    break
                elif i + 1 == len(temp):
                    self.values.append(value)
                    self.keys.append(key)
                    break
        else:
            self.values = [value]
            self.keys = [key]


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
                    current = current.keys[i + 1]
                    break
                elif value < temp[i]:
                    current = current.keys[i]
                    break
                elif i + 1 == len(current.values):
                    current = current.keys[i + 1]
                    break
        return current

    def get_first_leaf(self):
        current = self.root
        while not current.isLeaf:
            current = current.keys[0]

        return current

    def key_search(self, key):
        current = self.get_first_leaf()

        while True:
            for i in current.keys:
                if i == key:
                    return current

            current = current.next
            if current is None:
                break

        return None

    def find(self, value, key):
        l = self.search(value)
        for i, item in enumerate(l.values):
            if item == value:
                if key in l.key[i]:
                    return True
                else:
                    return False
        return False

    def insert(self, value, key: int):
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
            node1.next = old_node.next

            old_node.values = old_node.values[:mid + 1]
            old_node.keys = old_node.keys[:mid + 1]
            old_node.next = node1
            self.insert_in_parent(old_node, node1.values[0], node1)

    def insert_in_parent(self, n, value, ndash):
        if (self.root == n):
            rootNode = Node(n.order)
            rootNode.values = [value]
            rootNode.keys = [n, ndash]

            self.root = rootNode
            n.parent = rootNode
            ndash.parent = rootNode
            return

        parentNode = n.parent
        temp = parentNode.keys
        for i in range(len(temp)):
            if temp[i] == n:
                parentNode.values = parentNode.values[:i] + [value] + parentNode.values[i:]
                parentNode.keys = parentNode.keys[:i + 1] + [ndash] + parentNode.keys[i + 1:]

                if len(parentNode.keys) > parentNode.order:
                    parentDash = Node(parentNode.order)
                    parentDash.parent = parentNode.parent

                    mid = int(math.ceil(parentNode.order / 2)) - 1
                    parentDash.values = parentNode.values[mid + 1:]
                    parentDash.keys = parentNode.keys[mid + 1:]

                    value_ = parentNode.values[mid]

                    if mid == 0:
                        parentNode.values = parentNode.values[:mid + 1]
                    else:
                        parentNode.values = parentNode.values[:mid]
                        parentNode.keys = parentNode.keys[:mid + 1]

                        for node in parentNode.keys:
                            node.parent = parentNode
                        for node in parentDash.keys:
                            node.parent = parentDash

                        self.insert_in_parent(parentNode, value_, parentDash)

    def print_tree(self):
        lst = [self.root]
        level = [0]
        leaf = None
        flag = 0
        lev_leaf = 0

        node1 = Node(str(level[0]) + str(self.root.values))

        while len(lst) > 0:
            x = lst.pop(0)
            lev = level.pop(0)
            if not x.isLeaf:
                for i, item in enumerate(x.keys):
                    print(item.values)
            else:
                for i, item in enumerate(x.keys):
                    print(item.values)
                if flag == 0:
                    lev_leaf = lev
                    leaf = x
                    flag = 1

    def get_key_range(self, key_start=None, key_end=9999999999999999):
        current = self.root
        return_set = []

        if current is None:
            raise KeyError(f'Key {key_start} not found')

        if key_start is not None:
            current = self.key_search(key_start)
        else:
            current = self.get_first_leaf()

        while True:
            for val, key in zip(current.values, current.keys):
                if key < key_end:
                    return_set.append([key, val])

            if current.next is not None:
                current = current.next
            else:
                return return_set

    # key_start is inclusive, key_end is exclusive
    def sum(self, key_start=None, key_end=9999999999999999):
        current = self.root

        if current is None:
            raise KeyError(f'Key {key_start} not found')

        if key_start is not None:
            current = self.key_search(key_start)
        else:
            current = self.get_first_leaf()

        sum = 0
        while True:
            for val, key in zip(current.values, current.keys):
                if key < key_end:
                    sum += float(val)

            if current.next is not None:
                current = current.next
            else:
                return sum

    def average(self, key_start=None, key_end=9999999999999999):
        current = self.root

        if current is None:
            raise KeyError(f'Key {key_start} not found')

        if key_start is not None:
            current = self.key_search(key_start)
        else:
            current = self.get_first_leaf()

        sum = 0
        counter = 0
        while True:
            for val, key in zip(current.values, current.keys):
                counter += 1
                if key < key_end:
                    sum += float(val)

            if current.next is not None:
                current = current.next
            else:
                if counter != 0:
                    return sum / counter

    def max(self, key_start=None, key_end=9999999999999999):
        current = self.root

        if current is None:
            raise KeyError(f'Key {key_start} not found')

        if key_start is not None:
            current = self.key_search(key_start)
        else:
            current = self.get_first_leaf()

        maximum = None
        while True:
            for val, key in zip(current.values, current.keys):
                if key < key_end:
                    int_val = int(val)
                    if maximum is None or int_val > maximum:
                        maximum = int_val

            if current.next is not None:
                current = current.next
            else:
                return maximum

    def min(self, key_start=None, key_end=9999999999999999):
        current = self.root

        if current is None:
            raise KeyError(f'Key {key_start} not found')

        if key_start is not None:
            current = self.key_search(key_start)
        else:
            current = self.get_first_leaf()

        minimum = None
        while True:
            for val, key in zip(current.values, current.keys):
                if key < key_end:
                    int_val = int(val)
                    if minimum is None or int_val < minimum:
                        minimum = int_val

            if current.next is not None:
                current = current.next
            else:
                return minimum
