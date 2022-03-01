#!/usr/bin/python3.8
import sys
import pytest
from pprint import pprint

from src import ExtIndexRack as IndexRack
from . import util

#-------------------------------------------------------------------

# 読み情報がない

def test01_kana_catalog():
    return
    data = {
        'doc1': [('single','検証０１','id-01','',None)],
        'doc2': [('single','検証０１','id-02','main',None)],
    }
    bld = util.builder(data)
    bld.config.kana_text_indexer_mode = 'small'
    idx = IndexRack(bld)
    gidx = idx.create_index()
    assert gidx == [
        ('検', [('検証０１',
                 [[('main', 'doc2.html#id-02'),
                   ('', 'doc1.html#id-01')],
                  [], None])]),
    ]

# 読みが設定されていればその内容に従う

def test02_kana_catalog():
    data = {
        'doc1': [('single','いいいい|検証０２','id-01','',None)],
        'doc2': [('single','ろろろろ|検証０２','id-02','',None)],
        'doc3': [('single','はははは|検証０２','id-03','main',None)],
        'doc4': [('single','にににに|検証０２','id-04','main',None)],
    }
    bld = util.builder(data)
    bld.config.kana_text_indexer_mode = 'small'
    idx = IndexRack(bld)
    gidx = idx.create_index()
    assert gidx == [
        ('あ', [('いいいい|検証０２', [[('', 'doc1.html#id-01')], [], None])]),
        ('な', [('にににに|検証０２', [[('main', 'doc4.html#id-04')], [], None])]),
        ('は', [('はははは|検証０２', [[('main', 'doc3.html#id-03')], [], None])]),
        ('ら', [('ろろろろ|検証０２', [[('', 'doc2.html#id-02')], [], None])]),
    ]

# 辞書ファイルあり、読み情報なし

def test03_kana_catalog():
    data = {
        'doc1': [('single','球球球','id-01','',None)],
        'doc2': [('single','拾拾拾','id-02','main',None)],
    }
    bld = util.builder(data)
    bld.config.kana_text_indexer_mode = 'small'
    bld.config.kana_text_word_list = []
    bld.config.kana_text_word_file = 'tests/word_list.txt'
    idx = IndexRack(bld)
    gidx = idx.create_index()
    assert gidx == [
        ('な', [('ねねね|拾拾拾', [[('main', 'doc2.html#id-02')], [], None])]),
        ('ら', [('るるる|球球球', [[('', 'doc1.html#id-01')], [], None])]),
    ]

# 辞書ファイルあり、読み情報あり

def test04_kana_catalog():
    data = {
        'doc1': [('single','いいい|球球球','id-01','',None)],
        'doc2': [('single','ろろろ|拾拾拾','id-02','main',None)],
    }
    bld = util.builder(data)
    bld.config.kana_text_indexer_mode = 'small'
    bld.config.kana_text_word_list = []
    bld.config.kana_text_word_file = 'tests/word_list.txt'
    bld.config.html_kana_text_on_genindex = True
    idx = IndexRack(bld)
    gidx = idx.create_index()
    assert gidx == [
        ('あ', [('いいい|球球球', [[('', 'doc1.html#id-01')], [], None])]),
        ('ら', [('ろろろ|拾拾拾', [[('main', 'doc2.html#id-02')], [], None])]),
    ]

# 辞書ファイルあり、読み情報あり、優先順位/種別

def test05_kana_catalog():
    data = {
        'doc1': [('single','いい|球球球','id-01','',None)],
        'doc2': [('single','ろろ|拾拾拾','id-02','main',None)],
    }
    bld = util.builder(data)
    bld.config.kana_text_indexer_mode = 'small'
    bld.config.kana_text_word_list = []
    bld.config.kana_text_word_file = 'tests/word_list.txt'
    bld.config.html_kana_text_on_genindex = True
    idx = IndexRack(bld)
    gidx = idx.create_index()
    assert gidx == [
        ('あ', [('いい|球球球', [[('', 'doc1.html#id-01')], [], None])]),
        ('ら', [('ろろ|拾拾拾', [[('main', 'doc2.html#id-02')], [], None])]),
    ]

# 辞書ファイルあり、用語読み情報あり、索引読み情報あり

def test06_kana_catalog():
    data = {
        'doc1': [('single','いいい|球球球','id-01','',None)],
        'doc2': [('single','ろろろ|球球球','id-02','main',None)],
    }
    bld = util.builder(data)
    bld.config.kana_text_indexer_mode = 'small'
    bld.config.kana_text_word_list = []
    bld.config.kana_text_word_file = 'tests/word_list.txt'
    bld.config.html_kana_text_on_genindex = True
    idx = IndexRack(bld)
    gidx = idx.create_index()
    assert gidx == [
        ('あ', [('いいい|球球球', [[('', 'doc1.html#id-01')], [], None])]),
        ('ら', [('ろろろ|球球球', [[('main', 'doc2.html#id-02')], [], None])]),
    ]

# 辞書ファイルあり、用語読み情報あり、索引読み情報なし

def test07_kana_catalog():
    data = {
        'doc1': [('single','球球球','id-01','',None)],
        'doc2': [('single','ろろろ|球球球','id-02','main',None)],
    }
    bld = util.builder(data)
    bld.config.kana_text_indexer_mode = 'small'
    bld.config.kana_text_word_list = []
    bld.config.kana_text_word_file = 'tests/word_list.txt'
    bld.config.html_kana_text_on_genindex = True
    idx = IndexRack(bld)
    gidx = idx.create_index()
    assert gidx == [
        ('ら', [('ろろろ|球球球',
                [[('main', 'doc2.html#id-02'), ('', 'doc1.html#id-01')], [], None])]),
    ]

# 辞書ファイルあり、用語読み情報あり、索引読み情報なし、優先順

def test08_kana_catalog():
    data = {
        'doc1': [('single','球球球','id-01','',None)],
        'doc2': [('single','ろろ|球球球','id-02','main',None)],
        'doc3': [('single','ははは|球球球','id-03','main',None)],
    }
    bld = util.builder(data)
    bld.config.kana_text_indexer_mode = 'small'
    bld.config.kana_text_word_list = []
    bld.config.kana_text_word_file = 'tests/word_list.txt'
    bld.config.html_kana_text_on_genindex = True
    idx = IndexRack(bld)
    gidx = idx.create_index()
    assert gidx == [
        ('は', [('ははは|球球球',
                [[('main', 'doc3.html#id-03'), ('', 'doc1.html#id-01')], [], None])]),
        ('ら', [('ろろ|球球球',
                [[('main', 'doc2.html#id-02')], [], None])]),
    ]

# 辞書ファイルあり、用語読み情報あり、索引読み情報なし、優先順

def test09_kana_catalog():
    data = {
        'doc1': [('single','球球球','id-01','',None)],
        'doc2': [('single','ろろろ|球球球','id-02','main',None)],
        'doc3': [('single','はは|球球球','id-03','main',None)],
    }
    bld = util.builder(data)
    bld.config.kana_text_indexer_mode = 'small'
    bld.config.kana_text_word_list = []
    bld.config.kana_text_word_file = 'tests/word_list.txt'
    bld.config.html_kana_text_on_genindex = True
    idx = IndexRack(bld)
    gidx = idx.create_index()
    assert gidx == [
        ('は', [('はは|球球球',
                [[('main', 'doc3.html#id-03')], [], None])]),
        ('ら', [('ろろろ|球球球',
                [[('main', 'doc2.html#id-02'), ('', 'doc1.html#id-01')], [], None])]),
    ]

# 辞書ファイルあり、用語読み情報あり、索引読み情報なし、優先順

def test10_kana_catalog():
    data = {
        'doc1': [('single','球球球','id-01','',None)],
        'doc2': [('single','ろろろ|球球球','id-02','main',None)],
        'doc3': [('single','ははは|球球球','id-03','main',None)],
    }
    bld = util.builder(data)
    bld.config.kana_text_indexer_mode = 'small'
    bld.config.kana_text_word_list = []
    bld.config.kana_text_word_file = 'tests/word_list.txt'
    bld.config.html_kana_text_on_genindex = True
    idx = IndexRack(bld)
    gidx = idx.create_index()
    assert gidx == [
        ('は', [('ははは|球球球',
                [[('main', 'doc3.html#id-03')], [], None])]),
        ('ら', [('ろろろ|球球球',
                [[('main', 'doc2.html#id-02'), ('', 'doc1.html#id-01')], [], None])]),
    ]

# 辞書ファイルあり、用語読み情報あり、索引読み情報なし、優先順

def test11_kana_catalog():
    data = {
        'doc1': [('single','球球球','id-01','',None)],
        'doc2': [('single','ろろろ|球球球^3','id-02','main',None)],
        'doc3': [('single','ははは|球球球^12','id-03','main',None)],
    }
    bld = util.builder(data)
    bld.config.kana_text_indexer_mode = 'small'
    bld.config.kana_text_word_list = []
    bld.config.kana_text_word_file = 'tests/word_list.txt'
    bld.config.html_kana_text_on_genindex = True
    idx = IndexRack(bld)
    gidx = idx.create_index()
    assert gidx == [
        ('は', [('ははは|球球球',
                [[('main', 'doc3.html#id-03'), ('', 'doc1.html#id-01')], [], None])]),
        ('ら', [('ろろろ|球球球',
                [[('main', 'doc2.html#id-02')], [], None])]),
    ]

# 辞書ファイルあり、用語読み情報あり、索引読み情報なし、設定ファイルあり

def test99_kana_catalog():
    data = {
        'doc1': [('single','球球球','id-01','',None)],
        'doc2': [('single','ろろろ|球球球','id-02','main',None)],
    }
    bld = util.builder(data)
    bld.config.kana_text_indexer_mode = 'small'
    bld.config.kana_text_word_list = ['ののの|球球球^', ]
    bld.config.kana_text_word_file = 'tests/word_list.txt'
    bld.config.html_kana_text_on_genindex = True
    idx = IndexRack(bld)
    gidx = idx.create_index()
    assert gidx == [
        ('な', [('ののの|球球球',
                [[('', 'doc1.html#id-01')], [], None])]),
        ('ら', [('ろろろ|球球球',
                [[('main', 'doc2.html#id-02')], [], None])]),
    ]
