#!/usr/bin/python3.8
import sys
import unittest
from pprint import pprint
sys.path.append('sphinxcontrib')
from src import IndexRack
from . import util

#-------------------------------------------------------------------

#html_kana_text_on_genindex = True
testcase01in = {
'doc04': [('single','にに|四四^11; へへ|六六^11','id-04','',None)],
}

testcase01out = [
('な',
  [('にに|四四',
    [[], [('へへ|六六', [('', 'doc04.html#id-04')])], None])])]

#html_kana_text_on_genindex = True
testcase02in = {
'doc04': [('single','にに|四四^11; へへ|六六^11','id-04','',None)],
'doc03': [('single','にに|四四^11; ほほ|五五^11','id-03','', '分類子')],
}

testcase02out = [
('分類子',
  [('にに|四四',
    [[],
     [('へへ|六六', [('', 'doc04.html#id-04')]),
      ('ほほ|五五', [('', 'doc03.html#id-03')])],
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
    [[], [('はは|参参', [('', 'doc02.html#id-02')])], None])]),
 ('分類子',
  [('にに|四四',
    [[],
     [('へへ|六六', [('', 'doc04.html#id-04')]),
      ('ほほ|五五', [('', 'doc03.html#id-03')])],
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
     [('はは|参参', [('', 'doc02.html#id-02')]),
      ('ろろ|弐弐', [('', 'doc01.html#id-01')])],
     None])]),
 ('分類子',
  [('にに|四四',
    [[],
     [('へへ|六六', [('', 'doc04.html#id-04')]),
      ('ほほ|五五', [('', 'doc03.html#id-03')])],
     None])])
]

#-------------------------------------------------------------------

class testIndexRack(unittest.TestCase):
    def test01_structure_of_data(self):
        self.maxDiff = None
        env = util.env(testcase01in)
        bld = util.builder(env)
        bld.config.kana_text_indexer_mode = 'small'
        bld.config.html_kana_text_on_genindex = True
        idx = IndexRack(bld)
        gidx = idx.create_genindex()
        self.assertEqual(gidx, testcase01out)

    def test02_structure_of_data(self):
        self.maxDiff = None
        env = util.env(testcase02in)
        bld = util.builder(env)
        bld.config.kana_text_indexer_mode = 'small'
        bld.config.html_kana_text_on_genindex = True
        idx = IndexRack(bld)
        gidx = idx.create_genindex()
        self.assertEqual(gidx, testcase02out)

    def test03_structure_of_data(self):
        self.maxDiff = None
        env = util.env(testcase03in)
        bld = util.builder(env)
        bld.config.kana_text_indexer_mode = 'small'
        bld.config.html_kana_text_on_genindex = True
        idx = IndexRack(bld)
        gidx = idx.create_genindex()
        self.assertEqual(gidx, testcase03out)

    def test04_structure_of_data(self):
        self.maxDiff = None
        env = util.env(testcase04in)
        bld = util.builder(env)
        bld.config.kana_text_indexer_mode = 'small'
        bld.config.html_kana_text_on_genindex = True
        idx = IndexRack(bld)
        gidx = idx.create_genindex()
        self.assertEqual(gidx, testcase04out)

#-------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()

    #bld.config.kana_text_indexer_mode = 'small'
    #gidx = bld.create_genindex(testcase08in)
    #pprint(gidx)
