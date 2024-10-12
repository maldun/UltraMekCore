
// ultramek.cpp - cpp library for Ultramek (compatible with MegaMek)

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

#include "ultramek.hpp"
#include "geometry.hpp"
#include "graph.hpp"
#include <vector>
#include <cmath>
#include <array>

UltraMek::UltraMek()
{
  unit_length = 1.0;
  unit_height = 1.0;
  hex_dim_x = 0;
  hex_dim_y = 0;
  grid_centers = nullptr;
  hex_ids = nullptr;
  board = Graph();
}

UltraMek::~UltraMek()
{
    // do nothing (yet)
   if(grid_centers != nullptr)
   {
      delete grid_centers;
      grid_centers = nullptr;
   }
}


double ***UltraMek::create_grid_centers(int dim_x, int dim_y)
{
  double ***matrix = compute_grid_centers(dim_x,dim_y,unit_length);
  return matrix;
}

double **UltraMek::create_hex_vertices(double pos_x, double pos_y, double length)
{
  double **matrix = compute_hex_vertices(pos_x,pos_y,length);
  return matrix;     
}

int *UltraMek::create_vertex_order()
{
  int *order = compute_vertex_order();
  return order;     
}

// for test purposes
double UltraMek::compute_euclidean(double x,double y)
{
  vector<double> vec{x,y};
  return sqrt(vec[0]*vec[0] + vec[1]*vec[1]);
}

int **UltraMek::create_board_graph(int dim_x,int dim_y,double** weights)
{
   board = Graph(dim_x,dim_y,weights);
   int **id_matrix = initialize_2d_matrix<int>(dim_x, dim_y);
   for(Node node : board.getNodes())
   {
      int X = node.getPosX(); 
      int Y = node.getPosY();
      id_matrix[X][Y] = node.getID();
      
   }
   return id_matrix;
}

int *UltraMek::compute_shortest_walk_ids(int start_id,int target_id)
{
  
   Node s = board.getNodeByID(start_id);
   if(s.getID()==-1)
   {
      return {0}; 
   }
   Node t = board.getNodeByID(target_id);
   if(t.getID()==-1)
   {
      return {0}; 
   }
   vector<int> path = board.shortest_path_ids(s,t);
   int *result = new int[path.size()+2];
   result[0] = path.size()+1;
   result[1] = s.getID();
   for(long unsigned int k=0;k<path.size();k++)
   {
     result[k+2] = path[k];
   }
   return result;
}

int UltraMek::point_in_hex_with_center(double *x,double *center,double unit_length)
{
  return point_inside_hex_with_center(x,center,unit_length);
}

void UltraMek::setup_grid_centers()
{
  if(hex_dim_x > 0 and hex_dim_y > 0)
  {grid_centers = create_grid_centers(hex_dim_x,hex_dim_y);}
  
}

void UltraMek::setup_board_geometry(unsigned int dim_x, unsigned int dim_y,double unit_length=1.0,double unit_height=0.5)
{
  hex_dim_x = dim_x;
  hex_dim_y = dim_y;
  set_unit_length(unit_length);
  set_unit_height(unit_height);
  setup_grid_centers();
}

int *UltraMek::compute_board_hex_for_point(double* p)
{
  int *result = new int[2];
  result[0] = -1;result[1] = -1;
  
  if(grid_centers==nullptr or unit_length <= 0)
  {return result;}
  
  result = point_on_grid(p,hex_dim_x,hex_dim_y,grid_centers,unit_length);
  
  return result;
}



//////////////////////////////////////// TESTS /////////////////////////////////////////////////////


int test_doubling()
{
  UltraMek mek = UltraMek();
  if(mek.doubling(2.0) != 4.0){ return 1;}

  return 0;
}

int test_compute_euclidean()
{
   UltraMek mek = UltraMek();
   if(mek.compute_euclidean(3.0,4.0) != 5.0){ return 1;}
   return 0;
}

int test_unit_length()
{
  UltraMek mek = UltraMek();
  if(mek.get_unit_length() != 1.0){ return 1;}
  mek.set_unit_length(2.0);
  if(mek.get_unit_length() != 2.0){ return 1;}

  return 0;
}

int test_unit_height()
{
  UltraMek mek = UltraMek();
  if(mek.get_unit_height() != 1.0){ return 1;}
  mek.set_unit_height(2.0);
  if(mek.get_unit_height() != 2.0){ return 1;}

  return 0;
}

int test_hex_diameter()
{
  UltraMek mek = UltraMek();
  if(mek.get_hex_diameter() != 2.0){ return 1;}
  mek.set_unit_length(2.0);
  if(mek.get_hex_diameter() != 4.0){ return 1;}

  return 0;
}

int test_graph_creation()
{
  UltraMek mek = UltraMek();
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
  mek.create_board_graph(dim_x,dim_y,weights);
  return 0;
}



int test_point_inside_hex_um()
{
  double center[2] = {0,0};
  double unit_length = 1.0;
  double x[2] = {0,0};
  UltraMek mek = UltraMek();
  if(mek.point_in_hex_with_center(x,center,unit_length) != 1)
   {return 1;}
  x[0] = 0.1; x[1] = 0.1;
  if(mek.point_in_hex_with_center(x,center,unit_length) != 1)
   {return 1;}
  x[0] = 100.0; x[1] = 0.1;
  if(mek.point_in_hex_with_center(x,center,unit_length) != 0)
   {return 1;}
   
   return 0;
}

int test_geometry_setup()
{
  
  double unit_length = 1.0;
  double unit_height = 0.5;
  unsigned int dim_x = 16;
  unsigned int dim_y = 17;
  
  UltraMek mek = UltraMek();
  mek.setup_board_geometry(dim_x,dim_y,unit_length);
  if(mek.get_unit_length() != unit_length){return 1;}
  if(mek.get_unit_height() != unit_height){return 1;}
  if(mek.get_dim_x() != dim_x){return 1;}
  if(mek.get_dim_y() != dim_y){return 1;}
  double ***centers = mek.get_grid_centers();
  double ***centersX = mek.create_grid_centers(dim_x,dim_y);
  for(unsigned int i=0;i<dim_x;i++)
  {
     for(unsigned int j=0;j<dim_y;j++)
     {
       if(centers[i][j][0] != centersX[i][j][0] and centers[i][j][1] != centersX[i][j][1])
       {
         return 1;
       }
     }
  }
  return 0;
}

int test_compute_shortest_walk_ids()
{
  UltraMek mek = UltraMek();
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
  mek.create_board_graph(dim_x,dim_y,weights);
  int *path = mek.compute_shortest_walk_ids(0,8);
  int expected_path[4] = {0,3,4,8};
  for(int i=0;i<path[0];i++)
  {
    //cout << "Shortest Board Path: " << path[i+1] << endl; 
    if(path[i+1]!=expected_path[i])
    {
      return 1; 
    }
  }
  counter = 0;
  for(int i=0;i<dim_x;i++)
  {
    for(int j=0;j<dim_y;j++)
    {
      weights[i][j] = counter;
      counter+=1.0;
    }
  }
  weights[1][1]=20;
  int expected_path2[5] = {0,3,6,7,8};
  mek.create_board_graph(dim_x,dim_y,weights);
  path = mek.compute_shortest_walk_ids(0,8);
  for(int i=0;i<path[0];i++)
  {
    //cout << "Shortest Board Path: " << path[i+1] << endl; 
    if(path[i+1]!=expected_path2[i])
    {
      return 1; 
    }
  }
  counter = 0;
  for(int i=0;i<dim_x;i++)
  {
    for(int j=0;j<dim_y;j++)
    {
      weights[j][i] = counter;
      counter+=1.0;
    }
  }
  weights[1][1]=20;
  int expected_path3[4] = {0,1,5,8};
  mek.create_board_graph(dim_x,dim_y,weights);
  path = mek.compute_shortest_walk_ids(0,8);
  for(int i=0;i<path[0];i++)
  {
    //cout << "Shortest Board Path: " << path[i+1] << endl; 
    if(path[i+1]!=expected_path3[i])
    {
      return 1; 
    }
  }
  return 0;
}

int test_compute_board_hex_for_point()
{
  double unit_length = 1.0;
  unsigned int dim_x = 16;
  unsigned int dim_y = 17;
  
  
  UltraMek mek = UltraMek();
  mek.setup_board_geometry(dim_x,dim_y,unit_length);
  double ***centers = mek.get_grid_centers();
  double p[2] = {5,-20};
  int *result = mek.compute_board_hex_for_point(p);
  if(mek.point_in_hex_with_center(p,centers[result[0]][result[1]],unit_length)!=1)
  {return 1;}
  
  return 0;
}

int ultra_mek_tests()
{
  if(test_doubling()!=0)
  {
    cout << "Test Doubling failed!" << endl;
    return 1;
  }

  if(test_hex_diameter()!=0)
  {
    cout << "Test hex diameter failed!" << endl;
    return 1;
  }

  if(test_unit_length()!=0)
  {
    cout << "Test unit_length failed!" << endl;
    return 1;
  }

  if(test_unit_height()!=0)
  {
    cout << "Test unit_height failed!" << endl;
    return 1;
  }
  
  if(test_compute_euclidean()!=0)
  {
    cout << "Test compute euclidean failed!" << endl;
    return 1;
  }
    if(test_graph_creation()!=0)
  {
    cout << "Test graph creation failed!" << endl;
    return 1;
  }
  
  if(test_compute_shortest_walk_ids()!=0)
  {
    cout << "Test path finding (ids) failed!" << endl;
    return 1;
  }
   if(test_point_inside_hex_um()!=0)
  {
    cout << "Test if point inside hex failed!" << endl;
    return 1;
  }
  if(test_geometry_setup()!=0)
  {
    cout << "Test geometry creation!" << endl;
    return 1;
  }
  
  cout << "UkltraMek tests passed!" << endl;
  return 0;
}
