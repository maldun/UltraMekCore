// ultramek_gd.h - Ultramek cpp bindings for godot (compatible with MegaMek)

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

//Used snippets of code by © Copyright 2014-2022, Juan Linietsky, Ariel Manzur and the Godot community (CC-BY 3.0)

#ifndef ULTRAMEK_GD_H
#define ULTRAMEK_GD_H

// We don't need windows.h in this plugin but many others do and it throws up on itself all the time
// So best to include it and make sure CI warns us when we use something Microsoft took for their own goals....
#ifdef WIN32
#include <windows.h>
#endif

#include <godot_cpp/classes/ref.hpp>
#include "ultramek.hpp"

using namespace godot;

class UltraMekGD : public RefCounted
{
    GDCLASS(UltraMekGD, RefCounted);
    UltraMek mek;

protected:
    static void _bind_methods();

public:
    UltraMekGD();
    ~UltraMekGD();

    double get_hex_diameter();
    double doubling(double);
    void set_unit_length(double);
    double get_unit_length();
};

#endif //ULTRAMEK_GD_H
