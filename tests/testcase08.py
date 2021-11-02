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

def main():
    unittest.main()

if __name__ == '__main__':
    unittest.main()
