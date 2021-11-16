#!/usr/bin/python3.8
import sys
import pytest

from src import ExtIndexRack as IndexRack
from . import util

#-------------------------------------------------------------------

#ひらがなにまとめる
testcase04in = { #テストパターン
    'doc1': [
        ('single','ナナナ|太郎','id-311','',None),
        ('single','ニニニ|はな子; フフフ|森の熊','id-343','main',None),
        ('pair','ヌヌヌ|手紙; ハハハ|狸と狐','id-321','',None),
        ('triple','ネネネ|犬猫; ハハハ|子鹿; さささ|急須','id-331','',None),
    ],
    'doc3': [
        ('single','かかか|東京; くくく|戦斧','id-148','main',None),
        ('single','ききき|満月; くくく|騎士','id-143','',None),
        ('pair','くくく|月光; くくく|伯爵','id-123','',None),
        ('triple','けけけ|花見; かかか|男爵; さささ|機関室','id-131','',None),
    ],
}

testcase04out = [
  ('か',
   [('かかか|東京', [[], [('戦斧', [('main', 'doc3.html#id-148')])], None]),
    ('かかか|男爵', [[], [('機関室, 花見', [('', 'doc3.html#id-131')])], None])]),
  ('き', [('ききき|満月', [[], [('騎士', [('', 'doc3.html#id-143')])], None])]),
  ('く',
   [('くくく|伯爵', [[], [('月光', [('', 'doc3.html#id-123')])], None]),
    ('くくく|月光', [[], [('伯爵', [('', 'doc3.html#id-123')])], None])]),
  ('け',
   [('けけけ|花見', [[], [('男爵 機関室', [('', 'doc3.html#id-131')])], None])]),
  ('さ',
   [('さささ|急須', [[], [('犬猫 子鹿', [('', 'doc1.html#id-331')])], None]),
    ('さささ|機関室', [[], [('花見 男爵', [('', 'doc3.html#id-131')])], None])]),
  ('な', [('ナナナ|太郎', [[('', 'doc1.html#id-311')], [], None])]),
  ('に',
   [('ニニニ|はな子', [[], [('森の熊', [('main', 'doc1.html#id-343')])], None])]),
  ('ぬ', [('ヌヌヌ|手紙', [[], [('狸と狐', [('', 'doc1.html#id-321')])], None])]),
  ('ね',
   [('ネネネ|犬猫', [[], [('子鹿 急須', [('', 'doc1.html#id-331')])], None])]),
  ('は',
   [('ハハハ|子鹿', [[], [('急須, 犬猫', [('', 'doc1.html#id-331')])], None]),
    ('ハハハ|狸と狐', [[], [('手紙', [('', 'doc1.html#id-321')])], None])])
]

#あかさたな…にまとめる
testcase05in = { #テストパターン
    'doc1': [
        ('single','ナナナ|太郎','id-311','',None),
        ('single','ニニニ|はな子; フフフ|森の熊','id-343','main',None),
        ('pair','ヌヌヌ|手紙; ハハハ|狸と狐','id-321','',None),
        ('triple','ネネネ|犬猫; ハハハ|子鹿; さささ|急須','id-331','',None),
    ],
    'doc3': [
        ('single','かかか|東京; くくく|戦斧','id-148','main',None),
        ('single','ききき|満月; くくく|騎士','id-143','',None),
        ('pair','くくく|月光; くくく|伯爵','id-123','',None),
        ('triple','けけけ|花見; かかか|男爵; さささ|機関室','id-131','',None),
    ],
}

testcase05out = [
  ('か',
   [('かかか|東京', [[], [('戦斧', [('main', 'doc3.html#id-148')])], None]),
    ('かかか|男爵', [[], [('機関室, 花見', [('', 'doc3.html#id-131')])], None]),
    ('ききき|満月', [[], [('騎士', [('', 'doc3.html#id-143')])], None]),
    ('くくく|伯爵', [[], [('月光', [('', 'doc3.html#id-123')])], None]),
    ('くくく|月光', [[], [('伯爵', [('', 'doc3.html#id-123')])], None]),
    ('けけけ|花見', [[], [('男爵 機関室', [('', 'doc3.html#id-131')])], None])]),
  ('さ',
   [('さささ|急須', [[], [('犬猫 子鹿', [('', 'doc1.html#id-331')])], None]),
    ('さささ|機関室', [[], [('花見 男爵', [('', 'doc3.html#id-131')])], None])]),
  ('な',
   [('ナナナ|太郎', [[('', 'doc1.html#id-311')], [], None]),
    ('ニニニ|はな子', [[], [('森の熊', [('main', 'doc1.html#id-343')])], None]),
    ('ヌヌヌ|手紙', [[], [('狸と狐', [('', 'doc1.html#id-321')])], None]),
    ('ネネネ|犬猫', [[], [('子鹿 急須', [('', 'doc1.html#id-331')])], None])]),
  ('は',
   [('ハハハ|子鹿', [[], [('急須, 犬猫', [('', 'doc1.html#id-331')])], None]),
    ('ハハハ|狸と狐', [[], [('手紙', [('', 'doc1.html#id-321')])], None])])
]

#「ぱ」が「は」の項目に表示される.
testcase06in = { #テストパターン
'doc1': [ ('single','ナナナ|太郎','id-311','',None), ],
'doc2': [ ('single','ニニニ|はな子; フフフ|森の熊','id-343','main',None), ], #KaKkou
'doc3': [ ('pair','ヌヌヌ|手紙; ハハハ|狸と狐','id-321','',None), ],
'doc4': [ ('triple','ネネネ|犬猫; ハハハ|子鹿; さささ|急須','id-331','',None), ], #KaKkou
'doc5': [ ('single','かかか|東京; くくく|戦斧','id-148','main',None), ],
'doc6': [ ('single','ききき|満月; くくく|騎士','id-143','',None), ],
'doc7': [ ('single','ぱなぱな|はな子; ほほ|野良熊','id-343','main',None), ], #KaKkou
'doc8': [ ('pair','くくく|月光; くくく|伯爵','id-123','',None), ],
'doc9': [ ('triple','けけけ|花見; かかか|男爵; さささ|機関室','id-131','',None), ], #KaKkou
}


#-------------------------------------------------------------------

def test04_first_letter_of_term():
    bld = util.builder(testcase04in)
    bld.config.kana_text_indexer_mode = 'large'
    idx = IndexRack(bld)
    gidx = idx.create_index()
    assert gidx == testcase04out

def test05_first_letter_of_term():
    bld = util.builder(testcase05in)
    bld.config.kana_text_indexer_mode = 'small'
    idx = IndexRack(bld)
    gidx = idx.create_index()
    assert gidx == testcase05out

def test06_first_letter_of_term():
    bld = util.builder(testcase06in)
    bld.config.kana_text_indexer_mode = 'small'
    idx = IndexRack(bld)
    gidx = idx.create_index()
    assert len(gidx) == 4
    assert gidx[0][0] == 'か'
    assert gidx[1][0] == 'さ'
    assert gidx[2][0] == 'な'
    assert gidx[3][0] == 'は'
    assert gidx[0][1][0][0] == 'かかか|東京'
    assert gidx[0][1][0][1] == [[], [('戦斧', [('main', 'doc5.html#id-148')])], None]
    assert gidx[0][1][1][0] == 'かかか|男爵'
    assert gidx[0][1][1][1] == [[], [('機関室, 花見', [('', 'doc9.html#id-131')])], None]
    assert gidx[0][1][2][0] == 'ききき|満月'
    assert gidx[0][1][2][1] == [[], [('騎士', [('', 'doc6.html#id-143')])], None]
    assert gidx[0][1][3][0] == 'くくく|伯爵'
    assert gidx[0][1][3][1] == [[], [('月光', [('', 'doc8.html#id-123')])], None]
    assert gidx[0][1][4][0] == 'くくく|月光'
    assert gidx[0][1][4][1] == [[], [('伯爵', [('', 'doc8.html#id-123')])], None]
    assert gidx[0][1][5][0] == 'けけけ|花見'
    assert gidx[0][1][5][1] == [[], [('男爵 機関室', [('', 'doc9.html#id-131')])], None]
    assert gidx[1][1][0][0] == 'さささ|急須'
    assert gidx[1][1][0][1] == [[], [('犬猫 子鹿', [('', 'doc4.html#id-331')])], None]
    assert gidx[1][1][1][0] == 'さささ|機関室'
    assert gidx[1][1][1][1] == [[], [('花見 男爵', [('', 'doc9.html#id-131')])], None]
    assert gidx[2][1][0][0] == 'ナナナ|太郎'
    assert gidx[2][1][0][1] == [[('', 'doc1.html#id-311')], [], None]
    assert gidx[2][1][1][0] == 'ヌヌヌ|手紙'
    assert gidx[2][1][1][1] == [[], [('狸と狐', [('', 'doc3.html#id-321')])], None]
    assert gidx[2][1][2][0] == 'ネネネ|犬猫'
    assert gidx[2][1][2][1] == [[], [('子鹿 急須', [('', 'doc4.html#id-331')])], None]
    assert gidx[3][1][0][0] == 'ぱなぱな|はな子'
    assert gidx[3][1][0][1] == [[],
                                [('野良熊', [('main', 'doc7.html#id-343')]),
                                 ('森の熊', [('main', 'doc2.html#id-343')])],
                                None]
    assert gidx[3][1][1][0] == 'ハハハ|子鹿'
    assert gidx[3][1][1][1] == [[], [('急須, 犬猫', [('', 'doc4.html#id-331')])], None]
    assert gidx[3][1][2][0] == 'ハハハ|狸と狐'
    assert gidx[3][1][2][1] == [[], [('手紙', [('', 'doc3.html#id-321')])], None]
