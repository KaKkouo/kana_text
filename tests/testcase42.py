#!/usr/bin/python3.8
import sys
import unittest

from src import ExtIndexRack as IndexRack
from . import util

#-------------------------------------------------------------------

testcase01in = { #テストパターン
    'doc1': [ ('single','いいい|壱壱壱^3','id-111','',None), ],
    'doc2': [ ('single','ろろろ|壱壱壱^21','id-121','',None), ],
    'doc3': [ ('single','ははは|壱壱壱^111','id-131','',None), ],
}

testcase01out = [
('は',
  [('ははは|壱壱壱',
    [[('', 'doc1.html#id-111'),
      ('', 'doc2.html#id-121'),
      ('', 'doc3.html#id-131')],
     [],
     None])])
]


#-------------------------------------------------------------------


class testIndexRack(unittest.TestCase):
    def test01_create_index(self):
        self.maxDiff = None
        env = util.env(testcase01in)
        bld = util.builder(env)
        idx = IndexRack(bld)
        gidx = idx.create_index()
        self.assertEqual(gidx, testcase01out)


#-------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
