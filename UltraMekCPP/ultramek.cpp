
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

UltraMek::UltraMek()
{
    // do nothing (yet)
}

int test_doubling()
{
  UltraMek mek = UltraMek();
  if(mek.doubling(2) != 4){ return 1;}

  return 0;
}

int ultra_mek_tests()
{
  if(test_doubling()!=0)
  {
    cout << "Test Doubling failed!" << endl;
    return 1;
  }
  
  cout << "UkltraMek tests passed!" << endl;
  return 0;
}
