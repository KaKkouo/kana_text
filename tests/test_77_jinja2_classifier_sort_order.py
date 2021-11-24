#!/usr/bin/python3.8
import sys
import unittest
from pprint import pprint
from jinja2 import Template

from src import ExtIndexRack as IndexRack
from . import util


def get_result(file_name):
    with open(file_name, 'r') as fd:
        result = fd.read()
    return result


def get_template(file_name):
    with open(file_name, 'r') as fd:
        tpl_text = fd.read()
    return Template(tpl_text)


template = get_template('tests/genindex.tpl')
testcase01str = "tests/jinja2/result77_01.txt"


def test01_classifier_sort_order():
    dataset = {
        'doc01': [('single', 'いい|壱壱', 'id-011', 'main', None)],  # 3
        'doc02': [('single', 'ろろ|弐弐', 'id-021', 'main', None)],  # 3
        'doc03': [('single', '参参参参_', 'id-031', 'main', None)],  # 5
        'doc04': [('single', '4四四四四', 'id-041', 'main', None)],  # 5
        'doc05': [('single', 'fifth五五', 'id-051', 'main', None)],  # 5
        'doc06': [('single', '&六六ロク', 'id-061', 'main', None)],  # 1
        'doc07': [('single', 'へへ|七七', 'id-071', 'main', '$|記号')],  # 1
        'doc08': [('single', 'とと|八八', 'id-081', 'main', '1|数字')],  # 2
        'doc09': [('single', 'ちち|九九', 'id-091', 'main', 'a|英字')],  # 2
        'doc10': [('single', 'ちち|拾拾', 'id-101', 'main', 'ぬ|かな')],  # 4
        'doc11': [('single', 'ちち|拾壱', 'id-101', 'main', '試|漢字')],  # 6
    }
    bld = util.builder(dataset)
    bld.config.kana_text_indexer_mode = 'small'
    idx = IndexRack(bld)
    gidx = idx.create_index()
    text = template.render({'genindexentries': gidx})
    rslt = get_result(testcase01str)
    assert rslt == text
