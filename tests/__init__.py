import unittest

from unittest_01 import testKanaText
from unittest_02 import testKanaValue
from unittest_03 import testKanaIndexer

def suites():
    suites = unittest.TestSuite()
    suites.addTests(unittest.makeSuite(testKanaText))
    suites.addTests(unittest.makeSuite(testKanaValue))
    suites.addTests(unittest.makeSuite(testKanaIndexer))
    return suites
