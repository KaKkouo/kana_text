#!/usr/bin/python
import sys
import unittest
sys.path.append('sphinxcontrib')
from src import KanaText

#オプションの処理
testcase01i = [
    #テストパターン
    "よみ１|用語１",
    "よみ２|用語２^120a3",
    "よみ３|用語３^",
    "よみ４|用語４^10a3あいうえお",
    "よみ５|用語５^あいうえお",
    "用語６",
    "用語７^120a3",
    "用語８^",
    "用語９^120a3あいうえお",
    "用語Ａ^あいうえお", ]

testcase01o = [   #想定する結果
    [(False, '用語１')],
    [(True, ('用', 'よ')), (True, ('語', 'み２')), (False, '２')],
    [(True, ('用語３', 'よみ３'))],
    [(True, ('用', 'よ')), (False, '語'), (False, '４')],
    [(True, ('用語５', 'よみ５'))],
    [(False, '用語６')],
    [(False, '用語７')],
    [(False, '用語８')],
    [(False, '用語９')],
    [(False, '用語Ａ')], ]

class testKanaText(unittest.TestCase):
    #オプションの処理
    def test01_asruby(self):
        for t, e in zip(testcase01i, testcase01o):
            term = KanaText(t)
            rslt = term.asruby()
            self.assertEqual(e, rslt)

def main():
    unittest.main()

if __name__ == '__main__':
    unittest.main()
