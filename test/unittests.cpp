﻿// unittests.cpp - cpp unittests for Ultramek (compatible with MekHQ)

// Copyright © 2024 Stefan H. Reiterer.
// stefan.harald.reiterer@gmail.com 
// This work is under GPL v2 as it should remain free but compatible with MekHQ

// This program is free software; you can redistribute it and/or
// modify it under the terms of the GNU General Public License
// as published by the Free Software Foundation; either version 2
// of the License, or (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with this program; if not, write to the Free Software
// Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

#include "unittests.hpp"

int main(int argc, char *argv[])
{
    if(geometry_tests() != 0)
    {
      cout << "Geometry Tests failed" << endl;
      throw runtime_error("Error: Geometry Test Failed!");
    }
    if(node_tests() != 0)
    {
      cout << "Node Tests failed" << endl;
      throw runtime_error("Error: Node Test Failed!");
    }
    if(edge_tests() != 0)
    {
      cout << "Edge Tests failed" << endl;
      throw runtime_error("Error: Edge Test Failed!");
    }
    if(graph_tests() != 0)
    {
      cout << "Graph Tests failed" << endl;
      throw runtime_error("Error: Graph Test Failed!");
    }
    if(ultra_mek_tests() != 0)
    {
      cout << "UltraMek Tests failed" << endl;
      throw runtime_error("Error: Ultramek Test Failed!");
    }
    cout << "All tests passed!" << endl;
    return 0;
} 
