#!/usr/bin/python3.8
import sys
import unittest
from pprint import pprint
from jinja2 import Template

sys.path.append('sphinxcontrib')
from src import ExIndexRack as IndexRack
from . import util

#-------------------------------------------------------------------

#kana_text_on_genindex = True
testcase01in = {
'doc04': [('single','にに|四四^11; へへ|六六^11','id-04','',None)],
'doc03': [('single','にに|四四^11; ほほ|五五^11','id-03','', '分類子')],
'doc02': [('single','いい|壱壱^11; はは|参参^11','id-02','',None)],
'doc01': [('single','いい|壱壱^11; ろろ|弐弐^11','id-01','',None)],
}

#kana_text_on_genindex = True
testcase02in = {
'doc04': [('single','にに|四四^11; へへ|六六^11','id-04','',None)],
}

#kana_text_on_genindex = True
testcase03in = {
'doc04': [('single','にに|四四^11; へへ|六六^11','id-04','',None)],
'doc03': [('single','にに|四四^11; ほほ|五五^11','id-03','', '分類子')],
}

#kana_text_on_genindex = True
testcase04in = {
'doc04': [('single','にに|四四^11; へへ|六六^11','id-04','',None)],
'doc03': [('single','にに|四四^11','id-03','', '分類子')],
'doc02': [('single','いい|壱壱^11; はは|参参^11','id-02','',None)],
}

#kana_text_word_listの上書き
testcase05in = {
'doc01': [('single','ああ|球球球; いい|球球球','id-01','',None)],
'doc02': [('see','かか|球球球; めめ|球球球','id-02','',None)],
'doc03': [('single','ささ|球球球; んん|球球球','id-03','',None)],
'doc04': [('seealso','たた|拾拾拾; いい|拾拾拾','id-04','',None)],
'doc05': [('single','なな|拾拾拾; めめ|拾拾拾','id-05','',None)],
'doc06': [('single','おお|拾拾拾; んん|拾拾拾','id-06','',None)],
}

#kana_text_word_listの上書き
testcase06in = {
'doc01': [('single','ああ|球球球; いい|球球球','id-01','',None)],
'doc02': [('see','かか|球球球; めめ|球球球','id-02','',None)],
'doc03': [('single','ささ|球球球; んん|球球球','id-03','',None)],
'doc04': [('seealso','たた|拾拾拾; いい|拾拾拾','id-04','',None)],
'doc05': [('single','なな|拾拾拾','id-05','',None)],
'doc06': [('single','おお|拾拾拾','id-06','',None)],
}

testcase01str = "tests/result81_01.txt"
testcase02str = "tests/result81_02.txt"
testcase03str = "tests/result81_03.txt"
testcase04str = "tests/result81_04.txt"
testcase05str = "tests/result81_05.txt"
testcase06str = "tests/result81_06.txt"

testcase07in = testcase01in
testcase08in = testcase02in
testcase09in = testcase03in
testcase10in = testcase04in

testcase07str = "tests/result81_07.txt"
testcase08str = "tests/result81_08.txt"
testcase09str = "tests/result81_09.txt"
testcase10str = "tests/result81_10.txt"

#-------------------------------------------------------------------

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
        env = util.env(testcase01in)
        bld = util.builder(env)
        bld.config.kana_text_indexer_mode = 'small'
        bld.config.kana_text_on_genindex = True
        idx = IndexRack(bld)
        gidx = idx.create_index()
        text = template.render({'genindexentries': gidx})
        rslt = get_result(testcase01str)
        self.assertEqual(rslt, text)

    def test02_text_by_jinja2(self):
        self.maxDiff = None
        env = util.env(testcase02in)
        bld = util.builder(env)
        bld.config.kana_text_indexer_mode = 'small'
        bld.config.kana_text_on_genindex = True
        idx = IndexRack(bld)
        gidx = idx.create_index()
        #self.assertEqual(testcase01out, gidx)
        text = template.render({'genindexentries': gidx})
        rslt = get_result(testcase02str)
        self.assertEqual(rslt, text)

    def test03_text_by_jinja2(self):
        self.maxDiff = None
        env = util.env(testcase03in)
        bld = util.builder(env)
        bld.config.kana_text_indexer_mode = 'small'
        bld.config.kana_text_on_genindex = True
        idx = IndexRack(bld)
        gidx = idx.create_index()
        #self.assertEqual(testcase01out, gidx)
        text = template.render({'genindexentries': gidx})
        rslt = get_result(testcase03str)
        self.assertEqual(rslt, text)

    def test04_text_by_jinja2(self):
        self.maxDiff = None
        env = util.env(testcase04in)
        bld = util.builder(env)
        bld.config.kana_text_indexer_mode = 'small'
        bld.config.kana_text_on_genindex = True
        idx = IndexRack(bld)
        gidx = idx.create_index()
        #self.assertEqual(testcase01out, gidx)
        text = template.render({'genindexentries': gidx})
        rslt = get_result(testcase04str)
        self.assertEqual(rslt, text)

    def test05_text_by_jinja2(self):
        self.maxDiff = None
        env = util.env(testcase05in)
        bld = util.builder(env)
        bld.config.kana_text_indexer_mode = 'small'
        bld.config.kana_text_on_genindex = True
        idx = IndexRack(bld)
        gidx = idx.create_index()
        #self.assertEqual(testcase01out, gidx)
        text = template.render({'genindexentries': gidx})
        rslt = get_result(testcase05str)
        self.assertEqual(rslt, text)

    def test06_text_by_jinja2(self):
        self.maxDiff = None
        env = util.env(testcase06in)
        bld = util.builder(env)
        bld.config.kana_text_indexer_mode = 'small'
        bld.config.kana_text_on_genindex = True
        idx = IndexRack(bld)
        gidx = idx.create_index()
        #self.assertEqual(testcase01out, gidx)
        text = template.render({'genindexentries': gidx})
        rslt = get_result(testcase06str)
        self.assertEqual(rslt, text)

    def test07_text_by_jinja2(self):
        self.maxDiff = None
        env = util.env(testcase07in)
        bld = util.builder(env)
        bld.config.kana_text_indexer_mode = 'small'
        idx = IndexRack(bld)
        gidx = idx.create_index()
        text = template.render({'genindexentries': gidx})
        rslt = get_result(testcase07str)
        self.assertEqual(rslt, text)

    def test08_text_by_jinja2(self):
        self.maxDiff = None
        env = util.env(testcase08in)
        bld = util.builder(env)
        bld.config.kana_text_indexer_mode = 'small'
        idx = IndexRack(bld)
        gidx = idx.create_index()
        text = template.render({'genindexentries': gidx})
        rslt = get_result(testcase08str)
        self.assertEqual(rslt, text)

    def test09_text_by_jinja2(self):
        self.maxDiff = None
        env = util.env(testcase09in)
        bld = util.builder(env)
        bld.config.kana_text_indexer_mode = 'small'
        idx = IndexRack(bld)
        gidx = idx.create_index()
        text = template.render({'genindexentries': gidx})
        rslt = get_result(testcase09str)
        self.assertEqual(rslt, text)

    def test10_text_by_jinja2(self):
        self.maxDiff = None
        env = util.env(testcase10in)
        bld = util.builder(env)
        bld.config.kana_text_indexer_mode = 'small'
        idx = IndexRack(bld)
        gidx = idx.create_index()
        text = template.render({'genindexentries': gidx})
        rslt = get_result(testcase10str)
        self.assertEqual(rslt, text)

#-------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
