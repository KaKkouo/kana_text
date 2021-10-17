import unittest

from . import unittest01, unittest02, unittest03, unittest04, unittest05
from . import unittest06, unittest07, unittest08, unittest09

def suites():
    suites = unittest.TestSuite()
    suites.addTests(unittest.makeSuite(unittest01.testKanaText))
    suites.addTests(unittest.makeSuite(unittest02.testKanaTextUnit))
    suites.addTests(unittest.makeSuite(unittest03.testIndexUnit))
    suites.addTests(unittest.makeSuite(unittest04.testIndexRack))
    suites.addTests(unittest.makeSuite(unittest05.testIndexRack))
    suites.addTests(unittest.makeSuite(unittest06.testIndexRack))
    suites.addTests(unittest.makeSuite(unittest07.testIndexRack))
    suites.addTests(unittest.makeSuite(unittest08.testIndexRack))
    suites.addTests(unittest.makeSuite(unittest09.testIndexEntries))
    return suites
