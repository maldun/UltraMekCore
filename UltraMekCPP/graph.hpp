// graph.hpp - cpp graph class header for Ultramek (compatible with MegaMek)

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


#ifndef __GRAPH_H__
#define __GRAPH_H__

#include "node.hpp"
#include "edge.hpp"
#include <vector>

using namespace std;


class Graph
{
  long unsigned int nr_nodes;
  long unsigned int nr_edges;
  vector<Node>nodes;
  vector<Edge>edges;
  string NODE_KEY = "Nodes:";
  string EDGE_KEY = "Edges:";
  public:  
    Graph(vector<Node>, vector<Edge>);
    int parseNrObjects(string, string, string);
    bool isConsistent();
    Graph(const string);
    Graph();
    ~Graph();
    Graph(const int,const int,double**);
    vector<Node> getNodes();
    vector<Edge> getEdges();
    int getNrNodes();
    int getNrEdges();
    void writeToFile(string);
	bool hasEdge(Node,Node);
	bool hasNode(int);
	Edge getEdge(Node,Node);
    vector<int> shortest_path_ids(Node, Node);
    vector<Node> shortest_path(Node, Node);
    Node getNodeByPos(const int,const int);
    Node getNodeByID(const int);
    int createBoardEdge(Node,double**,int,int,int,int);
    
};

int get_shortest_index(vector<Node>, map<int,double>);
vector<int> shortest_path_dijkstra(Graph, Node, Node);

int graph_tests();

#endif // __GRAPH_H__
