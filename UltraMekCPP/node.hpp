// node.hpp - cpp node class header for Ultramek (compatible with MegaMek)

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


#ifndef __NODE_H__
#define __NODE_H__
#include <string>
#include<iostream>
using namespace std;

class Node
{
    int ID;
    int pos_x = -1;
    int pos_y = -1;
  public:
    Node ();
    Node (const int);
    Node (const int,const int,const int);
    Node (const string);
    Node (const Node&);
    int getID() const;
    int getPosX() const;
    int getPosY() const;
    bool operator< (const Node&);
    string toString() const;
};

int node_tests();

#endif //__NODE_H__
