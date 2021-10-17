import unittest

from unittest_01 import testKanaText as KanaText
from unittest_02 import testKanaTextUnit as KanaTextUnit
from unittest_03 import testIndexUnit as IndexUnit
from unittest_04 import testIndexRack as IndexRack1
from unittest_05 import testIndexRack as IndexRack2
from unittest_06 import testIndexRack as IndexRack3
from unittest_07 import testIndexRack as IndexRack4
from unittest_08 import testIndexRack as IndexRack5
from unittest_09 import testIndexEntries as IndexEntries

def suites():
    suites = unittest.TestSuite()
    suites.addTests(unittest.makeSuite(KanaText))
    suites.addTests(unittest.makeSuite(KanaTextUnit))
    suites.addTests(unittest.makeSuite(IndexUnit))
    suites.addTests(unittest.makeSuite(IndexRack1))
    suites.addTests(unittest.makeSuite(IndexRack2))
    suites.addTests(unittest.makeSuite(IndexRack3))
    suites.addTests(unittest.makeSuite(IndexRack4))
    suites.addTests(unittest.makeSuite(IndexRack5))
    suites.addTests(unittest.makeSuite(IndexEntries))
    return suites
