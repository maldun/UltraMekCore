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

from dataclasses import dataclass, field, asdict
import json
import os
import unittest
from .functions import strip_and_part_line

from .constants import U8

@dataclass
class Tile:
    """
    Class to store and handle tiles.
    """
    pos_x: int = -1
    pos_y: int = -1
    tile_type: str = ""
    height: int = 0
    properties: list = field(default_factory= lambda: list())

    def to_dict(self):
        return asdict(self)

    def get_property(self, prop):
        for p in self.properties:
            if prop == p[0]:
                if prop == "road":
                    return p[1:3]
                return p[1]
        return [0,0] if prop == "road" else 0

class Board:
    """
    Class to parse and handle board files and provide logic and transforms.
    Tiles direction: (list is transposed for convienience, i.e. self.tiles[x][y]
    calls the tile on pos_x and pos_y, to make closer to usage in numpy)
    ------- x
    |
    |
    |
    y
    """
    SIZE_IDENTIFIER = "size"
    HEX_IDENTIFIER = "hex"
    END_IDENTIFIER = "end"

    LAYERS = {"woods","heights","rough","sand","swamp","water","planted_fields","foliage_elev",
                  "tile_type","road"}
    
    def __init__(self,filename):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Error: File {filename} does not exist!")

        with open(filename,'r',encoding=U8) as fp:
            for line in fp:
                if line.startswith(self.SIZE_IDENTIFIER): # We assume this is always first!
                    self.size_x, self.size_y = self.get_dims(line)
                    line_nr = 0
                    self.tiles = [[None for k in range(self.size_y)]
                                      for l in range(self.size_x)] 
                elif line.startswith(self.HEX_IDENTIFIER):
                    tile = self.create_tile_from_line(line,line_nr)
                    self.tiles[tile.pos_x][tile.pos_y] = tile
                    line_nr += 1
                elif line.startswith(self.END_IDENTIFIER):
                    break

        self.layers = None
                    
                
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
        if properties != '':
            properties = properties.split(';')
            properties = [[int(e) if k > 0 else e for k,e in enumerate(p.split(':'))]
                            for p in properties]
        else:
            properties = []
        height = int(line[2])
        return Tile(pos_x=pos_x,pos_y=pos_y,tile_type=tile_type,properties=properties,height=height)

    def to_dict(self):
        """
        Creates a dictionary object which is easyily convertible to json.
        """
        dic = {"size_x": self.size_x,"size_y":self.size_y}
        llist = [[tile.to_dict() for tile in row] for row in self.tiles]
        dic["tiles"] = llist
        return dic
    
    def to_json(self):
        """
        Creates a JSON string object which can be interpreted by other programs.
        """
        return json.dumps(self.to_dict())

    def flatten(self):
        """
        Flattens the board in that sense as it stores it in several
        flat layers which are easier to process by logic
        """
        layer_dict = {}
        for layer in self.LAYERS:
            if layer == "heights":
                layer_dict[layer] = [[tile.height for tile in row] for row in self.tiles]
            elif layer == "tile_type":
                layer_dict[layer] = [[tile.tile_type for tile in row] for row in self.tiles]
            else:
                layer_dict[layer] = [[tile.get_property(layer) for tile in row]
                                        for row in self.tiles]
        self.layers = layer_dict


    def to_flat_dict(self):
        """
        Creates a dictionary object which is easyily convertible to json.
        """
        if self.layers is None:
            self.flatten()
        dic = {"size_x": self.size_x,"size_y":self.size_y}
        dic.update(self.layers)
        return dic
        

##########################################################
# Tests
#########################################################

class TileTests(unittest.TestCase):
    """
    Tests for the Tile class.
    """
    def setUp(self):
        self.empty_tile = Tile()
        self.test_tile = Tile(pos_x=0,pos_y=1,tile_type="snow",properties=[["planted_fields",1]],\
                              height=-1)
    
    def test_Tile_creation(self):
        self.assertEqual(self.empty_tile.pos_x,-1)
        self.assertEqual(self.empty_tile.pos_y,-1)
        self.assertEqual(self.empty_tile.tile_type,"")
        self.assertEqual(self.empty_tile.properties,[])
        self.assertEqual(self.empty_tile.height,0)

        self.assertEqual(self.test_tile.pos_x,0)
        self.assertEqual(self.test_tile.pos_y,1)
        self.assertEqual(self.test_tile.tile_type,"snow")
        self.assertEqual(self.test_tile.properties,[["planted_fields",1]])
        self.assertEqual(self.test_tile.height,-1)

    def test_to_dict(self):
        dic = self.test_tile.to_dict()
        self.assertIsInstance(dic,dict)
        self.assertEqual(dic["tile_type"],"snow")
        self.assertEqual(dic["height"],-1)
        

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
        self.assertEqual(tile.properties,[["planted_fields",1]])
        
    def test_Board_creation(self):
        with self.assertRaises(FileNotFoundError) as context:
            Board("bla.board")

        b = self.boards[0]
        t = b.tiles[1][0]
        self.assertEqual(t.height,-1)
        self.assertEqual(t.properties,[])
        self.assertEqual(t.tile_type,"snow")


    def test_to_dict(self):
        b = self.boards[0]
        d = b.to_dict()
        t = d["tiles"][1][0]
        self.assertEqual(t['height'],-1)
        self.assertEqual(t['tile_type'],"snow")
        self.assertEqual(d["size_x"],b.size_x)
        self.assertEqual(d["size_y"],b.size_y)
        
    def test_to_json(self):
        b = self.boards[0]
        j = b.to_json()
        self.assertIsInstance(j,str)
        
    def test_to_flat_dict(self):
        b = self.boards[0]
        f = b.to_flat_dict()
        with open('test_json.json','w') as fp:
            json.dump(f,fp)



    
