# -*- coding: utf-8 -*-
"""
__main__.py - Running of the client

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
import socketserver
import socket

from . import server
from . import game

with open("UltraMekPy/config.json",'r') as conf:
    conn_dict = json.load(conf)['connection']


host, port = conn_dict['ip'], conn_dict['port']
with socketserver.TCPServer((host,port), server.UltraMekHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.allow_reuse_address=True
        server.serve_forever(poll_interval=0.5)
        server.request_queue_size=40
        server.timeout = None

