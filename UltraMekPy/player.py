"""
player.py - Classes and Tools for players (compatible with MekHQ)

Copyright © 2024 Stefan H. Reiterer.
stefan.harald.reiterer@gmail.com 
This work is under GPL v2 as it should remain free but compatible with MekHQ

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

import os
import unittest

@dataclass
class Player:
    name: str
    forces: dict
    initiative: int = 0

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self,val):
        self._name=val
        
    @property
    def forces(self):
        return self._forces
    @forces.setter
    def forces(self,val):
        self._forces=val
    
    @property
    def initiative(self):
        return self._initiative
    
    @initiative.setter
    def initiative(self,val):
        self._initiative = val
    
    def to_dict(self):
        return self.forces


class PlayerTests(unittest.TestCase):
    
    def setUp(self):
        from .game import GameState
        self.game = GameState()
        #self.mulp = MulParser()
        #self.uh = UnitHandler()
        self.path = os.path.join("test","samples")
        self.mul_files = ["example.mul","example2.mul","player1.mul"]
        self.mul_files = [os.path.join(self.path,f) for f in self.mul_files]
        self.player_name = "player1"
        self.player_forces = self.game.process_units(self.mul_files[2])
        self.player = Player(self.player_name,self.player_forces)

    def test___init__(self):
        self.assertEqual(self.player.name,self.player_name)
        
