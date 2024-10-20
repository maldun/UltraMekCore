#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
unittests.py - unittests for UltraMek

Copyright © 2024 Stefan H. Reiterer.
stefan.harald.reiterer@gmail.com 
This work is under GPL v2 as it should remain free but compatible with MegaMek

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

import os
import sys
sys.path.append(os.path.split(os.getcwd())[0])
sys.path.append(os.getcwd())

import unittest
import UltraMekPy
from UltraMekPy import boards, functions, parsers

MODULES = [boards,functions,parsers]

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite  = unittest.TestSuite()

    # add tests to the test suite
    for module in MODULES:
        tests = loader.loadTestsFromModule(module)
        suite.addTests(tests)

    # initialize a runner, pass it your suite and run it
    runner = unittest.TextTestRunner(verbosity=3)
    result = runner.run(suite)

    nr_errors = len(result.errors)
    print(f"Errors: {nr_errors} tests with errors: \n")
    for test, res in result.errors:
        print(test, end=': \n\n')
        print(res)
    nr_failed = len(result.failures)
    print(f"Fail: {nr_failed} tests failed: \n")
    for test, res in result.failures:
        print(test, end=': \n\n')
        print(res)
    
    if not result.wasSuccessful():
        sys.exit(nr_failed + nr_errors)


