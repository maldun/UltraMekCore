#include <iostream>
#include <vector>
#include <fstream>
#include <string>
#include <sstream>
#include <stdexcept>
#include <map>
#include <algorithm>
#include "node.hpp"
#include "edge.hpp"
#include "graph.hpp"
#include "algorithm.hpp"

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