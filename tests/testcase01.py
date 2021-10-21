#!/usr/bin/python
import sys
import unittest
sys.path.append('sphinxcontrib')
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

#未入力/扱えない文字列
testcase5i = [
    '', '  ', '　　',
    'かな|^',
    ]

testcase5o = [None, None, None, None]

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

#askana()の基本チェック
testcase7i = dataset0.dataset

testcase7o = [   #想定する結果
    "よみ１", "よみ２", "よみ３", "よみ４", "よみ５", "", "", "", "", "",
    "よみ１", "よみ２", "よみ３", "よみ４", "よみ５", "", "", "", "", "",
    "よみ１", "よみ２", "よみ３", "よみ４", "よみ５", "", "", "", "", "",
    "", "", ""
    ]

#len()の基本チェック
testcase8i = dataset0.dataset

testcase8o = [   #想定する結果
    2, 2, 2, 2, 2, 1, 1, 1, 1, 1,
    2, 2, 2, 2, 2, 1, 1, 1, 1, 1,
    2, 2, 2, 2, 2, 1, 1, 1, 1, 1,
    #0, 0, 0, #0.22.0/対応保留
    ]

class testKanaText(unittest.TestCase):
    #正規表現による字句解析
    def test01_astext(self):
        for t, e in zip(testcase1i, testcase1o):
            term = KanaText(t)
            rslt = term.astext()
            self.assertEqual(e, rslt)

    #非表示指定の「a-i」「q-y」の動作
    def test05_asruby(self):
        for t, e in zip(testcase5i, testcase5o):
            term = KanaText(t)
            rslt = term.asruby()
            self.assertEqual(e, rslt)

    #ashierの基本チェック
    def test06_ashier(self):
        for t, e in zip(testcase6i, testcase6o):
            term = KanaText(t)
            rslt = term.ashier()
            self.assertEqual(e, rslt)

    #askanaの基本チェック
    def test07_askana(self):
        for t, e in zip(testcase7i, testcase7o):
            term = KanaText(t)
            rslt = term.askana()
            self.assertEqual(e, rslt)

    #lenで基本チェック
    def test08_len(self):
        for t, e in zip(testcase8i, testcase8o):
            term = KanaText(t)
            rslt = len(term)
            self.assertEqual(e, rslt)

def main():
    unittest.main()

if __name__ == '__main__':
    unittest.main()
