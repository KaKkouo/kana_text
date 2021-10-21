#!/usr/bin/python
import sys
import unittest
sys.path.append('sphinxcontrib')
from src import KanaText

from . import dataset0

#askana()の基本チェック
testcase7i = dataset0.dataset

testcase7o = [   #想定する結果
    "よみ１", "よみ２", "よみ３", "よみ４", "よみ５", "", "", "", "", "",
    "よみ１", "よみ２", "よみ３", "よみ４", "よみ５", "", "", "", "", "",
    "よみ１", "よみ２", "よみ３", "よみ４", "よみ５", "", "", "", "", "",
    "", "", ""
    ]

class testKanaText(unittest.TestCase):
    #askanaの基本チェック
    def test07_askana(self):
        for t, e in zip(testcase7i, testcase7o):
            term = KanaText(t)
            rslt = term.askana()
            self.assertEqual(e, rslt)

def main():
    unittest.main()

if __name__ == '__main__':
    unittest.main()
