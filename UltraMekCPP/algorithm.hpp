#ifndef __ALGORITHM_H__
#define __ALGORITHM_H__

#include "node.hpp"
#include "edge.hpp"
#include "graph.hpp"
#include <vector>

#define INFINITY 1.7E+308 // max what is possible

vector<int> shortest_path_dijkstra(Graph graph, Node start, Node end);

#endif //__ALGORITHM_H__
