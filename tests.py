import unittest
from permlook import Word

class TestWord(unittest.TestCase):

    def test_cmp(self):
        with self.assertRaises(Exception):
            Word("")
        self.assertTrue(Word("foo")==Word("foo"))
        self.assertFalse(Word("foo")==Word("bar"))
        self.assertFalse(Word("foo")==Word("fooder"))
        self.assertTrue(Word("fooder")==Word("fodoer"))
        self.assertFalse(Word("fooder")==Word("ofoder"))
        self.assertFalse(Word("fooder")==Word("foodre"))
        self.assertFalse(Word("fooder")==Word("roodef"))

    def test_occurs(self):


if __name__ == '__main__':
    unittest.main()