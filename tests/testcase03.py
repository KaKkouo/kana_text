#!/usr/bin/python
import sys
import unittest
sys.path.append('sphinxcontrib')
from src import KanaText

from . import dataset0

#self.ashier()の基本チェック
testcase6i = dataset0.dataset

testcase6o = [   #想定する結果
    "用語１", "用語２", "用語３", "用語４", "用語５",
    "用語６", "用語７", "用語８", "用語９", "用語Ａ",
    "用語１", "用語２", "用語３", "用語４", "用語５",
    "用語６", "用語７", "用語８", "用語９", "用語Ａ",
    "用語１", "用語２", "用語３", "用語４", "用語５",
    "用語６", "用語７", "用語８", "用語９", "用語Ａ",
    "", "", ""]

class testKanaText(unittest.TestCase):
    #ashierの基本チェック
    def test06_ashier(self):
        for t, e in zip(testcase6i, testcase6o):
            term = KanaText(t)
            rslt = term.ashier()
            self.assertEqual(e, rslt)

def main():
    unittest.main()

if __name__ == '__main__':
    unittest.main()
