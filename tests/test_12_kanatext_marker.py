#!/usr/bin/python
import sys
import pytest

from src import KanaText
from . import dataset0, util

#正規表現による字句解析
testcase1i = dataset0.dataset2

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

#正規表現による字句解析
def test01_marker():
    for t, e in zip(testcase1i, testcase1o):
        KanaText.config = util.Config()
        KanaText.config.kana_text_option_marker = r'\#'
        term = KanaText(t)
        rslt = term.assort()
        assert rslt == e
        KanaText.config.kana_text_option_marker = r'\^'
