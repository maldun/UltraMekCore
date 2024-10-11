// ultramek_gd.cpp - Ultramek cpp bindings for godot (compatible with MegaMek)

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

#include "ultramek_gd.h"
#include <godot_cpp/core/class_db.hpp>

using namespace godot;

UltraMekGD::UltraMekGD()
{
  mek = UltraMek();
}

UltraMekGD::~UltraMekGD()
{
}


void UltraMekGD::set_unit_length(double l)
{
  mek.set_unit_length(l);
}

double UltraMekGD::get_unit_length()
{
  return mek.get_unit_height();
}

void UltraMekGD::set_unit_height(double l)
{
  mek.set_unit_height(l);
}

double UltraMekGD::get_unit_height()
{
  return mek.get_unit_height();
}

Array UltraMekGD::create_grid_centers(int dim_x, int dim_y)
{
  Array centers;
  double ***center_matrix = mek.create_grid_centers(dim_x, dim_y);
  for(int i=0;i<dim_x;i++)
  {
    Array content;
    for(int j=0;j<dim_y;j++)
    {
      Vector2 c(center_matrix[i][j][0],center_matrix[i][j][1]);
      content.push_back(c);
    }
    centers.push_back(content);
  }
  return centers; 
}

int UltraMekGD::point_in_hex_with_center(Vector2 x,Vector2 center)
{
  double xp[2] = {0,0};
  double cp[2] = {0,0};
  xp[0]=x[0];xp[1]=x[1];
  cp[0]=center[0];cp[1]=center[1];
  return mek.point_in_hex_with_center(xp,cp,mek.get_unit_length());
}

Array UltraMekGD::create_hex_vertices(double pos_x,double pos_y,double length)
{
  Array verts;
  double **vert_matrix = mek.create_hex_vertices(pos_x,pos_y,length);
  for(int i=0;i<HEX+1;i++)
  {
    Vector2 c(vert_matrix[i][0],vert_matrix[i][1]);
    verts.push_back(c);
  }
  return verts; 
}

Array UltraMekGD::create_vertex_order()
{
  Array order;
  int *order_vec = mek.create_vertex_order();
  for(int i=0;i<12*HEX;i++)
  {
    order.push_back(order_vec[i]);
  }
  return order; 
}


double UltraMekGD::get_hex_diameter()
{
  int result = mek.get_hex_diameter();
  return result;
}

double UltraMekGD::doubling(double x)
{
  double result = mek.doubling(x);
  return result;
}

double UltraMekGD::compute_euclidean(double x,double y)
{
    return mek.compute_euclidean(x,y);
}

Array UltraMekGD::create_board_graph(int dim_x,int dim_y,TypedArray<double> weights)
{
  double **wmatrix = new double*[dim_x];
  for(int i=0;i<dim_x;i++)
  {
    wmatrix[i] = new double[dim_y];
    for(int j=0;j<dim_y;j++)
    {
      wmatrix[i][j] = weights[i + dim_x*j];
    }
  }
  int **ids = mek.create_board_graph(dim_x,dim_y,wmatrix); 
  Array result;
  for(int i=0;i<dim_x;i++)
  {
    Array row = {};
    for(int j=0;j<dim_y;j++)
    {
      row.push_back(ids[i][j]);
    }
    result.push_back(row);
  }
  return result;
}

Array UltraMekGD::compute_shortest_walk_ids(int start_id,int target_id)
{
  Array path;
  path.push_back(start_id);
  int *path_arr = mek.compute_shortest_walk_ids(start_id,target_id);
  int len = sizeof(path_arr)/sizeof(int);
  for(int i=0;i<len;i++)
  {
    path.push_back(path_arr[i]); 
  }
  return path;
  
}

void UltraMekGD::_bind_methods()
{
    ClassDB::bind_method(D_METHOD("get_hex_diameter"), &UltraMekGD::get_hex_diameter);
    ClassDB::bind_method(D_METHOD("set_unit_length", "value"), &UltraMekGD::set_unit_length,
			 DEFVAL(1));
    ClassDB::bind_method(D_METHOD("set_unit_height", "value"), &UltraMekGD::set_unit_height,
			 DEFVAL(1));
    ClassDB::bind_method(D_METHOD("doubling", "value"), &UltraMekGD::doubling, DEFVAL(1));
    ClassDB::bind_method(D_METHOD("compute_euclidean", "x", "y"), &UltraMekGD::compute_euclidean, DEFVAL(1),DEFVAL(1));
    ClassDB::bind_method(D_METHOD("get_unit_length"), &UltraMekGD::get_unit_length);
    ClassDB::bind_method(D_METHOD("get_unit_height"), &UltraMekGD::get_unit_height);
    ClassDB::bind_method(D_METHOD("create_grid_centers", "dim_x", "dim_y"),
			 &UltraMekGD::create_grid_centers, DEFVAL(1),DEFVAL(1));
    ClassDB::bind_method(D_METHOD("create_hex_vertices", "pos_x", "pos_y","length","height"),
			 &UltraMekGD::create_hex_vertices,
			 DEFVAL(0),DEFVAL(0),DEFVAL(1),DEFVAL(1));
    ClassDB::bind_method(D_METHOD("create_vertex_order"), &UltraMekGD::create_vertex_order);
    ClassDB::bind_method(D_METHOD("create_board_graph", "dim_x", "dim_y", "weights"),
			 &UltraMekGD::create_board_graph, DEFVAL(1),DEFVAL(1),DEFVAL(1));
    ClassDB::bind_method(D_METHOD("compute_shortest_walk_ids", "start_id", "end_id"), &UltraMekGD::compute_shortest_walk_ids, DEFVAL(1),DEFVAL(1));
    ClassDB::bind_method(D_METHOD("point_in_hex_with_center", "x", "center"), &UltraMekGD::point_in_hex_with_center, DEFVAL(1),DEFVAL(1));
}
