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
from . import rolls
import unittest

class GameState:
    FORCES_KEY = "forces"
    ROLL_TYPE_KEY = "roll_type"
    ROLLS_KEY="rolls"
    PLAYER_NAME_KEY = "player"
    PLAYER_ORDER_KEY = "player_order"
    INITIATIVE_KEY = "initiative_rolled"
    DICES_KEY = "dices"
    
    def __init__(self):
        self.unit_handler = data.UnitHandler()
        self.mul_parser = par.MulParser()
        self.players ={}
        self.player_order = []

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
        
        self.players.update(players)
        return players
    
    def roll_initiative(self, initiative_request):
        player_name = initiative_request[self.PLAYER_NAME_KEY]
        player = self.players[player_name]
        roll = rolls.roll_map[rolls.INITIATIVE](self,initiative_request)
        player.initiative, dices = roll.roll()
        
        answer = {}
        answer[self.PLAYER_NAME_KEY] = player_name
        answer[self.INITIATIVE_KEY] = player.initiative
        answer[self.DICES_KEY] = dices
        
        initiatives = [p.initiative for p in self.players.values()]
        
        if (all([i>0 for i in initiatives]) is True) and (len(initiatives) == len(set(initiatives))):
            initiatives = sorted([p for p in self.players.values()],key=lambda x: x.initiative,reverse=False)
            self.player_order = initiatives
            inits = [p.name for p in initiatives]
        else:
            inits = []
            if len(initiatives) != len(set(initiatives)):
                for player in self.players.values():
                    player.initiative = 0
        answer[self.PLAYER_ORDER_KEY] = inits
        return answer
            
        
    
    # def perform_rolls(self, roll_request):
    #     for roll_data in roll_request[self.ROLLS_KEY]:
    #         roll_type = roll_data[self.ROLL_TYPE_KEY]
    #         roll = rolls.roll_map[roll_type](self,roll_data)
    #         roll.roll()
        
    
    def players2dict(self,players=None):
        if players is None:
            players = self.players
        player_data = {key:val.to_dict() for key,val in players.items()}
        return player_data
    
class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = GameState()
        self.player_request = {"PLAYER_REQUEST":{"player1":{"Name":"Player","color":[0.5,0,0],"deployment_border":"S","forces":"test/samples/player1.mul"},
                                                 "player2":{"Name":"Player2","color":[0,0,0.5],"deployment_border":"N","forces":"test/samples/player2.mul"}}
                              }
        self.initiative_requests = [{'INITIATIVE_REQUEST': {'player': 'player1'}},{"INITIATIVE_REQUEST":{"player":"player2"}}]
        self.game.setup_players(self.player_request["PLAYER_REQUEST"])

    def test_roll_initiative(self):
        import random
        random.seed(0)
        answers = [self.game.roll_initiative(req['INITIATIVE_REQUEST']) for req in self.initiative_requests]
        breakpoint()
        self.assertEqual(answers[0]['player_order'],[])
        if answers[0]['initiative_rolled'] > answers[1]['initiative_rolled']:
            order = [answers[1]['player'],answers[0]['player']]
        else:
            order = [answers[0]['player'],answers[1]['player']]
        self.assertEqual(order,answers[1]['player_order'])
