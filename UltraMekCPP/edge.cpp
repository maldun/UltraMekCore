// edge.cpp - cpp edge class for Ultramek (compatible with MekHQ)

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


#include <vector>
#include <string>
#include <iostream>
#include <sstream>
#include <iomanip>
#include "edge.hpp"
#include "node.hpp"
#include "edge.hpp"
using namespace std;

Edge::Edge()
{
  start = Node();
  end = Node();
  weight = -1.0;
}

Edge::Edge(const Node s,const Node e, double w)
{
  start = s;
  end = e;
  weight = w;
}

Edge::Edge(const string line)
{
  vector<string> vals (3,"");
  int delims = 0;
  string s = "";
  for(string::size_type i = 0; i < line.size(); i++)
  {
    s = string(1, line[i]);
    if(s != "" and s != DELIMITER)
    {
      vals[delims] += s;
    }
    if(s == DELIMITER)
    {
      delims++;
      continue;
    } 
  }

  
  start = Node(vals[0]);
  end = Node(vals[1]);
  weight = stod(vals[2]);
  
  vals.clear();
  vals = vector<string>();

}

int Edge::getStartID()
{
  return start.getID(); 
}

int Edge::getEndID()
{
  return end.getID(); 
}

Node Edge::getStartNode()
{
  return start;
}

Node Edge::getEndNode()
{
  return end;
}

double Edge::getWeight()
{
  return weight;
}

string Edge::toString() const
{
  stringstream stream;
  stream << std::fixed << std::setprecision(1) << weight;
  string w = stream.str();
  return start.toString()+DELIMITER+end.toString()+DELIMITER+w;
}

// Edge Tests
int testEdgeCreation()
{

  int id1 = 1;
  int id2 = 2;
  Node n1 = Node(id1);
  Node n2 = Node(id2);
  double w = 2.0;
  Edge edge = Edge(n1, n2, w);

  if((edge.getStartID()!=id1) or (edge.getEndID()!=id2) or edge.getWeight()!=w)
   {
      cout << "Edge Creation Failed! " << endl;
      return 1; 
   }

  Node m1 = edge.getStartNode();
  Node m2 = edge.getEndNode();
  if(m1.getID()!=id1 or m2.getID()!=id2)
  {
     cout << "Edge Creation Failed! (Wrong nodes)" << endl;
     return 1; 
  }

  Edge def = Edge();
  if(def.getWeight() != -1.0 or def.getEndID() != -1)
  {
    cout << "Edge Creation Failed! (Default Constructor)" << endl;
     return 1;
  }

  Edge str = Edge("1,2,3.0");
  if(str.getWeight() != 3.0 or str.getStartID() != 1 or str.getEndID() != 2)
  {
    cout << "Edge Creation Failed! (String Constructor)" << endl;
     return 1;
  }

  //cout << "Edge Creation Success! " << endl;
  return 0;
}

int edge_tests()
{
   if(testEdgeCreation()!=0)
   {
     return 1; 
   }
   cout << "Edge tests passed! " << endl;
   return 0;
}
