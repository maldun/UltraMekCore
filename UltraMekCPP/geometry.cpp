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

   
   double ***centers = initialize_3d_matrix(dim_x,dim_y,2);
   
   return centers;
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
  
  cout << "Geometry tests passed!" << endl;
  return 0;
}
