#ifndef MMap_H
#define MMap_H

#include<vector>
#include<map>
#include<string>
#include<iostream>
#include <fstream> 
#include <sstream>
#include "Tile.hpp"
#include "../Etc/helpers.hpp"

using namespace std;

class MMap
{
   public:
      int dim_x;
      int dim_y;
      vector<vector<Tile>> map_data;
      MMap(string);
      MMap(int,int,vector<vector<Tile>>);
      
};

int mmap_tests();

#endif
 
