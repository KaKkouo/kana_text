#!/usr/bin/python
import sys
import pytest

from src import KanaText
from . import dataset0

#self.asideo()の基本チェック
testcase01i = dataset0.dataset

testcase01o = [   #想定する結果
    "用語１", "用語２", "用語３", "用語４", "用語５",
    "用語６", "用語７", "用語８", "用語９", "用語Ａ",
    "用語１", "用語２", "用語３", "用語４", "用語５",
    "用語６", "用語７", "用語８", "用語９", "用語Ａ",
    "用語１", "用語２", "用語３", "用語４", "用語５",
    "用語６", "用語７", "用語８", "用語９", "用語Ａ",
    "", "", ""]

#asideoの基本チェック
def test01_asideo():
    for t, e in zip(testcase01i, testcase01o):
        term = KanaText(t)
        rslt = term.astext()
        assert rslt == e
