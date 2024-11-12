"""
rolls.py - Classes and Tools for managing rolls (compatible with MekHQ)

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

from abc import ABC, abstractmethod
import random
import unittest

class Roll(ABC):
    """
    Base class for performing rolls
    """
    def __init__(self,game_state,request_info):
        self.game_state = game_state
        self.request_info = request_info
    
    @classmethod
    def get_roll_type(cls):
        return cls.__name__
    
    def roll(self,nr_dices=2):
        result = self.compute_modifiers()
        for _ in range(nr_dices):
            result += random.randint(1,6)
        return result
    
    def _compute_modifiers(self,game_state,request_info):
        return 0
    
    def compute_modifiers(self):
        return self._compute_modifiers(self.game_state,self.request_info)
    

INITIATIVE = "Initiative"
class Initiative(Roll):
    pass

rtypes = [Initiative]
roll_map = {}
for rtype in rtypes:
    r = rtype.get_roll_type().lower()
    roll_map[r] = rtype

class RollTests(unittest.TestCase):
    
    def setUp(self):
        from .game import GameState
        self.game = GameState()

    def test___init__(self):
        for t,r in roll_map.items():
            self.assertIn(r().roll(),list(range(2,12+1)))
            self.assertIn("initiative",roll_map.keys())
        

