#!/usr/bin/python
import sys
import pytest

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

#lenで基本チェック
def test01_len():
    for t, e in zip(testcase01i, testcase01o):
        term = KanaText(t)
        rslt = len(term)
        assert rslt == e
