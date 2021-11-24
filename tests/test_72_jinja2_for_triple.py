#!/usr/bin/python3.8
import sys
import pytest
from pprint import pprint
from jinja2 import Template

from src import ExtIndexRack as IndexRack
from . import util

#-------------------------------------------------------------------

testcase01in = {
'doc02': [('triple','にに|四四^11; ほほ|五五^11; へへ|六六^11','id-1121','',None)],
'doc01': [('triple','いい|壱壱^11; ろろ|弐弐^11; はは|参参^11','id-1111','',None)],
}

testcase02in = testcase01in
testcase03in = testcase01in
testcase04in = testcase01in

testcase01str = "tests/jinja2/result72_01.txt"
testcase02str = "tests/jinja2/result72_02.txt"
testcase03str = "tests/jinja2/result72_03.txt"
testcase04str = "tests/jinja2/result72_04.txt"

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

def test01_jinja2_for_triple():
    bld = util.builder(testcase01in)
    bld.config.kana_text_indexer_mode = 'small'
    idx = IndexRack(bld)
    gidx = idx.create_index()
    text = template.render({'genindexentries': gidx})
    rslt = get_result(testcase01str)
    assert rslt == text

def test02_jinja2_for_triple():
    bld = util.builder(testcase02in)
    bld.config.kana_text_indexer_mode = 'small'
    bld.config.kana_text_change_triple = True
    idx = IndexRack(bld)
    gidx = idx.create_index()
    #self.assertEqual(testcase01out, gidx)
    text = template.render({'genindexentries': gidx})
    rslt = get_result(testcase02str)
    assert rslt == text

def test03_jinja2_for_triple():
    bld = util.builder(testcase03in)
    bld.config.kana_text_indexer_mode = 'large'
    idx = IndexRack(bld)
    gidx = idx.create_index()
    #self.assertEqual(testcase01out, gidx)
    text = template.render({'genindexentries': gidx})
    rslt = get_result(testcase03str)
    assert rslt == text

def test04_jinja2_for_triple():
    bld = util.builder(testcase04in)
    bld.config.kana_text_indexer_mode = 'large'
    bld.config.kana_text_change_triple = True
    idx = IndexRack(bld)
    gidx = idx.create_index()
    #self.assertEqual(testcase01out, gidx)
    text = template.render({'genindexentries': gidx})
    rslt = get_result(testcase04str)
    assert rslt == text
