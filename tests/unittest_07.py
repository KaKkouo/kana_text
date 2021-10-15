#!/usr/bin/python3.8
import sys
import unittest
from pprint import pprint
sys.path.append('sphinxcontrib')
from src import IndexRack

#-------------------------------------------------------------------

#html_kana_text_on_genindex = True
testcase01in = {
'doc04': [('single','にに|四四^11; へへ|六六^11','id-04','',None)],
'doc03': [('single','にに|四四^11; ほほ|五五^11','id-03','', '分類子')],
'doc02': [('single','いい|壱壱^11; はは|参参^11','id-02','',None)],
'doc01': [('single','いい|壱壱^11; ろろ|弐弐^11','id-01','',None)],
}

testcase01out = [
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

#html_kana_text_on_genindex = True
testcase02in = {
'doc04': [('single','にに|四四^11; へへ|六六^11','id-04','',None)],
}

testcase02out = [
('な',
  [('にに|四四',
    [[], [('へへ|六六', [('', 'doc04.html#id-04')])], None])])]

#html_kana_text_on_genindex = True
testcase03in = {
'doc04': [('single','にに|四四^11; へへ|六六^11','id-04','',None)],
'doc03': [('single','にに|四四^11; ほほ|五五^11','id-03','', '分類子')],
}

testcase03out = [
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
}

testcase04out = [
('あ',
  [('いい|壱壱',
    [[], [('はは|参参', [('', 'doc02.html#id-02')])], None])]),
 ('分類子',
  [('にに|四四',
    [[],
     [('へへ|六六', [('', 'doc04.html#id-04')]),
      ('ほほ|五五', [('', 'doc03.html#id-03')])],
     None])])]

#-------------------------------------------------------------------

class _env(object): pass

class _config(object):
    def __init__(self):
        self.kana_text_separator = r'\|'
        self.kana_text_indexer_mode = 'normal'
        self.kana_text_word_file = '~/sphinx/word_list.txt'
        self.kana_text_word_list = ()
        self.html_kana_text_on_genindex = False
        self.html_change_triple = False

class _builder(object):
    def __init__(self, env, cfg):
        self.env = env
        self.config = cfg

    def get_relative_uri(self, _, fn):
        return fn+'.html'

env = _env()

class testIndexRack(unittest.TestCase):
    def test01_structure_of_data(self):
        self.maxDiff = None
        cfg = _config()
        cfg.kana_text_indexer_mode = 'small'
        cfg.html_kana_text_on_genindex = True
        bld = _builder(env, cfg)
        idx = IndexRack(bld, True)
        gidx = idx.create_genindex(testcase01in)
        self.assertEqual(gidx, testcase01out)

    def test02_structure_of_data(self):
        self.maxDiff = None
        cfg = _config()
        cfg.kana_text_indexer_mode = 'small'
        cfg.html_kana_text_on_genindex = True
        bld = _builder(env, cfg)
        idx = IndexRack(bld, True)
        gidx = idx.create_genindex(testcase02in)
        self.assertEqual(gidx, testcase02out)

    def test03_structure_of_data(self):
        self.maxDiff = None
        cfg = _config()
        cfg.kana_text_indexer_mode = 'small'
        cfg.html_kana_text_on_genindex = True
        bld = _builder(env, cfg)
        idx = IndexRack(bld, True)
        gidx = idx.create_genindex(testcase03in)
        self.assertEqual(gidx, testcase03out)

    def test04_structure_of_data(self):
        self.maxDiff = None
        cfg = _config()
        cfg.kana_text_indexer_mode = 'small'
        cfg.html_kana_text_on_genindex = True
        bld = _builder(env, cfg)
        idx = IndexRack(bld, True)
        gidx = idx.create_genindex(testcase04in)
        self.assertEqual(gidx, testcase04out)

#-------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()

    #bld.config.kana_text_indexer_mode = 'small'
    #gidx = bld.create_genindex(testcase08in)
    #pprint(gidx)
