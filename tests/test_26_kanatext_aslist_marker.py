#!/usr/bin/python
import sys
import pytest

from src import KanaText

#オプションの処理
testcase01i = [
    #テストパターン
    "よみ１|用語１",
    "よみ２|用語２^120q13",
    "よみ３|用語３^",
    "よみ４|用語４^10q13あいうえお",
    "よみ５|用語５^あいうえお",
    "用語６",
    "用語７^120q13",
    "用語８^",
    "用語９^120q13あいうえお",
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

#オプションの処理
def test01_aslist():
    for t, e in zip(testcase01i, testcase01o):
        term = KanaText(t)
        rslt = term.aslist()
        assert rslt == e
