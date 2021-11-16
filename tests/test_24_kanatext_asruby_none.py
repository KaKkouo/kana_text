#!/usr/bin/python
import sys
import pytest

from src import KanaText
from . import dataset0

#未入力/扱えない文字列
testcase01i = [
    '', '  ', '　　',
    'かな|^',
    ]

testcase01o = [None, None, None, None]

#非表示指定の「a-i」「q-y」の動作
def test01_asruby():
    for t, e in zip(testcase01i, testcase01o):
        term = KanaText(t)
        rslt = term.asruby()
        assert rslt == e
