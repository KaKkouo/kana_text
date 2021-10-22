#!/usr/bin/python3.8
import sys
import unittest
from pprint import pprint
sys.path.append('sphinxcontrib')
from src import IndexRack
from . import util

#-------------------------------------------------------------------

#同じ単語なら同じ読み（細かく検証）
testcase01in = {
'doc01b': [('single','むむ|検証０１','id-01b','',None)],
'doc01a': [('single','ああ|検証０１','id-01a','',None)],
'doc01c': [('single','をを|検証０１','id-01c','',None)], #KaKkou
'doc02a': [('single','ああ|検証０２','id-02a','',None)],
'doc02b': [('single','むむ|検証０２','id-02b','main',None)], #KaKkou
'doc02c': [('single','をを|検証０２','id-02c','',None)],
'doc03a': [('single','ああ|検証０３','id-03a','',None)],
'doc03b': [('single',  'む|検証０３','id-03b','main',None)], #KaKkou
'doc03c': [('single','をを|検証０３','id-03c','',None)],
'doc04a': [('single',  'あ|検証０４','id-04a','',None)],
'doc04b': [('single','むむ|検証０４','id-04b','',None)], #KaKkou
'doc04c': [('single',  'を|検証０４','id-04c','',None)],
'doc05a': [('single','ああ|検証０５; いい|検証０５','id-05a','',None)],
'doc05b': [('single','むむ|検証０５; めめ|検証０５','id-05b','main',None)], #KaKkou
'doc05c': [('single','をを|検証０５; んん|検証０５','id-05c','',None)],
'doc06a': [('single','ああ|検証０６; いい|検証０６','id-06a','',None)],
'doc06b': [('single',  'む|検証０６; めめ|検証０６','id-06b','main',None)], #KaKkou
'doc06c': [('single','をを|検証０６; んん|検証０６','id-06c','',None)],
'doc07a': [('pair','ああ|検証０７; いい|検証０７','id-07a','',None)],
'doc07b': [('pair','むむ|検証０７; めめ|検証０７','id-07b','main',None)],
'doc07c': [('pair','をを|検証０７; んん|検証０７','id-07c','',None)],
'doc08a': [('pair','ああ|検証０８; いい|検証０８','id-08a','',None)],
'doc08b': [('pair',  'む|検証０８; めめ|検証０８','id-08b','main',None)],
'doc08c': [('pair','をを|検証０８; んん|検証０８','id-08c','',None),],
}

testcase01out = [
('ま',
  [('む|検証０３',
    [[('main', 'doc03b.html#id-03b'),
      ('', 'doc03a.html#id-03a'),
      ('', 'doc03c.html#id-03c')],
     [],
     None]),
   ('むむ|検証０１',
    [[('', 'doc01a.html#id-01a'),
      ('', 'doc01b.html#id-01b'),
      ('', 'doc01c.html#id-01c')],
     [],
     None]),
   ('むむ|検証０２',
    [[('main', 'doc02b.html#id-02b'),
      ('', 'doc02a.html#id-02a'),
      ('', 'doc02c.html#id-02c')],
     [],
     None]),
   ('むむ|検証０４',
    [[('', 'doc04a.html#id-04a'),
      ('', 'doc04b.html#id-04b'),
      ('', 'doc04c.html#id-04c')],
     [],
     None]),
   ('むむ|検証０５',
    [[],
     [('むむ|検証０５',
       [('main', 'doc05b.html#id-05b'),
        ('', 'doc05a.html#id-05a'),
        ('', 'doc05c.html#id-05c')])],
     None]),
   ('むむ|検証０７',
    [[],
     [('むむ|検証０７',
       [('main', 'doc07b.html#id-07b'),
        ('main', 'doc07b.html#id-07b'),
        ('', 'doc07a.html#id-07a'),
        ('', 'doc07a.html#id-07a'),
        ('', 'doc07c.html#id-07c'),
        ('', 'doc07c.html#id-07c')])],
     None]),
   ('めめ|検証０６',
    [[],
     [('めめ|検証０６',
       [('main', 'doc06b.html#id-06b'),
        ('', 'doc06a.html#id-06a'),
        ('', 'doc06c.html#id-06c')])],
     None]),
   ('めめ|検証０８',
    [[],
     [('めめ|検証０８',
       [('main', 'doc08b.html#id-08b'),
        ('main', 'doc08b.html#id-08b'),
        ('', 'doc08a.html#id-08a'),
        ('', 'doc08a.html#id-08a'),
        ('', 'doc08c.html#id-08c'),
        ('', 'doc08c.html#id-08c')])],
     None])])
]

#同じ単語なら同じ読み（triple）
testcase02in = {
'doc09a': [('triple','ああ|球球球; いい|球球球; そそ|球球球','id-09a','',None)],
'doc09b': [('triple','むむ|球球球; めめ|球球球; もも|球球球','id-09b','main',None)],
'doc09c': [('triple','をを|球球球; んん|球球球; ろろ|球球球','id-09c','',None)],
'doc10a': [('triple','ああ|拾拾拾; いい|拾拾拾; そそ|拾拾拾','id-10a','',None)],
'doc10b': [('triple',  'む|拾拾拾; めめ|拾拾拾; もも|拾拾拾','id-10b','main',None)],
'doc10c': [('triple','をを|拾拾拾; んん|拾拾拾; ろろ|拾拾拾','id-10c','',None)],
}

testcase02out = [
('ま',
  [('むむ|球球球',
    [[],
     [('むむ|球球球 むむ|球球球', #seeのデリミタ仕様
       [('main', 'doc09b.html#id-09b'),
        ('main', 'doc09b.html#id-09b'),
        ('', 'doc09a.html#id-09a'),
        ('', 'doc09a.html#id-09a'),
        ('', 'doc09c.html#id-09c'),
        ('', 'doc09c.html#id-09c')]),
      ('むむ|球球球, むむ|球球球', #seealsoのデリミタ仕様
       [('main', 'doc09b.html#id-09b'),
        ('', 'doc09a.html#id-09a'),
        ('', 'doc09c.html#id-09c')])],
     None]),
   ('めめ|拾拾拾',
    [[],
     [('めめ|拾拾拾 めめ|拾拾拾', #seeのデリミタ仕様
       [('main', 'doc10b.html#id-10b'),
        ('main', 'doc10b.html#id-10b'),
        ('', 'doc10a.html#id-10a'),
        ('', 'doc10a.html#id-10a'),
        ('', 'doc10c.html#id-10c'),
        ('', 'doc10c.html#id-10c')]),
      ('めめ|拾拾拾, めめ|拾拾拾', #seealsoのデリミタ仕様
       [('main', 'doc10b.html#id-10b'),
        ('', 'doc10a.html#id-10a'),
        ('', 'doc10c.html#id-10c')])],
     None])])
]

#同じ単語なら読みを揃える

testcase03in = {
'doc01': [('single','ああ|球球球; いい|球球球','id-01','',None)],
'doc02': [('see','かか|球球球; めめ|球球球','id-02','',None)],
'doc03': [('single','ささ|球球球; んん|球球球','id-03','',None)],
'doc04': [('seealso','たた|拾拾拾; いい|拾拾拾','id-04','',None)],
'doc05': [('single','なな|拾拾拾; めめ|拾拾拾','id-05','',None)],
'doc06': [('single','おお|拾拾拾; んん|拾拾拾','id-06','',None)],
}

testcase03out = [
('あ',
  [('ああ|球球球',
    [[],
     [('see 球球球', []),
      ('ああ|球球球', [('', 'doc01.html#id-01'), ('', 'doc03.html#id-03')]), ],
     None])]),
('な',
  [('なな|拾拾拾',
    [[],
     [('see also 拾拾拾', []),
      ('なな|拾拾拾', [('', 'doc05.html#id-05'), ('', 'doc06.html#id-06')]), ],
     None])])
]

#kana_text_word_listの上書き
testcase04in = {
'doc01': [('single','ああ|球球球; いい|球球球','id-01','',None)],
'doc02': [('see','かか|球球球; めめ|球球球','id-02','',None)],
'doc03': [('single','ささ|球球球; んん|球球球','id-03','',None)],
'doc04': [('seealso','たた|拾拾拾; いい|拾拾拾','id-04','',None)],
'doc05': [('single','なな|拾拾拾; めめ|拾拾拾','id-05','',None)],
'doc06': [('single','おお|拾拾拾; んん|拾拾拾','id-06','',None)],
}

testcase04out = [
('な',
  [('ののの|球球球',
    [[],
     [('ののの|球球球', [('', 'doc01.html#id-01'), ('', 'doc03.html#id-03')]),
      ('see 球球球', [])],
     None])]),
 ('ら',
  [('れれれ|拾拾拾',
    [[],
     [('れれれ|拾拾拾', [('', 'doc05.html#id-05'), ('', 'doc06.html#id-06')]),
      ('see also 拾拾拾', [])],
     None])])]

#kana_text_word_listの上書き
testcase05in = {
'doc01': [('single','ああ|球球球; いい|球球球','id-01','',None)],
'doc02': [('see','かか|球球球; めめ|球球球','id-02','',None)],
'doc03': [('single','ささ|球球球; んん|球球球','id-03','',None)],
'doc04': [('seealso','たた|拾拾拾; いい|拾拾拾','id-04','',None)],
'doc05': [('single','なな|拾拾拾; めめ|拾拾拾','id-05','',None)],
'doc06': [('single','おお|拾拾拾; んん|拾拾拾','id-06','',None)],
}

testcase05out = [
('な',
  [('ねねね|拾拾拾',
    [[],
     [('ねねね|拾拾拾', [('', 'doc05.html#id-05'), ('', 'doc06.html#id-06')]),
      ('see also 拾拾拾', [])],
     None])]),
 ('ら',
  [('るるる|球球球',
    [[],
     [('るるる|球球球', [('', 'doc01.html#id-01'), ('', 'doc03.html#id-03')]),
      ('see 球球球', [])],
     None])])
 ]

#-------------------------------------------------------------------

class testIndexRack(unittest.TestCase):

    def test01_kana_catalog(self):
        self.maxDiff = None
        env = util.env(testcase01in)
        bld = util.builder(env)
        bld.config.kana_text_indexer_mode = 'small'
        idx = IndexRack(bld)
        gidx = idx.create_genindex()
        self.assertEqual(gidx, testcase01out)

    def test02_kana_catalog(self):
        self.maxDiff = None
        env = util.env(testcase02in)
        bld = util.builder(env)
        bld.config.kana_text_indexer_mode = 'small'
        idx = IndexRack(bld)
        gidx = idx.create_genindex()
        self.assertEqual(gidx, testcase02out)

    def test03_kana_catalog(self):
        assert False
        self.maxDiff = None
        env = util.env(testcase03in)
        bld = util.builder(env)
        bld.config.kana_text_indexer_mode = 'small'
        idx = IndexRack(bld)
        gidx = idx.create_genindex()
        self.assertEqual(gidx, testcase03out)

    def test04_kana_catalog(self):
        assert False
        self.maxDiff = None
        env = util.env(testcase04in)
        bld = util.builder(env)
        bld.config.kana_text_word_list = ['ののの|球球球^', 'れれれ|拾拾拾^']
        bld.config.kana_text_indexer_mode = 'small'
        bld.config.html_kana_text_on_genindex = True
        idx = IndexRack(bld)
        gidx = idx.create_genindex()
        self.assertEqual(gidx, testcase04out)

    def test05_kana_catalog(self):
        assert False
        self.maxDiff = None
        env = util.env(testcase05in)
        bld = util.builder(env)
        bld.config.kana_text_word_list = []
        bld.config.kana_text_word_file = 'tests/word_list.txt'
        bld.config.kana_text_indexer_mode = 'small'
        bld.config.html_kana_text_on_genindex = True
        idx = IndexRack(bld)
        gidx = idx.create_genindex()
        self.assertEqual(gidx, testcase05out)

#-------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()

    #bld.config.kana_text_indexer_mode = 'small'
    #gidx = bld.create_genindex(testcase08in)
    #pprint(gidx)
