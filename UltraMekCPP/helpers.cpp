// helpers.cpp - cpp library for help functions for Ultramek (compatible with MegaMek)

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

#include "helpers.hpp"

vector<string> tokenizer(string s, char del)
{
    vector<string> result;
    stringstream ss(s);
    string word;
    while (!ss.eof()) {
        getline(ss, word, del);
        result.push_back(word);
    }
    return result;
}

string remove_closure(string token)
{
    token.pop_back();
    token.erase(token.begin());   
    return token;
}

void ltrim_inplace(string &s) 
{
    s.erase(s.begin(), find_if(s.begin(), s.end(), [](unsigned char ch) {
        return !isspace(ch);
    }));
}

void rtrim_inplace(string &s)
{
    s.erase(find_if(s.rbegin(), s.rend(), [](unsigned char ch) {
        return !isspace(ch);
    }).base(), s.end());
}

void trim_inplace(string &s) {
    rtrim_inplace(s);
    ltrim_inplace(s);
}

string ltrim(string s) 
{
    ltrim_inplace(s);
    return s;
}

string rtrim(string s) 
{
    rtrim_inplace(s);
    return s;
}

string trim(string s) 
{
    trim_inplace(s);
    return s;
}
