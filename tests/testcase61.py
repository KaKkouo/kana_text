#!/usr/bin/python3.8
import sys
import unittest
from pprint import pprint
sys.path.append('sphinxcontrib')
from src import ExIndexRack as IndexRack
from . import util

#-------------------------------------------------------------------

#同名の関数が複数のモジュールにある
testcase01in = {
'doc01a': [('single','function1() (aaa モジュール)','id-01a','',None)],
'doc01b': [('single','function1() (bbb モジュール)','id-01b','',None)],
'doc01c': [('single','function1() (ccc モジュール)','id-01c','',None)],
'doc01d': [('single','function1() (ddd モジュール)','id-01d','',None)],
'doc01e1': [('single','function1() (eee モジュール)','id-01e1','',None)],
'doc01e2': [('single','function1() (eee モジュール)','id-01e2','main',None)],
'doc01e3': [('single','function1() (eee モジュール)','id-01e3','',None)],
'doc01e4': [('single','function1() (eee モジュール)','id-01e4','main',None)],
'doc01f1': [('single','function1() (fff モジュール)','id-01f1','main',None)],
'doc01f2': [('single','function1() (fff モジュール)','id-01f2','main',None)],
}

testcase01out = [
  ('F',
   [('function1()',
     [[],
      [('(aaa モジュール)', [('', 'doc01a.html#id-01a')]),
       ('(bbb モジュール)', [('', 'doc01b.html#id-01b')]),
       ('(ccc モジュール)', [('', 'doc01c.html#id-01c')]),
       ('(ddd モジュール)', [('', 'doc01d.html#id-01d')]),
       ('(eee モジュール)',
        [('main', 'doc01e2.html#id-01e2'),
         ('main', 'doc01e4.html#id-01e4'),
         ('', 'doc01e1.html#id-01e1'),
         ('', 'doc01e3.html#id-01e3')]),
       ('(fff モジュール)',
        [('main', 'doc01f1.html#id-01f1'), ('main', 'doc01f2.html#id-01f2')])],
      None])])
]

#同名の関数がある場合とない場合
testcase02in = {
'doc01a': [('single','function1() (aaa モジュール)','id-01a','',None)],
'doc01b': [('single','function1() (bbb モジュール)','id-01b','',None)],
'doc01c': [('single','function3() (ccc モジュール)','id-01c','',None)],
'doc01d': [('single','function4() (ddd モジュール)','id-01d','',None)],
'doc01e1': [('single','function2() (eee モジュール)','id-01e1','',None)],
'doc01e2': [('single','function1() (eee モジュール)','id-01e2','main',None)],
'doc01e3': [('single','function1() (eee モジュール)','id-01e3','',None)],
'doc01e4': [('single','function1() (eee モジュール)','id-01e4','main',None)],
'doc01f1': [('single','function1() (fff モジュール)','id-01f1','main',None)],
'doc01f2': [('single','function1() (fff モジュール)','id-01f2','main',None)],
}

testcase02out = [
  ('F',
    [('function1()',
      [[],
       [('(aaa モジュール)', [('', 'doc01a.html#id-01a')]),
        ('(bbb モジュール)', [('', 'doc01b.html#id-01b')]),
        ('(eee モジュール)',
         [('main', 'doc01e2.html#id-01e2'),
          ('main', 'doc01e4.html#id-01e4'),
          ('', 'doc01e3.html#id-01e3')]),
        ('(fff モジュール)',
         [('main', 'doc01f1.html#id-01f1'), ('main', 'doc01f2.html#id-01f2')])],
       None]),
     ('function2() (eee モジュール)', [[('', 'doc01e1.html#id-01e1')], [], None]),
     ('function3() (ccc モジュール)', [[('', 'doc01c.html#id-01c')], [], None]),
     ('function4() (ddd モジュール)', [[('', 'doc01d.html#id-01d')], [], None])])
]


#同名の関数がある場合とない場合
testcase03in = {
'doc01a': [('single','function1() (aaa モジュール)','id-01a','',None)],
}

testcase03out = [
('F',
  [('function1() (aaa モジュール)',
    [[('', 'doc01a.html#id-01a')], [], None])])]

#同名の関数がある場合とない場合
testcase04in = {
'doc01a': [('single','function1() (aaa モジュール)','id-01a','',None)],
'doc01b': [('single','function1() (bbb モジュール)','id-01b','',None)],
}

testcase04out = [
('F',
  [('function1()',
    [[],
     [('(aaa モジュール)', [('', 'doc01a.html#id-01a')]),
      ('(bbb モジュール)', [('', 'doc01b.html#id-01b')])],
     None])])]

#同名の関数がある場合とない場合
testcase05in = {
'doc01a': [('single','function1() (aaa モジュール)','id-01a','',None)],
'doc01b': [('single','function1() (bbb モジュール)','id-01b','',None)],
'doc01c': [('single','function3() (ccc モジュール)','id-01c','',None)],
}

testcase05out = [
('F',
  [('function1()',
    [[],
     [('(aaa モジュール)', [('', 'doc01a.html#id-01a')]),
      ('(bbb モジュール)', [('', 'doc01b.html#id-01b')])],
     None]),
   ('function3() (ccc モジュール)',
    [[('', 'doc01c.html#id-01c')], [], None])
  ])
]

#同名の関数がある場合とない場合
testcase06in = {
'doc01a': [('single','function1() (aaa モジュール)','id-01a','',None)],
'doc01b': [('single','function1() (bbb モジュール)','id-01b','',None)],
'doc01c': [('single','function3() (ccc モジュール)','id-01c','',None)],
'doc01d': [('single','function4() (ddd モジュール)','id-01d','',None)],
}

testcase06out = [
('F',
  [('function1()',
    [[],
     [('(aaa モジュール)', [('', 'doc01a.html#id-01a')]),
      ('(bbb モジュール)', [('', 'doc01b.html#id-01b')])],
     None]),
   ('function3() (ccc モジュール)', [[('', 'doc01c.html#id-01c')], [], None]),
   ('function4() (ddd モジュール)', [[('', 'doc01d.html#id-01d')], [], None])
  ])
]

#-------------------------------------------------------------------

class testIndexRack(unittest.TestCase):
    def test01_function_catalog(self):
        self.maxDiff = None
        env = util.env(testcase01in)
        bld = util.builder(env)
        bld.config.kana_text_indexer_mode = 'small'
        idx = IndexRack(bld)
        gidx = idx.create_genindex()
        self.assertEqual(gidx, testcase01out)

    def test02_function_catalog(self):
        self.maxDiff = None
        env = util.env(testcase02in)
        bld = util.builder(env)
        bld.config.kana_text_indexer_mode = 'small'
        idx = IndexRack(bld)
        gidx = idx.create_genindex()
        self.assertEqual(gidx, testcase02out)

    def test03_function_catalog(self):
        self.maxDiff = None
        env = util.env(testcase03in)
        bld = util.builder(env)
        bld.config.kana_text_indexer_mode = 'small'
        idx = IndexRack(bld)
        gidx = idx.create_genindex()
        self.assertEqual(gidx, testcase03out)

    def test04_function_catalog(self):
        self.maxDiff = None
        env = util.env(testcase04in)
        bld = util.builder(env)
        bld.config.kana_text_indexer_mode = 'small'
        idx = IndexRack(bld)
        gidx = idx.create_genindex()
        self.assertEqual(gidx, testcase04out)

    def test05_function_catalog(self):
        self.maxDiff = None
        env = util.env(testcase05in)
        bld = util.builder(env)
        bld.config.kana_text_indexer_mode = 'small'
        idx = IndexRack(bld)
        gidx = idx.create_genindex()
        self.assertEqual(gidx, testcase05out)

    def test06_function_catalog(self):
        self.maxDiff = None
        env = util.env(testcase06in)
        bld = util.builder(env)
        bld.config.kana_text_indexer_mode = 'small'
        idx = IndexRack(bld)
        gidx = idx.create_genindex()
        self.assertEqual(gidx, testcase06out)

#-------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()

    #bld.config.kana_text_indexer_mode = 'small'
    #gidx = bld.create_genindex(testcase08in)
    #pprint(gidx)
