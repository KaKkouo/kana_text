#!/usr/bin/python
import sys
import unittest

from src import KanaText
from . import dataset0

#askana()の基本チェック
testcase01i = dataset0.dataset

testcase01o = [   #想定する結果
    "よみ１", "よみ２", "よみ３", "よみ４", "よみ５", "", "", "", "", "",
    "よみ１", "よみ２", "よみ３", "よみ４", "よみ５", "", "", "", "", "",
    "よみ１", "よみ２", "よみ３", "よみ４", "よみ５", "", "", "", "", "",
    "", "", ""
    ]

class testKanaText(unittest.TestCase):
    #askanaの基本チェック
    def test01_askana(self):
        for t, e in zip(testcase01i, testcase01o):
            term = KanaText(t)
            rslt = term.askana()
            self.assertEqual(e, rslt)

def main():
    unittest.main()

if __name__ == '__main__':
    unittest.main()
