"""
server.py - Classes and Tools for servers and logic

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

import json
import socket
import socketserver
from .constants import NL

from . import requests as req
from . import game

class UltraMekHandler(socketserver.StreamRequestHandler):
    """
    TCP Server for UltraMek for managing games and doing stuff 
    """

    def setup(self):
        super().setup()
        self.setup_game_state()
    
    def setup_game_state(self):
        self.game_state = game.GameState()
    
    def request_processor(self, request):
        """
        Takes a request dictionary and handles it accordingly
        """
        result = {}
        for request_type, request_data in request.items():
            res = req.request_type_map[request_type](request_data,self.game_state)
            result[request_type] = res
        return json.dumps(result) + NL
    
    def handle(self): # must be implemented
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        self.data = self.rfile.readline().strip()
        print("{} sent:".format(self.client_address[0]))
        request = json.loads(self.data.decode())
        print(request)
        result = self.request_processor(request)
        #print(self.data)
        # Likewise, self.wfile is a file-like object used to write back
        # to the client
        print("Answer: ", result)
        #self.wfile.write(self.data.upper())
        self.wfile.write(result.encode())
        #self.wfile.write("Help!\n".encode())


