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
                    current = current.keys[i+1]
                    break
                elif value < temp[i]:
                    current = current.keys[i]
                    break
                elif i + 1 == len(current.values):
                    current = current.keys[i+1]
                    break
        return current

    def get_first_leaf(self):
        current = self.root
        while not current.isLeaf:
            current = current.keys[0]

        return current

    def key_search(self, key):
        """
        Search for the leaf node that may contain the given key.

        Parameters:
        key (int/float/str): The key to search for.

        Returns:
        Node: The leaf node where the key should be located.
        """
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

    # key_start is inclusive, key_end is exclusive
    def sum(self, key_start=None, key_end=9999999999999999):
        current = self.root

        if current is None:
            raise KeyError(f'Key {key_start} not found')

        if key_start is not None:
            current = self.key_search(key_start)
        else:
            while not current.isLeaf:
                if isinstance(current.keys[0], Node):
                    current = current.keys[0]
                    continue

        sum = 0
        while True:
            for val, key in zip(current.values, current.keys):
                if key < key_end:
                    sum += int(val)

            if current.next is not None:
                current = current.next
            else:
                return sum



    def remove(self, value):
        pass

    def update(self, key, value):
        pass

if __name__ == '__main__':
    bplustree = BPlusTree(3)
    dates = ["11/22/2024", "11/21/2024", "11/20/2024", "11/19/2024", "11/18/2024"]
    values = ['5', '15', '25', '35', '45']

    for value, date in zip(values, dates):
        formatted_date = date.split('/')
        formatted_date = datetime(int(formatted_date[2]), int(formatted_date[0]), int(formatted_date[1])).timestamp()
        bplustree.insert(value, formatted_date)

    bplustree.print_tree()
    test_date = "11/22/2024".split('/')
    sumo = bplustree.sum(datetime(int(test_date[2]), int(test_date[0]), int(test_date[1])).timestamp())
    pass