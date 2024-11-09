﻿// helpers.hpp - cpp library header for help functions for Ultramek (compatible with MekHQ)

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

#ifndef HELPERS_H
#define HELPERS_H

#include<vector>
#include<map>
#include<string>
#include<iostream>
#include <fstream> 
#include <sstream>
#include <algorithm> 
#include <cctype>
#include <locale>

using namespace std;

vector<string> tokenizer(string, char);
string remove_closure(string);
void ltrim_inplace(string&);
void rtrim_inplace(string&);
void trim_inplace(string&);
string ltrim(string);
string rtrim(string); 
string trim(string); 

#endif
