// edge.hpp - cpp edge class header for Ultramek (compatible with MegaMek)

// Copyright © 2024 Stefan H. Reiterer.
// stefan.harald.reiterer@gmail.com 
// This work is under GPL v2 as it should remain free but compatible with MegaMek

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


#ifndef __EDGE_H__
#define __EDGE_H__
#include "node.hpp"
#include <string>

class Edge
{
  Node start;
  Node end;
  double weight;
  string DELIMITER = ",";
  public:
    Edge ();
    Edge (const Node,const Node, double);
    Edge (const string);
    int getStartID();
    int getEndID();
    Node getStartNode();
    Node getEndNode();
    double getWeight();
    string toString() const; 
};

int edge_tests();

#endif // __EDGE_H__
