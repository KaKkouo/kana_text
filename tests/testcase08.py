#!/usr/bin/python
import sys
import unittest

from src import KanaText

class testKanaText(unittest.TestCase):
    def test01_empty(self):
        term = KanaText('')
        self.assertEqual(repr(term), "<#empty>")
        self.assertEqual(term['kana'], None)
        self.assertEqual(term['hier'], "")

    def test02_raise(self):
        term = KanaText('用語零弐')
        with self.assertRaises(IndexError):
            text = term[2]
        with self.assertRaises(TypeError):
            text = term[(1, 1)]
        with self.assertRaises(AttributeError):
            term[3] = "よみ"
        with self.assertRaises(TypeError):
            term[(1, 1)] = "よみ"

    def test02_repr(self):
        term = KanaText("", "用語零参")
        self.assertEqual(repr(term), "<#rawtext: '用語零参'>")

def main():
    unittest.main()

if __name__ == '__main__':
    unittest.main()
