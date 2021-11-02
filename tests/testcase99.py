#!/usr/bin/python
import unittest

from src import command

#-------------------------------------------------------------------

class testCommand(unittest.TestCase):
    def test01_genindex(self):
        command.genindex()

#-------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
