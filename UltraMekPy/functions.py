#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
functions.py - help functions for UltraMek

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

import unittest
import re

def split_camel_case(string):
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', string)
    return [m.group(0) for m in matches]

def strip_and_part_line(line,char=None):
    line = line.strip()
    line = line.split(char)
    line = [l.strip() for l in line if len(line) > 0]
    return line

def replace_whitespace(text,char):
    return re.sub(r"\s+", char,text , flags=re.UNICODE)

def string2float(val):
    try:
        val = float(val)
        if int(val)==val:
            val = int(val)
    except ValueError:
        pass
        
    return val

class FunctionTests(unittest.TestCase):
    """
    Test Classfor functions
    """
    def test_strip_and_part_line(self):
        line = "  a  b   c    "
        result = strip_and_part_line(line)
        for r,c in zip(result,['a','b','c']):
            self.assertEqual(r,c)

    def test_camel_case_spliter(self):
        line = "CamelCase"
        result =split_camel_case(line)
        expected = ["Camel","Case"]
        for r, e in zip(result,expected):
            self.assertEqual(r,e)
            
        line = "camelCase"
        result =split_camel_case(line)
        expected = ["camel","Case"]
        for r, e in zip(result,expected):
            self.assertEqual(r,e)
            
    def test_replace_whitespace(self):
        line = "abc def"
        expected = "abc_def"
        self.assertEqual(expected,replace_whitespace(line,'_'))
            
