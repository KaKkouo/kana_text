#!/usr/bin/python
import sys
import unittest
sys.path.append('sphinxcontrib')
from src import KanaText

from . import dataset0

#未入力/扱えない文字列
testcase5i = [
    '', '  ', '　　',
    'かな|^',
    ]

testcase5o = [None, None, None, None]

class testKanaText(unittest.TestCase):
    #非表示指定の「a-i」「q-y」の動作
    def test05_asruby(self):
        for t, e in zip(testcase5i, testcase5o):
            term = KanaText(t)
            rslt = term.asruby()
            self.assertEqual(e, rslt)

def main():
    unittest.main()

if __name__ == '__main__':
    unittest.main()
