"""
boards.py - Classes and Tools for Map/Board Handling (compatible with MegaMek)

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

from dataclasses import dataclass, field
import os
import unittest
from .functions import strip_and_part_line

@dataclass
class Tile:
    """
    Class to store and handle tiles.
    """
    pos_x: int = -1
    pos_y: int = -1
    tile_type: str = ""
    height: int = 0
    properties: tuple = field(default_factory= lambda: tuple())

class Board:
    """
    Class to parse and handle board files and provide logic and transforms.
    """
    SIZE_IDENTIFIER = "size"
    HEX_IDENTIFIER = "hex"
    END_IDENTIFIER = "end"
    
    def __init__(self,filename):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Error: File {filename} does not exist!")

        with open(filename,'r') as fp:
            for line in fp:
                if line.startswith(self.SIZE_IDENTIFIER): # We assume this is always first!
                    self.size_x, self.size_y = self.get_dims(line)
                    line_nr = 0
                    tiles = [[None for k in range(self.size_x)]
                                      for l in range(self.size_y)] 
                elif line.startswith(self.HEX_IDENTIFIER):
                    self.create_tile_from_line(line,line_nr)
                    line_nr += 1
                elif line.startswith(self.END_IDENTIFIER):
                    break
                    
                
    @staticmethod
    def get_dims(line):
        line = strip_and_part_line(line)
        size_x = int(line[1])
        size_y = int(line[2])
        return size_x, size_y
        
    def create_tile_from_line(self,line,line_nr):
        pos_x = line_nr%self.size_x
        pos_y = line_nr//self.size_x
        line = strip_and_part_line(line)
        tile_type = line[-1].replace('"',"")
        properties = line[-2].replace('"',"")
        properties = properties.split(';')
        properties = tuple(tuple([int(e) if k > 0 else e for k,e in enumerate(p.split(':'))])
                           for p in properties)
        height = int(line[2])
        return Tile(pos_x=pos_x,pos_y=pos_y,tile_type=tile_type,properties=properties,height=height)
        



##########################################################
# Tests
#########################################################

class TileTests(unittest.TestCase):
    """
    Tests for the Tile class.
    """
    def setUp(self):
        self.empty_tile = Tile()
        self.test_tile = Tile(pos_x=0,pos_y=1,tile_type="snow",properties=(("planted_fields",1),),\
                              height=-1)
    
    def test_Tile_creation(self):
        self.assertEqual(self.empty_tile.pos_x,-1)
        self.assertEqual(self.empty_tile.pos_y,-1)
        self.assertEqual(self.empty_tile.tile_type,"")
        self.assertEqual(self.empty_tile.properties,())
        self.assertEqual(self.empty_tile.height,0)

        self.assertEqual(self.test_tile.pos_x,0)
        self.assertEqual(self.test_tile.pos_y,1)
        self.assertEqual(self.test_tile.tile_type,"snow")
        self.assertEqual(self.test_tile.properties,(("planted_fields",1),))
        self.assertEqual(self.test_tile.height,-1)
        

class BoardTests(unittest.TestCase):
    """
    Tests for the Board class.
    """
    def setUp(self):
        self.path = os.path.join("test","samples")
        self.board_files = ["snow.board","test.board",]
        self.boards = [Board(os.path.join(self.path,f)) for f in self.board_files]

    def test_get_dims(self):
        line = "size 16 17"
        x,y = Board.get_dims(line)
        self.assertEqual(x,16)
        self.assertEqual(y,17)
        
    def test_create_tile_from_line(self):
        line = 'hex 0402 -2 "planted_fields:1" "snow"'
        line_nr = 21-2
        board = self.boards[0]
        tile = board.create_tile_from_line(line,line_nr)
        self.assertEqual(tile.pos_x,3)
        self.assertEqual(tile.pos_y,1)
        self.assertEqual(tile.height,-2)
        self.assertEqual(tile.tile_type,"snow")
        self.assertEqual(tile.properties,(("planted_fields",1),))
        
    def test_Board_creation(self):
        with self.assertRaises(FileNotFoundError) as context:
            Board("bla.board")






    
