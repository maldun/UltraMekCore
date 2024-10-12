// ultramek.hpp - cpp library header for Ultramek (compatible with MegaMek)

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

#ifndef ULTRAMEK_H
#define ULTRAMEK_H

#include "helpers.hpp"
#include "geometry.hpp"
#include "graph.hpp"

class UltraMek
{
  double unit_length;
  double unit_height;
  double ***grid_centers;
  int **hex_ids;
  double **walk_weights;
  unsigned int hex_dim_x;
  unsigned int hex_dim_y;
  Graph board;
  //double INF = INFINITY;
  
  public:
    UltraMek();
    ~UltraMek();
    double doubling(double); // for test purposes ...
     void set_unit_length(double);
     void set_unit_height(double);
     int **create_board_graph(int,int,double**);
     void set_grid_centers(int,int);
     double get_unit_length();
     double get_unit_height();
     double get_hex_diameter();
     double ***create_grid_centers(int,int);
     double **create_hex_vertices(double,double,double);
     int *create_vertex_order();
     double compute_euclidean(double,double);
     int *compute_shortest_walk_ids(int,int);
     int point_in_hex_with_center(double*,double*,double);
     void setup_grid_centers();
     double ***get_grid_centers();
     int *compute_board_hex_for_point(double*);
     unsigned int get_dim_x();
     unsigned int get_dim_y();
     
     //void setup_ultramek_geometry(unsigned int dim_x,unsigned int dim_y,double unit_length=1.0,double unit_height=0.5);
     void setup_board_geometry(unsigned int,unsigned int,double,double);
     
};

inline double UltraMek::doubling(double x) {return 2*x;}
inline void UltraMek::set_unit_length(double l) {unit_length = l;}
inline void UltraMek::set_unit_height(double l) {unit_height = l;}
inline double UltraMek::get_unit_length() {return unit_length;}
inline double UltraMek::get_unit_height() {return unit_height;}
inline double UltraMek::get_hex_diameter() {return doubling(unit_length);}
inline unsigned int UltraMek::get_dim_x() {return hex_dim_x;}
inline unsigned int UltraMek::get_dim_y() {return hex_dim_y;}
inline double ***UltraMek::get_grid_centers() {return grid_centers;}
int ultra_mek_tests();

#endif
