// geometry - cpp library gemoetric operations for Ultramek (compatible with MegaMek)

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

#include "geometry.hpp"

double **initialize_2d_matrix(unsigned int dim_x,unsigned int dim_y)
{
   double **matrix = new double*[dim_x];
   for(unsigned int i=0;i<dim_x;i++)
   {
      matrix[i] = new double[dim_y];
      for(unsigned int j=0;j<dim_y;j++)
      {
	 matrix[i][j] = 0;
	 
      }  
   }
   return matrix;
}


double ***initialize_3d_matrix(unsigned int dim_x,unsigned int dim_y,unsigned int dim_z)
{
   double ***matrix = new double**[dim_x];
   for(unsigned int i=0;i<dim_x;i++)
   {
      matrix[i] = new double*[dim_y];
      for(unsigned int j=0;j<dim_y;j++)
      {
	 matrix[i][j] = new double[dim_z];
	 for(unsigned int k=0;k<dim_z;k++)
	 {
	   matrix[i][j][k] = 0.0;
	 }
      }  
   }
   return matrix;
}

double ***compute_grid_centers(unsigned int dim_x, unsigned int dim_y, double unit_length)
{

   double ***centers = initialize_3d_matrix(dim_x,dim_y,DIM2);
   double shift_x = unit_length;
   double shift_y = compute_hex_height(unit_length)/2.0;
   double delta_x = 3*unit_length/2;
   double delta_y = compute_hex_height(unit_length);
   
   for(unsigned int i = 0; i<dim_x;i++)
   {
       for(unsigned int j = 0; j<dim_y;j++)
       {
	   // x - coord
           centers[i][j][0] = shift_x + i*delta_x;
	   // y - coord
           centers[i][j][1] = - shift_y - (i%2)*shift_y - j*delta_y;
       }
   }
   return centers;
}

double **compute_hex_vertices(double pos_x, double pos_y,double unit_length,double unit_height)
{

  double **verts = initialize_2d_matrix(2*HEX+2,DIM3);
  double alpha = PI/3;

  // add centers
  verts[0][0] = pos_x;
  verts[0][1] = pos_y;
  verts[0][2] = 0;
  
  verts[7][0] = pos_x;
  verts[7][1] = pos_y;
  verts[7][2] = unit_height;
  
  for(int i=0;i<HEX;i++)
  {
    verts[i+1][0] = pos_x + unit_length*cos(i*alpha);
    verts[i+1][1] = pos_y + unit_length*sin(i*alpha);
    verts[i+1][2] = 0;

    verts[i+HEX+2][0] = pos_x + unit_length*cos(i*alpha);
    verts[i+HEX+2][1] = pos_y + unit_length*sin(i*alpha);
    verts[i+HEX+2][2] = unit_height;
  }
  return verts;
}


double compute_hex_height(double side_length)
{
  double c = sqrt(3.0)*side_length;
  return c; 
}

double compute_hex_sub_height(double side_length)
{
  double c = side_length/2.0;
  return c; 
}

int test_compute_hex_height()
{
  if(compute_hex_height(2.0) != sqrt(3.0)*2.0)
  {
    return 1;
  }
  return 0;
}

int test_compute_hex_sub_height()
{
  if(compute_hex_sub_height(2.0) != 1.0)
  {
    return 1;
  }
  return 0;
}

int test_3d_matrix_creation()
{
  int x= 17; int y = 16; int z = 3;
  double ***matrix = initialize_3d_matrix(x,y,z);
  for(int i = 0; i<x; i++)
  {
    for(int j = 0; j<y; j++)
    {
      for(int k = 0; k<z; k++)
      {
        if(matrix[i][j][k] != 0) {return 1;}
      }
    }
  }
  delete matrix;

  return 0;
}

int test_2d_matrix_creation()
{
  int x= 17; int y = 16;
  double **matrix = initialize_2d_matrix(x,y);
  for(int i = 0; i<x; i++)
  {
    for(int j = 0; j<y; j++)
    {
      if(matrix[i][j] != 0) {return 1;}
    }
  }
  delete matrix;

  return 0;
}

int test_compute_grid_centers()
{
  int x = 2; int y = 2;
  double l = 1.0;
  double ***matrix = compute_grid_centers(x,y,l);
  if(matrix[0][0][0] != l){return l;}
  if(matrix[0][0][1] != -sqrt(3)*l/2.0){return 1;}
  if(matrix[1][0][0] != 2.5*l){return 1;}
  if(matrix[1][0][1] != -sqrt(3)*l){return 1;}

  if(matrix[0][1][0] != l){return 1;}
  if(matrix[0][1][1] != -3*sqrt(3)*l/2.0){return 1;}
  if(matrix[1][1][0] != 2.5*l){return 1;}
  if(matrix[1][1][1] != -2.0*sqrt(3)*l){return 1;}

  delete matrix;

  
  return 0;
  
}

int test_compute_hex_vertices()
{
  double h = 1.0;
  double l = 1.0;
  double **matrix = compute_hex_vertices(0,0,l,h);
  if(matrix[0][0] != 0){return 1;}
  if(matrix[0][1] != 0){return 1;}
  if(matrix[0][2] != 0){return 1;}
  
  if(matrix[1][0] != l){return 1;}
  if(matrix[1][1] != 0){return 1;}
  if(matrix[1][2] != 0){return 1;}

  if(matrix[4][0] != -l){return 1;}
  if(abs(matrix[4][1]) > 1e-6){return 1;}
  if(matrix[4][2] != 0){return 1;}

  if(abs(matrix[9][0]-l/2.0) > 1e-6){return 1;}
  if(abs(matrix[9][1]-l*sqrt(3.0)/2.0) > 1e-6){return 1;}
  if(matrix[9][2] != h){return 1;}
  
  delete matrix;

  return 0;
  
}

int geometry_tests()
{

  if(test_compute_hex_height() != 0)
  {
    cout << "Test hex height failed!" << endl;
    return 1;
  }

  if(test_compute_hex_sub_height() != 0)
  {
    cout << "Test hex sub height failed!" << endl;
    return 1;
  }
  
  if(test_2d_matrix_creation() != 0)
  {
    cout << "Test 2d matrix creation failed!" << endl;
    return 1;
  }

  if(test_3d_matrix_creation() != 0)
  {
    cout << "Test 3d matrix creation failed!" << endl;
    return 1;
  }

  if(test_compute_hex_vertices() != 0)
  {
    cout << "Test hex vertices failed!" << endl;
    return 1;
  }

  if(test_compute_grid_centers() != 0)
  {
    cout << "Test grid center creation failed!" << endl;
    return 1;
  }
  
  cout << "Geometry tests passed!" << endl;
  return 0;
}
