import unittest
from BPlusTree import BPlusTree, Node


class MyTestCase(unittest.TestCase):
    def test_search(self):
        tree = BPlusTree(3)
        result = tree.search('5')
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
