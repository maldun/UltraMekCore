// node.cpp - cpp node class for Ultramek (compatible with MegaMek)

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


// Node Class
#include "node.hpp"
#include <sstream>
using namespace std;

Node::Node()
{
  ID = -1;
}

Node::Node(const int id)
{
  ID = id;
}

Node::Node(const string ids)
{
  stringstream id (ids);
  id >> ID;
}

Node::Node(const Node &n)
{
  ID = n.ID;
}

int Node::getID() const
{
  return ID;
}

bool Node::operator< (const Node& n)
{
  return (n.getID() < ID);
}

string Node::toString() const
{
  return to_string(ID);
}

// Node Tests
int testNodeCreation()
{
   Node node = Node(1);
   if(node.getID()!=1)
   {
      cout << "Node Creation Failed! " << endl;
      return 1;
   }

   Node node2 = Node("12");
   if(node2.getID()!=12)
   {
      cout << "Node Creation from String Failed! " << endl;
      return 1;
   }

   //cout << "Node Creation Success! " << endl;
   return 0;
}

int testNodeComparision()
{
  Node n(1);
  Node m(2);

  if(n < m and !(m < n))
  {
    cout << "Node comparision failed!" << endl;
    return 1;
  }
  //cout << "Node Comparison Success! " << endl;
  return 0;
}

int node_tests()
{
   if(testNodeCreation() != 0)
   {
      return 1; 
   }
   if(testNodeComparision() != 0)
   {
     return 1; 
   }
   cout << "Node tests passed!" << endl;
   return 0;
}
