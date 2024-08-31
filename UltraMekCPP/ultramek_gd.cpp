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

void UltraMekGD::set_unit_length(double l)
{
  mek.set_unit_length(l);
}

double UltraMekGD::get_unit_length()
{
  return mek.get_unit_length();
}

UltraMekGD::~UltraMekGD()
{
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

void UltraMekGD::_bind_methods()
{
    ClassDB::bind_method(D_METHOD("get_hex_diameter"), &UltraMekGD::get_hex_diameter);
    ClassDB::bind_method(D_METHOD("set_unit_length", "value"), &UltraMekGD::set_unit_length,
			 DEFVAL(1));
    ClassDB::bind_method(D_METHOD("doubling", "value"), &UltraMekGD::doubling, DEFVAL(1));
    ClassDB::bind_method(D_METHOD("get_unit_length"), &UltraMekGD::get_unit_length);
    ClassDB::bind_method(D_METHOD("create_grid_centers", "dim_x", "dim_y"),
			 &UltraMekGD::create_grid_centers, DEFVAL(1),DEFVAL(1));
    //ClassDB::bind_method(D_METHOD("get_total"), &Summator::get_total);
}
