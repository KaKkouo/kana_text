#!/usr/bin/python3.8
import sys
import unittest
from pprint import pprint
from jinja2 import Template

sys.path.append('sphinxcontrib')
from src import ExIndexRack as IndexRack
from . import util

#-------------------------------------------------------------------

testcase01in = {
'doc02': [('triple','にに|四四^11; ほほ|五五^11; へへ|六六^11','id-1121','',None)],
'doc01': [('triple','いい|壱壱^11; ろろ|弐弐^11; はは|参参^11','id-1111','',None)],
}

testcase02in = testcase01in
testcase03in = testcase01in
testcase04in = testcase01in

testcase01str = "tests/result82_01.txt"
testcase02str = "tests/result82_02.txt"
testcase03str = "tests/result82_03.txt"
testcase04str = "tests/result82_04.txt"

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

    def test01_triple_by_jinja2(self):
        self.maxDiff = None
        env = util.env(testcase01in)
        bld = util.builder(env)
        bld.config.kana_text_indexer_mode = 'small'
        idx = IndexRack(bld)
        gidx = idx.create_index()
        text = template.render({'genindexentries': gidx})
        rslt = get_result(testcase01str)
        self.assertEqual(rslt, text)

    def test02_triple_by_jinja2(self):
        self.maxDiff = None
        env = util.env(testcase02in)
        bld = util.builder(env)
        bld.config.kana_text_indexer_mode = 'small'
        bld.config.kana_text_change_triple = True
        idx = IndexRack(bld)
        gidx = idx.create_index()
        #self.assertEqual(testcase01out, gidx)
        text = template.render({'genindexentries': gidx})
        rslt = get_result(testcase02str)
        self.assertEqual(rslt, text)

    def test03_triple_by_jinja2(self):
        self.maxDiff = None
        env = util.env(testcase03in)
        bld = util.builder(env)
        bld.config.kana_text_indexer_mode = 'large'
        idx = IndexRack(bld)
        gidx = idx.create_index()
        #self.assertEqual(testcase01out, gidx)
        text = template.render({'genindexentries': gidx})
        rslt = get_result(testcase03str)
        self.assertEqual(rslt, text)

    def test04_triple_by_jinja2(self):
        self.maxDiff = None
        env = util.env(testcase04in)
        bld = util.builder(env)
        bld.config.kana_text_indexer_mode = 'large'
        bld.config.kana_text_change_triple = True
        idx = IndexRack(bld)
        gidx = idx.create_index()
        #self.assertEqual(testcase01out, gidx)
        text = template.render({'genindexentries': gidx})
        rslt = get_result(testcase04str)
        self.assertEqual(rslt, text)

#-------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
