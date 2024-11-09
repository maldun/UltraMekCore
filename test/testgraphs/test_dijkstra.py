from networkx import *
from numpy import *
nodes = []
counter = 0
dim_x = 3
dim_y = 3
weights = []
for k in range(dim_y):
    w = []
    for l in range(dim_x):
        nodes.append((counter,l,k))
        w.append(counter)
        counter +=1
    weights.append(w)

weights = array(weights)

G = DiGraph()
for n in nodes:
    G.add_node(n)

def get_node_by_pos(graph,i,j):
    for node in graph.nodes:
        if node[1] == i and node[2] == j:
            return node
        
    return None

def create_board_edge(graph,curr,weights,i,j,shift_x,shift_y):
  m2 = get_node_by_pos(graph,i+shift_x,j+shift_y);
  if(m2 != None):
     graph.add_edge(curr,m2,weight=weights[i+shift_x][j+shift_y])
     return 0;
  return 1;

def create_board_graph(dim_x,dim_y,weights):
    graph = DiGraph()
    counter = 0
    for i in range(dim_y):
        for j in range(dim_x):
            graph.add_node((counter,j,i))
            counter +=1
    
    for i in range(dim_x):
        for j in range(dim_y):
            m = get_node_by_pos(graph,i,j)
            if i%2!=0:
               create_board_edge(graph,m, weights,i,j,0,-1);
               create_board_edge(graph, m,weights,i,j,-1,0);
               create_board_edge(graph, m,weights,i,j,1,0);
               create_board_edge(graph, m,weights,i,j,-1,1);
               create_board_edge(graph, m,weights,i,j,0,1);
               create_board_edge(graph, m,weights,i,j,1,1);
            else:
              create_board_edge(graph, m,weights,i,j,0,1);
              create_board_edge(graph, m,weights,i,j,-1,0);
              create_board_edge(graph, m,weights,i,j,1,0);
              create_board_edge(graph, m,weights,i,j,-1,-1);
              create_board_edge(graph, m,weights,i,j,0,-1);
              create_board_edge(graph, m,weights,i,j,1,-1);
    return graph

    
G = create_board_graph(dim_x,dim_y,weights)

print(nodes)

print(shortest_path(G,nodes[0],nodes[-1]))
weights[1][1] = 20
print(weights)
G2 = create_board_graph(dim_x,dim_y,weights)
nodes = list(G2.nodes)
print(shortest_path(G2,nodes[0],nodes[-1],weight="weight"))

G3 = create_board_graph(dim_x,dim_y,weights.T)
print(shortest_path(G3,nodes[0],nodes[-1],weight="weight"))
