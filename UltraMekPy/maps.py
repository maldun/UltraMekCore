"""
maps.py - Classes and Tools for Map Handling (compatible with MegaMek)

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

from dataclasses import dataclass 
import unittest

@dataclass
class Tile:
    """
    Class to store and handle tiles.
    """
    pos_x: int = -1
    pos_y: int = -1
    tile_type: string = ""
    properties: dict = {}

    @classmethod
    def create_tile_from_string(cls,string):
        pass

class Map:
    """
    Class to parse and handle map files
    """
    pass

class TileTests(unittest.testcase):
    """
    Tests for the Tile class.
    """
    def test_Tile_creation(self):
        pass





    
