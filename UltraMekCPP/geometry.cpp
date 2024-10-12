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

int *point_on_grid(double* p,int dim_x,int dim_y,double ***grid_centers,double unit_length)
{
  double px = p[0];
  double py = p[1];
  
  int *out = new int[2];
  out[0]=-1;out[1]=-1;
  
  if(px < grid_centers[0][0][0]-unit_length or px > grid_centers[dim_x-1][0][0]+unit_length)
  {
    return out;
  }
  if(py > grid_centers[0][0][1]+unit_length or py < grid_centers[0][dim_y-1][1]-unit_length)
  {
    return out;
  }
  int lowerx = 0;
  int upperx = dim_x;
  int dist = upperx-lowerx;
  int dist2 = dist;
  while(dist>4)
  {
    if(grid_centers[lowerx][0][0]-unit_length <= px and px <= grid_centers[upperx/2][0][0])  
    {
       //lowerx = lowerx;
       upperx = upperx/2;
    }
    else if(grid_centers[upperx/2][0][0] < px and px <= grid_centers[min(upperx,dim_x-1)][0][0]+unit_length)  
    {
       lowerx = upperx/2;
       //upperx = upperx;
    }
    else
    {break;}
    // stop deadlock ...
    dist2 = upperx-lowerx;
    if(dist2 == dist)
    {break;}
    else 
    {dist=dist2;}
    
  }
  int lowery = 0;
  int uppery = dim_y;
  dist = uppery-lowery;
  while(dist>4)
  {
    // cout << "lower: " << lowery << " upper: " << uppery << endl;
    // cout << "lower: " << grid_centers[0][lowery][1]+unit_length << " upper: " << grid_centers[0][uppery-1][1] << endl;
   if(grid_centers[0][lowery][1]+2*unit_length >= py and py >= grid_centers[0][uppery/2][1])  
    {
       //lowery = lowery;
       uppery = uppery/2;
    }
    else if(grid_centers[0][uppery/2][1] > py and py>=grid_centers[0][min(uppery,dim_y-1)][1]-unit_length)
    {
       lowery = uppery/2;
       //uppery = uppery;
    }
    else
    {break;}
    // stop deadlock ...
    dist2 = uppery-lowery;
    if(dist2 == dist)
    {break;}
    else 
    {dist=dist2;}
    }
    //cout << "lowerx: " << lowerx << " upperx: " << upperx << endl;
    //cout << "lowery: " << lowery << " uppery: " << uppery << endl;
    for(int i=lowerx;i<upperx;i++)
    {
      for(int j=lowery;j<uppery;j++)
      {
         //cout << "(" << i << "," << j << ") " << point_inside_hex_with_center(p,grid_centers[i][j],unit_length) << endl; 
         if(point_inside_hex_with_center(p,grid_centers[i][j],unit_length)==1)
         {
            
            out[0]=i;out[1]=j;
            return out;
         }
      }
   }
  return out;
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

double **compute_hex_vertices(double pos_x, double pos_y,double unit_length)
{

  double **verts = initialize_2d_matrix(HEX+1,DIM2);
  double alpha = PI/3;

  // add centers
  verts[0][0] = pos_x;
  verts[0][1] = pos_y;
  //verts[0][2] = 0;
  
  //verts[7][0] = pos_x;
  //verts[7][1] = pos_y;
  //verts[7][2] = unit_height;
  
  for(int i=0;i<HEX;i++)
  {
    verts[i+1][0] = pos_x + unit_length*cos(i*alpha);
    verts[i+1][1] = pos_y + unit_length*sin(i*alpha);
    //verts[i+1][2] = 0;

    //verts[i+HEX+2][0] = pos_x + unit_length*cos(i*alpha);
    //verts[i+HEX+2][1] = pos_y + unit_length*sin(i*alpha);
    //verts[i+HEX+2][2] = unit_height;
  }
  return verts;
}

int point_inside_triangle(double* x,double* y0,double* y1,double* y2)
{
   // Checks if x is inside the triangle(y0,y1,y2)
   // We use that a 2x2 linear equation has a unique solution if
   // the vectors are l.i.
  double z0[2] = {0,0};
  double z1[2] = {0,0};
  double xi[2] = {0,0};
  double alpha = 0; 
  for(int i=0;i<2;i++)
  {
     z0[i] = y1[i]-y0[i];
     z1[i] = y2[i]-y0[i];
     xi[i] = x[i]- y0[i];
  }
  double det = z0[0]*z1[1] - z1[0]*z0[1];
  if(det*det < 1e-6) // l.d. system ...triangle degenerated
  {
    return -1; 
  }
  // solve the 2x2 system A*alpha = [z0,z1]*alpha = [[z0[0],z1[0]];[z0[1],z1[1]]]*[alpha[0];alpha[1]] = x
  // use explizit formula for inv(A) = [[z1[1],-z1[0]];[-z0[1],z0[0]]/det(A)
  alpha = (z1[1]*xi[0] -z1[0]*xi[1])/det;
  if((alpha < 0) or (alpha > 1))
  {
    return 0;
  }
  alpha = (-z0[1]*xi[0] +z0[0]*xi[1])/det;
  if((alpha < 0) or (alpha > 1))
  {
    return 0;
  }
  return 1;
  
}

int point_inside_hex(double* x, double** verts)
{
   int state = 0;
   for(int k=0;k<HEX;k++)
   {
       state = point_inside_triangle(x,verts[0],verts[k+1],verts[(k+1)%(HEX)+1]);
       if(state != 0)
       {
         return state;
       }
   }
   return 0;
}

int point_inside_hex_with_center(double *x,double *center,double unit_length)
{
  double **verts = compute_hex_vertices(center[0],center[1],unit_length);
  int state = point_inside_hex(x, verts);
  delete verts;
  return state; 
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
  double l = 1.0;
  double **matrix = compute_hex_vertices(0,0,l);
  if(matrix[0][0] != 0){return 1;}
  if(matrix[0][1] != 0){return 1;}
  //if(matrix[0][2] != 0){return 1;}
  
  if(matrix[1][0] != l){return 1;}
  if(matrix[1][1] != 0){return 1;}
  //if(matrix[1][2] != 0){return 1;}

  if(matrix[4][0] != -l){return 1;}
  if(abs(matrix[4][1]) > 1e-6){return 1;}
  //if(matrix[4][2] != 0){return 1;}

//   if(abs(matrix[9][0]-l/2.0) > 1e-6){return 1;}
//   if(abs(matrix[9][1]-l*sqrt(3.0)/2.0) > 1e-6){return 1;}
//   if(matrix[9][2] != h){return 1;}
//   
  delete matrix;

  return 0;
  
}

int test_point_inside_triangle()
{
   double x[2] = {0,0};
   double y0[2] = {1,0};
   double y1[2] = {2,0};
   double y2[2] = {2,1};
   
   if(point_inside_triangle(x,y0,y1,y2) != 0)
   {return 1;}
   x[0] = 1.5; x[1] = 0.1;
   if(point_inside_triangle(x,y0,y1,y2) != 1)
   {return 1;}
   x[0] = 1.5; x[1] = 1.1;
   if(point_inside_triangle(x,y0,y1,y2) != 0)
   {return 1;}
   x[0] = 1.1; x[1] = 0.02;
   if(point_inside_triangle(x,y0,y1,y2) != 1)
   {return 1;}
   y2[0] = y1[0]; y2[1] = y1[1];
   if(point_inside_triangle(x,y0,y1,y2) != -1)
   {return 1;}
   return 0;
}

int test_point_inside_hex()
{
  double center[2] = {0,0};
  double unit_length = 1.0;
  double **verts = compute_hex_vertices(center[0],center[1],unit_length);
  double x[2] = {0,0};
  if(point_inside_hex(x,verts) != 1)
   {return 1;}
  if(point_inside_hex_with_center(x,center,unit_length) != 1)
   {return 1;}
  x[0] = 0.1; x[1] = 0.1;
  if(point_inside_hex(x,verts) != 1)
   {return 1;}
  if(point_inside_hex_with_center(x,center,unit_length) != 1)
   {return 1;}
  x[0] = 100.0; x[1] = 0.1;
  if(point_inside_hex(x,verts) != 0)
   {return 1;}
  if(point_inside_hex_with_center(x,center,unit_length) != 0)
   {return 1;}
   
   delete verts;
   return 0;
}

int test_point_on_board()
{
  double unit_length = 1.0;
  int dim_x = 16;
  int dim_y = 17;
  double ***centers = compute_grid_centers(dim_x,dim_y,unit_length);
  double p[2] = {5,-20};
  //cout << centers[0][0][0] << " " << centers[0][0][1] << endl;
  //cout << centers[dim_x-1][dim_y-1][0] << " " << centers[dim_x-1][dim_y-1][1] << endl;
  int *result = point_on_grid(p,dim_x,dim_y,centers,unit_length);
  if(point_inside_hex_with_center(p,centers[result[0]][result[1]],unit_length)!=1)
  {return 1;}
  
  p[0] = -1;
  result = point_on_grid(p,dim_x,dim_y,centers,unit_length);
  if(result[0] != -1 and result[1] != -1)
  {return 1;}
  p[1] = 1; p[0] = 5;
  result = point_on_grid(p,dim_x,dim_y,centers,unit_length);
  if(result[0] != -1 and result[1] != -1)
  {return 1;}
  
  dim_x = 1;
  dim_y = 2;
  centers = compute_grid_centers(dim_x,dim_y,unit_length);
  p[1]= p[0]=0;
  result = point_on_grid(p,dim_x,dim_y,centers,unit_length);
  if(result[0] != 0 and result[1] != 0)
  {
    //cout << centers[0][0][0] << centers[0][0][1] << endl;
    //cout << point_inside_hex_with_center(p,centers[0][0],unit_length) << endl;
    return 1;}
  
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
  if(test_point_inside_triangle() != 0)
  {
    cout << "Test inside triangle failed!" << endl;
    return 1;
  }
  if(test_point_inside_hex() != 0)
  {
    cout << "Test inside hex failed!" << endl;
    return 1;
  }
  if(test_point_on_board() != 0)
  {
    cout << "Test point on board failed!" << endl;
    return 1;
  }
  
  cout << "Geometry tests passed!" << endl;
  return 0;
}
