import unittest

from unittest_01 import testKanaText
from unittest_02 import testKanaTextUnit
from unittest_03 import testKanaIndexer

def suites():
    suites = unittest.TestSuite()
    suites.addTests(unittest.makeSuite(testKanaText))
    suites.addTests(unittest.makeSuite(testKanaTextUnit))
    suites.addTests(unittest.makeSuite(testKanaIndexer))
    return suites
