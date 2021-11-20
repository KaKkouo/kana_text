#!/usr/bin/python3.8
import sys
import unittest
from pprint import pprint
from jinja2 import Template

from src import ExtIndexRack as IndexRack
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

testcase01str = "tests/result71_01.txt"
testcase02str = "tests/result71_02.txt"
testcase03str = "tests/result71_03.txt"
testcase04str = "tests/result71_04.txt"

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

def test01_jinja2_for_single():
    bld = util.builder(testcase01in)
    bld.config.kana_text_indexer_mode = 'small'
    bld.config.kana_text_on_genindex = True
    idx = IndexRack(bld)
    gidx = idx.create_index()
    text = template.render({'genindexentries': gidx})
    rslt = get_result(testcase01str)
    assert rslt == text

def test02_jinja2_for_single():
    bld = util.builder(testcase02in)
    bld.config.kana_text_indexer_mode = 'small'
    bld.config.kana_text_on_genindex = True
    idx = IndexRack(bld)
    gidx = idx.create_index()
    #self.assertEqual(testcase01out, gidx)
    text = template.render({'genindexentries': gidx})
    rslt = get_result(testcase02str)
    assert rslt == text

def test03_jinja2_for_single():
    bld = util.builder(testcase03in)
    bld.config.kana_text_indexer_mode = 'small'
    bld.config.kana_text_on_genindex = True
    idx = IndexRack(bld)
    gidx = idx.create_index()
    #self.assertEqual(testcase01out, gidx)
    text = template.render({'genindexentries': gidx})
    rslt = get_result(testcase03str)
    assert rslt == text

def test04_jinja2_for_single():
    bld = util.builder(testcase04in)
    bld.config.kana_text_indexer_mode = 'small'
    bld.config.kana_text_on_genindex = True
    idx = IndexRack(bld)
    gidx = idx.create_index()
    #self.assertEqual(testcase01out, gidx)
    text = template.render({'genindexentries': gidx})
    rslt = get_result(testcase04str)
    assert rslt == text
