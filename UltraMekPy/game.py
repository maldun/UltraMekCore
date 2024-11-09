"""
game.py - Classes and Tools for Game state and logic Handling (compatible with MekHQ)

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
from copy import deepcopy

from . import boards
from . import parsers as par
from . import data
from . import constants as const
from .player import Player

class GameState:
    FORCES_KEY = "forces"
    def __init__(self):
        self.unit_handler = data.UnitHandler()
        self.mul_parser = par.MulParser()

    def setup_board(self, board):
        self.board = board
    
    def process_units(self, forces):
        # parse corrseponding mul file
        mulp = self.mul_parser
        forces = mulp(forces)
        entities = forces[mulp.ENTITY_PLURAL]
        for ID, entity in entities.items():
            entity_data = self.unit_handler(entity)
            forces[mulp.ENTITY_PLURAL][ID][const.ENTITY_DATA] = entity_data
            gfx_data = self.unit_handler.get_gfx(entity)
            forces[mulp.ENTITY_PLURAL][ID][const.GFX_DATA] = gfx_data
        return forces
    
    def setup_players(self, player_request):
        players = {}
        for key, val in player_request.items():
            val1 = deepcopy(val)
            val1[self.FORCES_KEY] = self.process_units(val[self.FORCES_KEY])
            players[key] = Player(key,val1)
            
        self.players = players
        return players
        
