#!/usr/bin/python
import sys
import unittest

from src import KanaText
from . import dataset0

#正規表現による字句解析
testcase1i = dataset0.dataset

testcase1o = [   #想定する結果
    "よみ１|用語１",
    "よみ２|用語２",
    "よみ３|用語３",
    "よみ４|用語４",
    "よみ５|用語５",
    "用語６",
    "用語７",
    "用語８",
    "用語９",
    "用語Ａ",
    "よみ１|用語１",
    "よみ２|用語２",
    "よみ３|用語３",
    "よみ４|用語４",
    "よみ５|用語５",
    "用語６",
    "用語７",
    "用語８",
    "用語９",
    "用語Ａ",
    "よみ１|用語１",
    "よみ２|用語２",
    "よみ３|用語３",
    "よみ４|用語４",
    "よみ５|用語５",
    "用語６",
    "用語７",
    "用語８",
    "用語９",
    "用語Ａ",
    "", "", ""]

class testKanaText(unittest.TestCase):
    #正規表現による字句解析
    def test01_assort(self):
        for t, e in zip(testcase1i, testcase1o):
            term = KanaText(t)
            rslt = term.assort()
            self.assertEqual(e, rslt)

def main():
    unittest.main()

if __name__ == '__main__':
    unittest.main()
