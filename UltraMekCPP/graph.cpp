// graph.cpp - cpp graph class for Ultramek (compatible with MegaMek)

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

#include <algorithm>
#include <map>
#include <iostream>
#include <vector>
#include <fstream>
#include <string>
#include <sstream>
#include <stdexcept>
#include "node.hpp"
#include "edge.hpp"
#include "graph.hpp"

#define INFINITY 1.7E+308 // max what is possible

using namespace std;

Graph::Graph(vector<Node> nodess, vector<Edge> edgess)
{
  vector<Node> nodes_copy (nodess);
  nodes = nodes_copy;
  vector<Edge> edges_copy (edgess);
  edges = edges_copy;

  nr_nodes = nodess.size();
  nr_edges = edgess.size();
}

Graph::Graph()
{
  nodes = vector<Node>{};
  edges = vector<Edge>{};
  nr_nodes = 0;
  nr_edges = 0;
}

Graph::~Graph()
{
  nodes = vector<Node>();  
  edges = vector<Edge>();  
  nr_nodes = 0;
  nr_edges = 0;
}

Node Graph::getNodeByPos(const int x,const int y)
{
  for(Node n: nodes)
  {
     if(n.getPosX()==x and n.getPosY()==y)
     {
       return n;
     }
  }
  return Node();
}

Node Graph::getNodeByID(const int id)
{
  for(Node n: nodes)
  {
     if(n.getID()==id)
     {
       return n;
     }
  }
  return Node();
}

int Graph::createBoardEdge(Node curr,double **weights,int i, int j, int shift_x,int shift_y)
{
  Node m2 = this->getNodeByPos(i+shift_x,j+shift_y);
  if(m2.getID() != -1)
  {
     Edge e1 = Edge(curr,m2,weights[i+shift_x][j+shift_y]);
     edges.push_back(e1);
     return 0;
  }
  return 1;
}

Graph::Graph(const int dim_x, const int dim_y, double **weights)
{
    nodes = vector<Node>();
    edges = vector<Edge>();
    
    int counter = 0;
    for(int i=0;i<dim_x;i++)
    {
      for(int j=0;j<dim_y;j++)
      {
         Node n = Node(counter,i,j);
         nodes.push_back(n);
         counter++;
      }
    }

    for(int i=0;i<dim_x;i++)
    {
      for(int j=0;j<dim_y;j++)
      {
         Node m = this->getNodeByPos(i,j);
         this->createBoardEdge(m,weights,i,j,0,-1);
         this->createBoardEdge(m,weights,i,j,-1,0);
         this->createBoardEdge(m,weights,i,j,1,0);
         this->createBoardEdge(m,weights,i,j,-1,1);
         this->createBoardEdge(m,weights,i,j,0,1);
         this->createBoardEdge(m,weights,i,j,1,1);
      }
    }
}



int Graph::parseNrObjects(string filename, string key, string end_key)
{
  string line;
  ifstream file (filename);
  int nr_objs = -1;
  bool read_objs = false;
  
  if(not file.good())
  {
    throw invalid_argument("Error: File "+filename+" not found!");
  }

  if(file.is_open())
  {
    while (getline (file, line))
    {
      if(line == key)
      {
	read_objs = true;
	nr_objs = 0;
	continue;
      }
      if(read_objs)
      {
	if(line != "" and line != end_key) nr_objs++;
	if(line == end_key) read_objs = false;
      }
    }
  }
    return nr_objs;
}

Graph::Graph(const string filename)
{
  string line;
  ifstream file (filename);
  bool read_nodes = false;
  bool read_edges = false;
  int nr_objs = -1;

  nr_nodes = Graph::parseNrObjects(filename, NODE_KEY,EDGE_KEY);
  nr_edges = Graph::parseNrObjects(filename, EDGE_KEY, "");
  nodes = vector<Node>(nr_nodes, Node());
  edges = vector<Edge>(nr_edges, Edge());
  if(not file.good())
  {
    throw invalid_argument("Error: File " + filename + " not found!");
  }

  if(file.is_open())
  {
    while (getline (file, line))
    {
      if(line == NODE_KEY)
      {
	read_nodes = true;
	read_edges = false;
	nr_objs = 0;
	continue;
      }
      if(read_nodes and line != "")
      {
	nodes[nr_objs] = Node(line);
        nr_objs++;
      }
      if(line == EDGE_KEY)
      {
        nr_objs = 0;
	read_nodes = false;
	read_edges = true;
	continue;
      }
      if(read_edges and line != "")
      {
	edges[nr_objs] = Edge(line);
        nr_objs++;
      }
    }
  }
}

vector<Node> Graph::getNodes()
{
  return nodes;
}

vector<Edge> Graph::getEdges()
{
  return edges;
}

int Graph::getNrNodes()
{
  return nr_nodes;
}

int Graph::getNrEdges()
{
  return nr_edges;
}

void Graph::writeToFile(const string filename)
{
  ofstream new_file (filename);
  new_file << NODE_KEY << endl;
  for(long unsigned int i = 0; i < nr_nodes; i++)
  {
    new_file << nodes[i].toString() << endl;
  }
  new_file << EDGE_KEY << endl;
  for(long unsigned int i = 0; i < nr_edges; i++)
  {
    new_file << edges[i].toString() << endl;
  }
  
  new_file.close();
}

bool Graph::isConsistent()
{

  if(nr_nodes != nodes.size())
  {
    return false;
  }
  if(nr_edges != edges.size())
  {
    return false;
  }
  for(long unsigned int j=0; j < nr_edges; j++)
  {
    bool start_is_in_graph = false;
    bool end_is_in_graph = false;
    for(long unsigned int i=0; i < nr_nodes;i++)
    {
      if(nodes[i].getID() == edges[j].getStartID())
      {
        start_is_in_graph = true;
        break;
      }
    }
    if(start_is_in_graph == false) {
      return false;
    }
    for(long unsigned int i=0; i < nr_nodes;i++)
    {
      if(nodes[i].getID() == edges[j].getEndID())
      {
        end_is_in_graph = true;
        break;
      }
    }
    if(end_is_in_graph == false) {
      return false;
    }
  }
  // Check if ids are positive
  for(long unsigned int i=0; i < nr_nodes;i++)
  {
	  if(nodes[i].getID() < 0)
	  {
		  return false;
	  }
  }
  
  return true;
}

bool Graph::hasEdge(const Node start,const Node end)
{
	for(long unsigned int i=0; i < nr_edges;i++)
	{
	   Edge e = edges[i];
       if(start.getID() == e.getStartID() && end.getID() == e.getEndID())
	   {
		   return(true);
	   }
    }
	return(false);
}

bool Graph::hasNode(const int node_id)
{
	for(long unsigned int i=0; i < nr_nodes;i++)
	{
	   Node n = nodes[i];
       if(n.getID() == node_id)
	   {
		   return(true);
	   }
    }
	return(false);
}

Edge Graph::getEdge(const Node start,const Node end)
{
	for(long unsigned int i=0; i < nr_edges;i++)
	{
	   Edge e = edges[i];
       if(start.getID() == e.getStartID() && end.getID() == e.getEndID())
	   {
		   return(e);
	   }
    }
	throw out_of_range("Error: Edge not found!");
}

// Help function that returns ID with minimum distance
int get_shortest_index(vector<Node> queue, map<int,double> distances)
{
	vector<double> dists;
	for(unsigned long int i=0;i<queue.size();i++)
	{
	   Node q = queue[i];
	   double d = distances[q.getID()];
	   dists.push_back(d);
	}
	auto it = min_element(dists.begin(), dists.end());
	int min_index = distance(dists.begin(), it);
	return min_index;

}

// Shortest path algorithm by Dijkstra
vector<int> shortest_path_dijkstra(Graph graph, Node start, Node end)
{
	vector<Node> graph_nodes (graph.getNodes());
	map<int,double> distances;
	map<int,int> previous;
	vector<Node> queue;
	int start_id = start.getID();
	int end_id = end.getID();
	
	if(graph.isConsistent() == false)
	{
	  throw(invalid_argument("Error: Input Graph not valid!"));
	}
	long unsigned int nr_nodes = graph.getNrEdges();
	// Initialize helper data structures
	for(long unsigned int i=0; i < nr_nodes; i++)
	{
		Node n = graph_nodes[i];
		queue.push_back(n);
		int nid = n.getID();
		distances[nid] = INFINITY;
		previous[nid] = -1;
		if(nid == start_id)
		{
			distances[nid] = 0.0;
		}
	}
	// main algorithm
    while(queue.size() > 0)
	{
	     int ind = get_shortest_index(queue,distances);
		 Node u = queue[ind];
		 queue.erase(queue.begin()+ind);
		 // scanning
		 for(unsigned long int j = 0;j<queue.size();j++)
		 {
			 Node v = queue[j];
			 if(graph.hasEdge(u,v)==true)
			 {
				 Edge e = graph.getEdge(u,v);
				 double neu = distances[u.getID()] + e.getWeight();
				 if(neu < distances[v.getID()])
				 {
                     distances[v.getID()] = neu;
                     previous[v.getID()] = u.getID();
				 }
			 }
			 
		 }
	}
	// post processing (compute path)
	vector<int> path;
	int u_id = end_id;
	while(u_id > 0)
	{
	   path.insert(path.begin(),u_id);
	   u_id = previous[u_id];
	}
	
	return(path);
}

vector<int> Graph::shortest_path_ids(Node start, Node end)
{
   return shortest_path_dijkstra(*this,start,end); 
}

vector<Node> Graph::shortest_path(Node start, Node end)
{
   vector<int> path_ids = this->shortest_path_ids(start,end);
   vector<Node> path;
   for(int id : path_ids)
   {
     path.push_back(this->getNodeByID(id)); 
   }
   return path; 
}

// Graph tests
Node NIL = Node();
Edge NILE = Edge(NIL,NIL,-1.0);

Graph createTestGraph(int N, double w)
{
  int i, j;
  vector<Node> nodes (N,NIL);
  vector<Edge> edges (N*N,NILE);
  for(i=0;i<N;i++)
  {
    nodes[i] = Node(i);
  }

  int index = 0;
  for(i=0;i<N;i++)
  {
    for(j=0;j<N;j++)
    {
      if( i != j)
      {
        edges[index] = Edge(nodes[i], nodes[j], w);
        if(i!=nodes[i].getID() or i!=edges[index].getStartID())
	{
	  cout << "Graph Creation failed! ID mismatch!" << endl;
	}
	index++;
	
      }
    }	
  }
  Graph graph = Graph(nodes,edges);
  return graph;

}

int testGraphCreation()
{
  int N = 3;
  double w = 0.0;
  Graph graph = createTestGraph(N, w);

  vector<Node>new_nodes (graph.getNodes());
  if(new_nodes[0].getID() != 0)
  {
    cout << "Graph Nodes not correct!" << endl;
    return 1;
  }

  if(graph.getNrNodes() != N)
  {
    cout << "Graph Number of Nodes not correct!" << endl;
    return 1;
  }

  vector<Edge>new_edges (graph.getEdges());
  Node endi = new_edges[1].getEndNode();

  if(endi.getID() != 2)
  {
    cout << "Graph Edges Storage not correct!" << endl;
    return 1;
  }
  
  if(new_edges[1].getEndID() != 2)
  {
    cout << "Graph Edges not correct!" << endl;
    return 1;
  }

  if(graph.getNrEdges() != N*N)
  {
    cout << "Graph Number of Edges not correct!" << endl;
    return 1;
  }
  
  int dim_x = 3;
  int dim_y = 3;
  double **weights = new double*[dim_x];
  for(int k=0;k<dim_x;k++)
  {
    weights[k] = new double[dim_y];
  }
  double counter = 0;
  for(int i=0;i<dim_x;i++)
  {
    for(int j=0;j<dim_y;j++)
    {
      weights[i][j] = counter;
      counter+=1.0;
    }
  }
  Graph graph2 = Graph(dim_x,dim_y,weights);
  vector<Node> nodes2 = graph2.getNodes();
  vector<Edge> edges2 = graph2.getEdges();
  if(nodes2[0].getID() != 0 or edges2[0].getStartNode().getID()!=0 or graph2.getNodeByPos(0,1).getID() != edges2[1].getEndID() or graph2.getNodeByPos(1,0).getID() != edges2[0].getEndID())
  {
    cout << "Graph From Board not correct!" << endl;
    return 1;
  }
  if(graph2.isConsistent()==false)
  {
    cout << "Graph From Board not consistent!" << endl;
    return 1;
  }
  
  Graph graph3 = Graph();
  if(graph3.getNodes().size()!=0 or graph3.getEdges().size()!=0)
  {
    cout << "Empty Graph creation not correct!" << endl;
    return 1;
  }
  
  // All tests passed
  //cout << "Graph Creation Successful!" << endl;
  return 0;
}

const string TEST_FOLDER = "test/testgraphs/";

int testGraphParsing()
{
  int N = 3;
  double w = 0;
  Graph graph = createTestGraph(N, w);
  int nr_nodes = graph.parseNrObjects(TEST_FOLDER + "testgraph0.txt", "Nodes:","Edges:");
  if(nr_nodes != 4)
  {
    cout << "Parsed nodes in testgraph0 and failed!" << endl;
    return 1;
  }
  nr_nodes = graph.parseNrObjects(TEST_FOLDER + "testgraph1.txt", "Nodes:","Edges:");
  if(nr_nodes != 5)
  {
    cout << "Parsed nodes in testgraph1 and failed!" << endl;
    return 1;
  }
  int nr_edges = graph.parseNrObjects(TEST_FOLDER+"testgraph1.txt", "Edges:", "");
  if(nr_edges != 6)
  {
    cout << "Parsed edges in testgraph1 and failed!" << endl;
    return 1;
  }

  Graph graph_from_file = Graph(TEST_FOLDER+"testgraph1.txt");
  if(graph_from_file.getNrNodes() != 5)
  {
    cout << "Parsed Graph from testgraph1 and failed (wrong number of nodes)!" << endl;
    return 1;
  }

  if(graph_from_file.getNrEdges() != 6)
  {
    cout << "Parsed Graph from testgraph1 and failed (wrong number of edges)!" << endl;
    return 1;
  }

  vector<Node> test_nodes (graph_from_file.getNodes());
  for(int i;i < graph_from_file.getNrNodes(); i++)
  {
    if(test_nodes[i].getID() > 5 or test_nodes[i].getID() < 1)
    {
      cout << "Parsed Graph from testgraph1 and failed (wrong node)!" << endl;
      return 1;
    }
  }
  vector<Edge> test_edges (graph_from_file.getEdges());
  for(int i=0; i < graph_from_file.getNrEdges(); i++)
  {
    if(test_edges[i].getWeight() > 3.0 or test_edges[i].getWeight() < 1.0)
    {
      cout << "Parsed Graph from testgraph1 and failed (wrong edge)!" << endl;
      return 1;
    }
  }
  
  //cout << "Parser tests passed!" << endl;
  return 0;
}

int testGraphConsistency()
{
  Graph graph_from_file = Graph(TEST_FOLDER+"testgraph12.txt");
  if(graph_from_file.isConsistent()!=true)
  {
    cout << "Graph.isConsistent failed on correct input!" << endl;
    return 1;
  }
  Graph graph_from_file_false = Graph(TEST_FOLDER+"testgraph13.txt");
  if(graph_from_file_false.isConsistent()!=false)
  {
    cout << "Graph.isConsistent failed on wrong input!" << endl;
    return 1;
  }
  Graph graph_from_file_neg = Graph(TEST_FOLDER+"testgraph14.txt");
  if(graph_from_file_neg.isConsistent()!=false)
  {
    cout << "Graph.isConsistent failed on negative id!" << endl;
    return 1;
  }
  
  //cout << "Consistency tests passed!" << endl;
  return 0;
}

int testToStringMethods()
{
  
  Node tester = Node(5);
  if(tester.toString() != "5")
  {
    cout << "Node.toString failed!" << endl;
    return 1;
  }

  string edge_string = "1,2,3.0";
  Edge test_edge(edge_string);
  if(test_edge.toString() != edge_string)
  {
    cout << "Edge.toString failed!" << endl;
    return 1;
  }

  // test Graph 2 File
  Graph graph1 = Graph(TEST_FOLDER+"testgraph1.txt");
  graph1.writeToFile(TEST_FOLDER+"testgraph11.txt");
  Graph graph11 = Graph(TEST_FOLDER+"testgraph11.txt");
  if(graph1.getNrNodes() != graph11.getNrNodes())
  {
    cout << "Graph.writeToFile failed!" << endl;
    return 1;
  }
  
  //cout << "toString tests passed!" << endl;
  return 0;
}

int testHasEdge()
{
  Graph graph = Graph(TEST_FOLDER+"testgraph1.txt");
  Node start = Node(1);
  Node end = Node(3);
  bool result1 = graph.hasEdge(start,end);
  if(result1 == false)
  {
	  return 1;
  }
  Node start1 = Node(1);
  Node end1 = Node(4);
  bool result2 = graph.hasEdge(start1,end1);
  if(result2 == true)
  {
	  return 1;
  }
  //cout << "hasEdge tests passed!" << endl;
  return 0;
}

int testHasNode()
{
  Graph graph = Graph(TEST_FOLDER+"testgraph1.txt");
  
  bool result1 = graph.hasNode(1);
  if(result1 == false)
  {
	  return 1;
  }
  bool result2 = graph.hasNode(10);
  if(result2 == true)
  {
	  return 1;
  }
  //cout << "hasNode tests passed!" << endl;
  return 0;
}

int testGetNodeFromPos()
{
   Node n = Node(0,1,1);
   Node m = Node(1,1,2);
   Edge e = Edge(n,m,0.0);
   vector<Node> nn{n,m};
   vector<Edge> ee{e};
   Graph g = Graph(nn,ee);
   
   
   if(!(g.getNodeByPos(1,1).getID()==0 && g.getNodeByPos(1,2).getID()==1 && g.getNodeByPos(3,1).getID()==-1))
  {
	cout << "GetNodeFromPos Test failed!" << endl;
	return 1;
  }
   
   return 0;
}

int testGetNodeFromID()
{
   Node n = Node(0,1,1);
   Node m = Node(1,1,2);
   Edge e = Edge(n,m,0.0);
   vector<Node> nn{n,m};
   vector<Edge> ee{e};
   Graph g = Graph(nn,ee);
   
   
   if(!(g.getNodeByID(0).getID()==0 && g.getNodeByID(1).getID()==1 && g.getNodeByID(3).getID()==-1))
  {
	cout << "GetNodeFromID Test failed!" << endl;
	return 1;
  }
   
   return 0;
}

int testDijkstra()
{
	
  Graph graph = Graph(TEST_FOLDER + "testgraph1.txt");
  Node start = Node(1);
  Node end = Node(3);
  vector<int> result = shortest_path_dijkstra(graph,start,end);
  if(!(result[0] == 1 && result[1] == 3))
  {
	cout << "Dijkstra test: Wrong path!" << endl;
	return 1;
  }
  start = Node(1);
  end = Node(5);
  result = shortest_path_dijkstra(graph,start,end);
  if(!(result[0] == 1 && result[1] == 3 && result[2] == 5))
  {
	cout << "Dijkstra test: Wrong path!" << endl;
	return 1;
  }
  //cout << "Input Graph (inf form of Edges):" << endl;
  vector<Edge> edges = graph.getEdges();
  vector<int> expected = {1,3,5};

  // cout << '(';
  // for(long unsigned int i=0;i<edges.size();i++)
  // {
	 //  cout << '(' << edges[i].getStartID() << ',' << edges[i].getEndID() <<
	 //  ',' << edges[i].getWeight() <<  ')' << ',';	  
  // }
  // cout << ')'  << endl;
  //cout << "Path: (";
  for(long unsigned int i=0;i < result.size();i++)
  {
	  //cout << result[i] << ',';
      if(expected[i] != result[i])
      {
         return 1; 
      }
  }
  //cout << ')' << endl;
  //cout << "Dijkstra tests passed!" << endl;
  return 0;
}

int testShortestPath()
{
  Graph graph = Graph(TEST_FOLDER + "testgraph1.txt");
  Node start = Node(1);
  Node end = Node(3);
  vector<int> result = graph.shortest_path_ids(start,end);
  vector<int> expected = {1,3,5};
  for(long unsigned int i=0;i < result.size();i++)
  {
      if(expected[i] != result[i])
      {
         return 1; 
      }
  }
  vector<Node> resultn = graph.shortest_path(start,end);
  for(long unsigned int i=0;i < result.size();i++)
  {
      if(expected[i] != resultn[i].getID())
      {
         return 1; 
      }
  }
  
  
  return 0;
  
}
int graph_tests()
{
  if(testGraphCreation() != 0)
     {return 1;}
  if(testGraphParsing() != 0)
   {return 1;}
  if(testToStringMethods() != 0)
   {return 1;}
  if(testGraphConsistency() != 0)
   {return 1;}
  if(testHasEdge() != 0)
   {return 1;}
  if(testHasNode() != 0)
   {return 1;}
  if(testDijkstra() != 0)
   {return 1;}
  if(testShortestPath() != 0)
   {return 1;}
  if(testGetNodeFromPos() != 0)
   {return 1;}
  if(testGetNodeFromID() != 0)
   {return 1;}
   

  cout << "Graph tests passed! " << endl;
  return 0;
}
