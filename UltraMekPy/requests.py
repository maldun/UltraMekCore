"""
requests.py - Classes and Tools for request handling (compatible with MegaMek)

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

import json
import os 

from . import boards
from . import functions as fn

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(DIR_PATH,"requests.json"),'r') as fp:
    REQUEST_MAP = json.load(fp)

class RequestProcessor:

    def __init__(self):
        cls_name = self.__class__.__name__
        self.request_type = fn.split_camel_case(cls_name)
        self.request_type = [word.upper() for word in self.request_type]
        self.request_type = "_".join(self.request_type)

    def get_request(self, dic):
        return dic[self.request_type] 
    
    def __call__(self, dic):
        request = dic
        #request = self.get_request(dic)

        result =  self._process(request)
        return result


class BoardRequest(RequestProcessor):

    def _process(self, request):
        fname = request['filename']
        b = boards.Board(fname)
        j = b.to_flat_dict()
        return j

rtypes = [BoardRequest]

request_type_map = {}
for rtype in rtypes:
    r = rtype()
    request_type_map[r.request_type] = r
