#!/usr/bin/python
import sys
import pytest

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

#askanaの基本チェック
def test01_askana():
    for t, e in zip(testcase01i, testcase01o):
        term = KanaText(t)
        rslt = term.askana()
        assert rslt == e
