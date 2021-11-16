#!/usr/bin/python3.8
import sys
import pytest
from pprint import pprint

from src import ExtIndexRack as IndexRack
from . import util

#-------------------------------------------------------------------

#html_kana_text_on_genindex = True
testcase01in = {
'doc04': [('single','にに|四四^11; へへ|六六^11','id-04','',None)],
}

testcase01out = [
('な',
  [('にに|四四',
    [[], [('六六', [('', 'doc04.html#id-04')])], None])])]

#html_kana_text_on_genindex = True
testcase02in = {
'doc04': [('single','にに|四四^11; へへ|六六^11','id-04','',None)],
'doc03': [('single','にに|四四^11; ほほ|五五^11','id-03','', '分類子')],
}

testcase02out = [
('分類子',
  [('にに|四四',
    [[],
     [('六六', [('', 'doc04.html#id-04')]),
      ('五五', [('', 'doc03.html#id-03')])],
     None])])]

#html_kana_text_on_genindex = True
testcase03in = {
'doc04': [('single','にに|四四^11; へへ|六六^11','id-04','',None)],
'doc03': [('single','にに|四四^11; ほほ|五五^11','id-03','', '分類子')],
'doc02': [('single','いい|壱壱^11; はは|参参^11','id-02','',None)],
}

testcase03out = [
('あ',
  [('いい|壱壱',
    [[], [('参参', [('', 'doc02.html#id-02')])], None])]),
 ('分類子',
  [('にに|四四',
    [[],
     [('六六', [('', 'doc04.html#id-04')]),
      ('五五', [('', 'doc03.html#id-03')])],
     None])])]

#html_kana_text_on_genindex = True
testcase04in = {
'doc04': [('single','にに|四四^11; へへ|六六^11','id-04','',None)],
'doc03': [('single','にに|四四^11; ほほ|五五^11','id-03','', '分類子')],
'doc02': [('single','いい|壱壱^11; はは|参参^11','id-02','',None)],
'doc01': [('single','いい|壱壱^11; ろろ|弐弐^11','id-01','',None)],
}

testcase04out = [
('あ',
  [('いい|壱壱',
    [[],
     [('参参', [('', 'doc02.html#id-02')]),
      ('弐弐', [('', 'doc01.html#id-01')])],
     None])]),
 ('分類子',
  [('にに|四四',
    [[],
     [('六六', [('', 'doc04.html#id-04')]),
      ('五五', [('', 'doc03.html#id-03')])],
     None])])
]

#-------------------------------------------------------------------

def test01_structure_of_data():
    bld = util.builder(testcase01in)
    bld.config.kana_text_indexer_mode = 'small'
    bld.config.html_kana_text_on_genindex = True
    idx = IndexRack(bld)
    gidx = idx.create_index()
    assert gidx == testcase01out

def test02_structure_of_data():
    bld = util.builder(testcase02in)
    bld.config.kana_text_indexer_mode = 'small'
    bld.config.html_kana_text_on_genindex = True
    idx = IndexRack(bld)
    gidx = idx.create_index()
    assert gidx == testcase02out

def test03_structure_of_data():
    bld = util.builder(testcase03in)
    bld.config.kana_text_indexer_mode = 'small'
    bld.config.html_kana_text_on_genindex = True
    idx = IndexRack(bld)
    gidx = idx.create_index()
    assert gidx == testcase03out

def test04_structure_of_data():
    bld = util.builder(testcase04in)
    bld.config.kana_text_indexer_mode = 'small'
    bld.config.html_kana_text_on_genindex = True
    idx = IndexRack(bld)
    gidx = idx.create_index()
    assert gidx == testcase04out

#-------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
