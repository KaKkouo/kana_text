#!/usr/bin/python
import sys, unittest

sys.path.append('sphinxcontrib')
from src import IndexRack

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
         [('see also bar', []), ('see foo', [])],
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

class _domain(object):
    def __init__(self, entries):
        self.entries = entries

class _env(object):
    def __init__(self, domain):
        self.domain = {}
        self.domain['index'] = domain
    def get_domain(self, domain_type):
        return self.domain[domain_type]

class _config(object):
    def __init__(self):
        self.kana_text_separator = r'\|'
        self.kana_text_indexer_mode = 'normal'
        self.kana_text_word_file = ''
        self.kana_text_word_list = ()
        self.html_kana_text_on_genindex = False
        self.html_change_triple = False

class _builder(object):
    def __init__(self, env):
        self.env = env
        self.get_domain = env.get_domain
        self.config = _config()
    def get_relative_uri(self, uri_type, file_name):
        return f'{file_name}.html'

class IndexEntries(IndexRack):
    def __init__(self, env):
        self.env = env
        self._kana_catalog = {}
    def create_index(self, builder):
        self.__init__(builder)
        self.config = builder.config
        self.get_relative_uri = builder.get_relative_uri
        return self.create_genindex()

#-------------------------------------------------------------------

class testIndexEntries(unittest.TestCase):
    def test01_classifier(self):
        self.maxDiff = None
        dmn = _domain(testcase01i)
        env = _env(dmn)
        bld = _builder(env)
        gidx = IndexEntries(env).create_index(bld)
        self.assertEqual(testcase01o, gidx)
    def test02_see_and_seealso(self):
        self.maxDiff = None
        dmn = _domain(testcase02i)
        env = _env(dmn)
        bld = _builder(env)
        gidx = IndexEntries(env).create_index(bld)
        self.assertEqual(testcase02o, gidx)
    def test03_homonymous_function(self):
        self.maxDiff = None
        dmn = _domain(testcase03i)
        env = _env(dmn)
        bld = _builder(env)
        gidx = IndexEntries(env).create_index(bld)
        self.assertEqual(testcase03o, gidx)
    def test04_homonymous_function(self):
        self.maxDiff = None
        dmn = _domain(testcase04i)
        env = _env(dmn)
        bld = _builder(env)
        gidx = IndexEntries(env).create_index(bld)
        self.assertEqual(testcase04o, gidx)

#-------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
