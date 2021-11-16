#!/usr/bin/python3.8
import sys
import unittest
from pprint import pprint
from jinja2 import Template

sys.path.append('sphinxcontrib')
from src import ExtIndexRack as IndexRack
from . import util

#-------------------------------------------------------------------

#kana_text_on_genindex = True
testcase07in = {
'doc04': [('single','にに|四四^11; へへ|六六^11','id-04','',None)],
'doc03': [('single','にに|四四^11; ほほ|五五^11','id-03','', '分類子')],
'doc02': [('single','いい|壱壱^11; はは|参参^11','id-02','',None)],
'doc01': [('single','いい|壱壱^11; ろろ|弐弐^11','id-01','',None)],
}

#kana_text_on_genindex = True
testcase08in = {
'doc04': [('single','にに|四四^11; へへ|六六^11','id-04','',None)],
}

#kana_text_on_genindex = True
testcase09in = {
'doc04': [('single','にに|四四^11; へへ|六六^11','id-04','',None)],
'doc03': [('single','にに|四四^11; ほほ|五五^11','id-03','', '分類子')],
}

#kana_text_on_genindex = True
testcase10in = {
'doc04': [('single','にに|四四^11; へへ|六六^11','id-04','',None)],
'doc03': [('single','にに|四四^11','id-03','', '分類子')],
'doc02': [('single','いい|壱壱^11; はは|参参^11','id-02','',None)],
}

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

def test07_jinja2_without_reading():
    bld = util.builder(testcase07in)
    bld.config.kana_text_indexer_mode = 'small'
    idx = IndexRack(bld)
    gidx = idx.create_index()
    text = template.render({'genindexentries': gidx})
    rslt = get_result(testcase07str)
    assert rslt == text

def test08_jinja2_without_reading():
    bld = util.builder(testcase08in)
    bld.config.kana_text_indexer_mode = 'small'
    idx = IndexRack(bld)
    gidx = idx.create_index()
    text = template.render({'genindexentries': gidx})
    rslt = get_result(testcase08str)
    assert rslt == text

def test09_jinja2_without_reading():
    bld = util.builder(testcase09in)
    bld.config.kana_text_indexer_mode = 'small'
    idx = IndexRack(bld)
    gidx = idx.create_index()
    text = template.render({'genindexentries': gidx})
    rslt = get_result(testcase09str)
    assert rslt == text

def test10_jinja2_without_reading():
    bld = util.builder(testcase10in)
    bld.config.kana_text_indexer_mode = 'small'
    idx = IndexRack(bld)
    gidx = idx.create_index()
    text = template.render({'genindexentries': gidx})
    rslt = get_result(testcase10str)
    assert rslt == text
