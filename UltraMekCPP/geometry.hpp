// unittests.hh - cpp unittests header for Ultramek (compatible with MegaMek)

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

double **initialize_2d_matrix(unsigned int, unsigned int);
double ***initialize_3d_matrix(unsigned int, unsigned int,unsigned int);
double ***compute_grid_centers(unsigned int, unsigned int,double);
double compute_hex_height(double);
double compute_hex_sub_height(double);

int geometry_tests();



#endif
