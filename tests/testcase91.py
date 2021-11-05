#!/usr/bin/python
import unittest
from src import ExtIndexRack as IndexRack
from . import util 

testcase01i = { 
'doc1': [
    ('single', 'aaa', 'id-111', '', 'clf1'),
    ('single', 'bbb', 'id-112', '', None),
],
'doc2': [
    ('single', 'aaa', 'id-121', '', None),
    ('single', 'bbb', 'id-122', '', 'clf2'),
], }

testcase01o = [
('clf1',
  [('aaa', [[('', 'doc1.html#id-111'), ('', 'doc2.html#id-121')], [], 'clf1']), ]
),
('clf2',
  [('bbb', [[('', 'doc1.html#id-112'), ('', 'doc2.html#id-122')], [], None]), ]
),
]


testcase02i = {
'doc1': [
    ('see','hogehoge; foo','id-211','main',None),
    ('seealso','hogehoge; bar','id-212','main',None), ]
}

testcase02o = [
('H',
    [('hogehoge',
        [[],
         [('see foo', []), ('see also bar', [])],
         None
        ])
    ])
]

testcase03i = {
'doc1': [
    ('single','func1() (aaa module)','id-311','',None),
    ('single','func1() (bbb module)','id-312','',None),
    ('single','func1() (ccc module)','id-313','',None),]
}

testcase03o = [
('F',
  [('func1()',
    [[],
     [('(aaa module)', [('', 'doc1.html#id-311')]),
      ('(bbb module)', [('', 'doc1.html#id-312')]),
      ('(ccc module)', [('', 'doc1.html#id-313')])
     ],
     None])])
]


testcase04i = {
'doc1': [
    ('single','func1() (aaa module)','id-411','',None),
    ('single','func1() (bbb module)','id-412','',None),
    ('single','func1() (ccc module)','id-413','main',None), ]
}

testcase04o = [
('F',
  [('func1()',
    [[],
     [('(aaa module)', [('', 'doc1.html#id-411')]),
      ('(bbb module)', [('', 'doc1.html#id-412')]),
      ('(ccc module)', [('main', 'doc1.html#id-413')]), ],
     None])])
]

#-------------------------------------------------------------------

class testIndexEntries(unittest.TestCase):
    def test01_classifier(self):
        env = util.env(testcase01i)
        bld = util.builder(env)
        gidx = IndexRack(bld).create_index()
        self.assertEqual(testcase01o, gidx)
    def test02_see_and_seealso(self):
        env = util.env(testcase02i)
        bld = util.builder(env)
        gidx = IndexRack(bld).create_index()
        self.assertEqual(testcase02o, gidx)
    def test03_homonymous_function(self):
        env = util.env(testcase03i)
        bld = util.builder(env)
        gidx = IndexRack(bld).create_index()
        self.assertEqual(testcase03o, gidx)
    def test04_homonymous_function(self):
        env = util.env(testcase04i)
        bld = util.builder(env)
        gidx = IndexRack(bld).create_index()
        self.assertEqual(testcase04o, gidx)

#-------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
