
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

UltraMek::UltraMek()
{
  unit_length = 1.0;
  unit_height = 1.0;
}

UltraMek::~UltraMek()
{
    // do nothing (yet)
}


double ***UltraMek::create_grid_centers(int dim_x, int dim_y)
{
  double ***matrix = compute_grid_centers(dim_x,dim_y,unit_length);
  return matrix;
}

double **UltraMek::create_hex_vertices(double pos_x, double pos_y, double length, double height)
{
  double **matrix = compute_hex_vertices(pos_x,pos_y,length,height);
  return matrix;     
}

int *UltraMek::create_vertex_order()
{
  int *order = compute_vertex_order();
  return order;     
}


//////////////////////////////////////// TESTS /////////////////////////////////////////////////////


int test_doubling()
{
  UltraMek mek = UltraMek();
  if(mek.doubling(2.0) != 4.0){ return 1;}

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
  
  cout << "UkltraMek tests passed!" << endl;
  return 0;
}
