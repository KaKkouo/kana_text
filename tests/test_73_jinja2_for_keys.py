#!/usr/bin/python3.8
import sys
import pytest
from pprint import pprint
from jinja2 import Template

from src import ExtIndexRack as IndexRack
from . import util

#-------------------------------------------------------------------

testcase01in = {
'doc01': [('keys','いい|壱壱^; ろろ|弐弐^; 逆引きのお題１','id-11','',None)],
'doc02': [('keys','はは|参参^; にに|四四^; 逆引きのお題２','id-21','',None)],
}

testcase02in = testcase01in

testcase01str = "tests/result73_01.txt"
testcase02str = "tests/result73_02.txt"

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

def test01_jinja2_for_keys():
    bld = util.builder(testcase01in)
    bld.config.kana_text_indexer_mode = 'small'
    bld.config.kana_text_on_genindex = True
    idx = IndexRack(bld)
    idx.entryclass.testmode = True
    gidx = idx.create_index()
    text = template.render({'genindexentries': gidx})
    rslt = get_result(testcase01str)
    assert rslt == text
    idx.entryclass.testmode = False

def test02_jinja2_for_keys():
    bld = util.builder(testcase02in)
    bld.config.kana_text_indexer_mode = 'large'
    bld.config.kana_text_on_genindex = True
    idx = IndexRack(bld)
    idx.entryclass.testmode = True
    gidx = idx.create_index()
    text = template.render({'genindexentries': gidx})
    rslt = get_result(testcase02str)
    assert rslt == text
    idx.entryclass.testmode = False

def test03_jinja2_for_keys():
    bld = util.builder(testcase01in)
    bld.config.kana_text_indexer_mode = 'small'
    bld.config.kana_text_on_genindex = True
    idx = IndexRack(bld)
    with pytest.raises(NotImplementedError):
        gidx = idx.create_index()
