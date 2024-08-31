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
