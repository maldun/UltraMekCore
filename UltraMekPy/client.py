"""
client.py - Classes and Tools for clients and logic

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

import socket

PORT = 8563
IP = "127.0.0.1"
BUFFER_SIZE = 1024

class UDPClient:
    """
    Simple UDP client for testing stuff
    """
    PROTOCOL = socket.SOCK_DGRAM
    def __init__(self,port=PORT,ip=IP,standard_buffer_size=BUFFER_SIZE):
        self.port = port
        self.ip = ip
        self.standard_buffer_size = standard_buffer_size
        self.create_socket()

    def create_socket(self):
        self.socket = socket.socket(socket.AF_INET, self.PROTOCOL)

    def send(self,msg):
        self.socket.sendto(msg.encode(), (self.ip, self.port))

    def recieve(self,buffer_size=None,return_port_info=False):
        if buffer_size is None:
            buffer_size = self.standard_buffer_size
        data, (recv_ip, recv_port) = self.socket.recvfrom(buffer_size)
        if return_port_info is True:
            return data, (recv_ip, recv_port)
        else:
            return data

