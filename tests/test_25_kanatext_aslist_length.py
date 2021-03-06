#!/usr/bin/python
import sys
import pytest

from src import KanaText

#オプションと文字データの文字数の多少
testcase01i = [ #テストケース
    'いろはにほへと|壱弐参四五六七八九',
    'いろはにほへと|壱弐参四五六七八九^',
    'いろはにほへと|壱弐参四五六七八九^111010111',
    'いろはにほへと|壱弐参四五六七八九^1201012',
    'いろはにほへと|壱弐参四五六七八九^33',
    'いろはにほへと|壱弐参四五六七八九^45',
    'いろはにほへと|壱弐参四五六七八九^55',
    'いろはにほへと|壱弐参四五六七八九^0000000000',
    'いろはにほへと|壱弐参四五六七八九^y9',
    'いろはにほへと|壱弐参四五六七八九^lmn7',
    'いろはにほへと|壱弐参四五六七八九^lmn9',
    'いろはにほへと|壱弐参四五六七八九^lmn55',
        ]

testcase01o = [   #期待する結果
    [(False, '壱弐参四五六七八九')],
    [(True, ('壱弐参四五六七八九', 'いろはにほへと'))],
    [  (True, ('壱', 'い')),
        (True, ('弐', 'ろ')),
        (True, ('参', 'は')),
        (False, '四'),
        (True, ('五', 'に')),
        (False, '六'),
        (True, ('七', 'ほ')),
        (True, ('八', 'へ')),
        (True, ('九', 'と'))],
    [  (True, ('壱', 'い')),
        (True, ('弐', 'ろは')),
        (False, '参'),
        (True, ('四', 'に')),
        (False, '五'),
        (True, ('六', 'ほ')),
        (True, ('七', 'へと')),
        (False, '八九')],
    [(True, ('壱', 'いろは')), (True, ('弐', 'にほへ')), (False, '参四五六七八九')],
    [(True, ('壱', 'いろはに')), (True, ('弐', 'ほへと')), (False, '参四五六七八九')],
    [(True, ('壱', 'いろはにほ')), (True, ('弐', 'へと')), (False, '参四五六七八九')],
    [  (False, '壱'), (False, '弐'), (False, '参'), (False, '四'), (False, '五'),
        (False, '六'), (False, '七'), (False, '八'), (False, '九')],
    [(False, '壱弐参四五六七八九')],
    [(True, ('壱', 'いろはにほへと')), (False, '弐参四五六七八九')],
    [(True, ('壱', 'いろはにほへと')), (False, '弐参四五六七八九')],
    [(True, ('壱', 'いろはにほ')), (True, ('弐', 'へと')), (False, '参四五六七八九')],
]

#オプションと文字データの文字数の多少
def test01_aslist():
    for t, e in zip(testcase01i, testcase01o):
        term = KanaText(t)
        rslt = term.aslist()
        assert rslt == e
