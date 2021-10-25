#!/usr/bin/python
import sys
import unittest
sys.path.append('sphinxcontrib')
from src import KanaText

from . import dataset0

#len()の基本チェック
testcase01i = dataset0.dataset

testcase01o = [   #想定する結果
    2, 2, 2, 2, 2, 1, 1, 1, 1, 1,
    2, 2, 2, 2, 2, 1, 1, 1, 1, 1,
    2, 2, 2, 2, 2, 1, 1, 1, 1, 1,
    #0, 0, 0, #0.22.0/対応保留
    ]

class testKanaText(unittest.TestCase):
    #lenで基本チェック
    def test01_len(self):
        for t, e in zip(testcase01i, testcase01o):
            term = KanaText(t)
            rslt = len(term)
            self.assertEqual(e, rslt)

def main():
    unittest.main()

if __name__ == '__main__':
    unittest.main()
