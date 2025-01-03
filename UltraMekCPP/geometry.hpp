﻿// geometry.hpp - cpp geometry header for Ultramek (compatible with MekHQ)

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

#ifndef GEOMETRY_H
#define GEOMETRY_H
#include<vector>
#include<map>
#include<iostream>
#include<string>
#include<cmath>
#include "helpers.hpp"

using namespace std;

const double PI = atan(1)*4;
const int DIM2 = 2;
const int DIM3 = 3;
const int HEX = 6;

double compute_hex_height(double);
double compute_hex_sub_height(double);

template <typename Type = double>
inline Type **initialize_2d_matrix(unsigned int dim_x,unsigned int dim_y)
{
   Type **matrix = new Type*[dim_x];
   for(unsigned int i=0;i<dim_x;i++)
   {
      matrix[i] = new Type[dim_y];
      for(unsigned int j=0;j<dim_y;j++)
      {
	 matrix[i][j] = 0;
	 
      }  
   }
   return matrix;
}

template <typename Type = double>
inline Type ***initialize_3d_matrix(unsigned int dim_x,unsigned int dim_y,unsigned int dim_z)
{
   Type ***matrix = new Type**[dim_x];
   for(unsigned int i=0;i<dim_x;i++)
   {
      matrix[i] = new Type*[dim_y];
      for(unsigned int j=0;j<dim_y;j++)
      {
	 matrix[i][j] = new Type[dim_z];
	 for(unsigned int k=0;k<dim_z;k++)
	 {
	   matrix[i][j][k] = 0.0;
	 }
      }  
   }
   return matrix;
}

template <typename Type = double>
inline void delete_2d_matrix(unsigned int dim_x,Type **matrix_2d)
{
  for(unsigned int k=0;k<dim_x;k++)
  { delete[] matrix_2d[k]; }
  delete[] matrix_2d;
  matrix_2d = nullptr;
}

template <typename Type = double>
inline void delete_3d_matrix(unsigned int dim_x,unsigned int dim_y,Type ***matrix_3d)
{
  for(unsigned int k=0;k<dim_x;k++)
  {
    for(unsigned int l=0;l<dim_y;l++)
    {delete[] matrix_3d[k][l]; }
    delete[] matrix_3d[k];
  }
  delete[] matrix_3d;
  matrix_3d = nullptr;
}

double **compute_hex_vertices(double,double,double);
double ***compute_grid_centers(unsigned int, unsigned int,double);
int point_inside_triangle(double*,double*,double*,double*);
int point_inside_hex(double*,double**);
int point_inside_hex_with_center(double*,double*,double);

int *point_on_grid(double*,int,int,double***,double);

inline int *compute_vertex_order()
{
  int *order = new int[3*24];
  for(int i=0;i<HEX;i++)
  {
    order[0+3*i] = 0;
    order[1+3*i] = 1+i;
    if(i+2<7){order[2+3*i] = 2+i;}
    else {order[2+3*i] = 1;}

    order[18+3*i] = 7;
    order[18+1+3*i] = 7+1+i;
    if(7+i+2<14){order[18+2+3*i] = 7+2+i;}
    else {order[18+2+3*i] = 8;}

    order[36+0+3*i] = 1+i;
    order[36+1+3*i] = 8+i;
    if(i<5){
      order[36+2+3*i] = 1+i+1;}
    else{
      order[36+2+3*i] = 1;}
    

    order[54+0+3*i] = 8+i;
    if(i<5){
      order[54+1+3*i] = 8+1+i;
      order[54+2+3*i] = 2+i;}
    else{
      order[54+1+3*i] = 8;
      order[54+2+3*i] = 1;}
  }
  return order;
}

int geometry_tests();



#endif
