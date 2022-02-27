#!/usr/bin/python3.8
import sys
import pytest

from src import ExtIndexRack as IndexRack
from . import util

#-------------------------------------------------------------------

testcase01in = { #テストパターン
    'doc1': [ ('single','いいい|壱壱壱^3','id-111','',None), ],
    'doc2': [ ('single','ろろろ|壱壱壱^21','id-121','',None), ],
    'doc3': [ ('single','ははは|壱壱壱^111','id-131','',None), ],
}

testcase01out = [
('い',
  [('いいい|壱壱壱', [[('', 'doc1.html#id-111')], [], None])]),
('は',
  [('ははは|壱壱壱', [[('', 'doc3.html#id-131')], [], None])]),
('ろ',
  [('ろろろ|壱壱壱', [[('', 'doc2.html#id-121')], [], None])]),
]


#-------------------------------------------------------------------


def test01_create_index():
    bld = util.builder(testcase01in)
    idx = IndexRack(bld)
    gidx = idx.create_index()
    assert gidx == testcase01out
