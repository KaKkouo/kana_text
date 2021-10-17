#!/usr/bin/python3.8
import sys
import unittest
from pprint import pprint
from jinja2 import Template

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

testcase02out = []

#html_kana_text_on_genindex = True
testcase03in = {
'doc04': [('single','にに|四四^11; へへ|六六^11','id-04','',None)],
'doc03': [('single','にに|四四^11; ほほ|五五^11','id-03','', '分類子')],
}

testcase03out = []

#html_kana_text_on_genindex = True
testcase04in = {
'doc04': [('single','にに|四四^11; へへ|六六^11','id-04','',None)],
'doc03': [('single','にに|四四^11','id-03','', '分類子')],
'doc02': [('single','いい|壱壱^11; はは|参参^11','id-02','',None)],
}

testcase04out = []

#kana_text_word_listの上書き
testcase05in = {
'doc01': [('single','ああ|球球球; いい|球球球','id-01','',None)],
'doc02': [('see','かか|球球球; めめ|球球球','id-02','',None)],
'doc03': [('single','ささ|球球球; んん|球球球','id-03','',None)],
'doc04': [('seealso','たた|拾拾拾; いい|拾拾拾','id-04','',None)],
'doc05': [('single','なな|拾拾拾; めめ|拾拾拾','id-05','',None)],
'doc06': [('single','おお|拾拾拾; んん|拾拾拾','id-06','',None)],
}

testcase05out = []

#kana_text_word_listの上書き
testcase06in = {
'doc01': [('single','ああ|球球球; いい|球球球','id-01','',None)],
'doc02': [('see','かか|球球球; めめ|球球球','id-02','',None)],
'doc03': [('single','ささ|球球球; んん|球球球','id-03','',None)],
'doc04': [('seealso','たた|拾拾拾; いい|拾拾拾','id-04','',None)],
'doc05': [('single','なな|拾拾拾','id-05','',None)],
'doc06': [('single','おお|拾拾拾','id-06','',None)],
}

testcase06out = []

testcase01str = "tests/result_08_01.txt"
testcase02str = "tests/result_08_02.txt"
testcase03str = "tests/result_08_03.txt"
testcase04str = "tests/result_08_04.txt"
testcase05str = "tests/result_08_05.txt"
testcase06str = "tests/result_08_06.txt"

#-------------------------------------------------------------------

class _env(object): pass

class _config(object):
    def __init__(self):
        self.kana_text_separator = r'\|'
        self.kana_text_indexer_mode = 'normal'
        self.kana_text_word_file = ''
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

def get_result(file_name):
    with open(file_name, 'r') as fd:
        result = fd.read()
    return result

def get_template(file_name):
    with open(file_name, 'r') as fd:
        tpl_text = fd.read()
    return Template(tpl_text)

template = get_template('tests/genindex.tpl')

class testIndexRack(unittest.TestCase):

    def test01_text_by_jinja2(self):
        self.maxDiff = None
        cfg = _config()
        cfg.kana_text_indexer_mode = 'small'
        cfg.html_kana_text_on_genindex = True
        bld = _builder(env, cfg)
        idx = IndexRack(bld)
        gidx = idx.create_genindex(testcase01in)
        #self.assertEqual(testcase01out, gidx)
        text = template.render({'genindexentries': gidx})
        rslt = get_result(testcase01str)
        self.assertEqual(rslt, text)

    def test02_text_by_jinja2(self):
        self.maxDiff = None
        cfg = _config()
        cfg.kana_text_indexer_mode = 'small'
        cfg.html_kana_text_on_genindex = True
        bld = _builder(env, cfg)
        idx = IndexRack(bld)
        gidx = idx.create_genindex(testcase02in)
        #self.assertEqual(testcase01out, gidx)
        text = template.render({'genindexentries': gidx})
        rslt = get_result(testcase02str)
        self.assertEqual(rslt, text)

    def test03_text_by_jinja2(self):
        self.maxDiff = None
        cfg = _config()
        cfg.kana_text_indexer_mode = 'small'
        cfg.html_kana_text_on_genindex = True
        bld = _builder(env, cfg)
        idx = IndexRack(bld, True)
        gidx = idx.create_genindex(testcase03in)
        #self.assertEqual(testcase01out, gidx)
        text = template.render({'genindexentries': gidx})
        rslt = get_result(testcase03str)
        self.assertEqual(rslt, text)

    def test04_text_by_jinja2(self):
        self.maxDiff = None
        cfg = _config()
        cfg.kana_text_indexer_mode = 'small'
        cfg.html_kana_text_on_genindex = True
        bld = _builder(env, cfg)
        idx = IndexRack(bld, True)
        gidx = idx.create_genindex(testcase04in)
        #self.assertEqual(testcase01out, gidx)
        text = template.render({'genindexentries': gidx})
        rslt = get_result(testcase04str)
        self.assertEqual(rslt, text)

    def test05_text_by_jinja2(self):
        self.maxDiff = None
        cfg = _config()
        cfg.kana_text_indexer_mode = 'small'
        cfg.html_kana_text_on_genindex = True
        bld = _builder(env, cfg)
        idx = IndexRack(bld, True)
        gidx = idx.create_genindex(testcase05in)
        #self.assertEqual(testcase01out, gidx)
        text = template.render({'genindexentries': gidx})
        rslt = get_result(testcase05str)
        self.assertEqual(rslt, text)

    def test06_text_by_jinja2(self):
        self.maxDiff = None
        cfg = _config()
        cfg.kana_text_indexer_mode = 'small'
        cfg.html_kana_text_on_genindex = True
        bld = _builder(env, cfg)
        idx = IndexRack(bld)
        gidx = idx.create_genindex(testcase06in)
        #self.assertEqual(testcase01out, gidx)
        text = template.render({'genindexentries': gidx})
        rslt = get_result(testcase06str)
        self.assertEqual(rslt, text)

#-------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()

    #bld.config.kana_text_indexer_mode = 'small'
    #gidx = bld.create_genindex(testcase08in)
    #pprint(gidx)
