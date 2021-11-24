#!/usr/bin/python3.8
import sys
import unittest
from pprint import pprint
from jinja2 import Template

sys.path.append('sphinxcontrib')
from src import ExtIndexRack as IndexRack
from . import util

#-------------------------------------------------------------------

#kana_text_word_listの上書き
testcase01in = {
'doc01': [('single','ああ|球球球; いい|球球球','id-01','',None)],
'doc02': [('see','かか|球球球; めめ|球球球','id-02','',None)],
'doc03': [('single','ささ|球球球; んん|球球球','id-03','',None)],
'doc04': [('seealso','たた|拾拾拾; いい|拾拾拾','id-04','',None)],
'doc05': [('single','なな|拾拾拾; めめ|拾拾拾','id-05','',None)],
'doc06': [('single','おお|拾拾拾; んん|拾拾拾','id-06','',None)],
}

#kana_text_word_listの上書き
testcase02in = {
'doc01': [('single','ああ|球球球; いい|球球球','id-01','',None)],
'doc02': [('see','かか|球球球; めめ|球球球','id-02','',None)],
'doc03': [('single','ささ|球球球; んん|球球球','id-03','',None)],
'doc04': [('seealso','たた|拾拾拾; いい|拾拾拾','id-04','',None)],
'doc05': [('single','なな|拾拾拾','id-05','',None)],
'doc06': [('single','おお|拾拾拾','id-06','',None)],
}

testcase01str = "tests/jinja2/result75_01.txt"
testcase02str = "tests/jinja2/result75_02.txt"

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

def test01_jinja2_for_see_seealso():
    bld = util.builder(testcase01in)
    bld.config.kana_text_indexer_mode = 'small'
    bld.config.kana_text_on_genindex = True
    idx = IndexRack(bld)
    gidx = idx.create_index()
    #self.assertEqual(testcase01out, gidx)
    text = template.render({'genindexentries': gidx})
    rslt = get_result(testcase01str)
    assert rslt == text

def test02_jinja2_for_see_seealso():
    bld = util.builder(testcase02in)
    bld.config.kana_text_indexer_mode = 'small'
    bld.config.kana_text_on_genindex = True
    idx = IndexRack(bld)
    gidx = idx.create_index()
    #self.assertEqual(testcase01out, gidx)
    text = template.render({'genindexentries': gidx})
    rslt = get_result(testcase02str)
    assert rslt == text
