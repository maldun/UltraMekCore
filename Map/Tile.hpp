#ifndef Tile_H
#define Tile_H
#include<vector>
#include<map>
#include<iostream>
#include<string>
#include "../Etc/helpers.hpp"

using namespace std;

class Tile
{
   public:
	   int pos_x;
	   int pos_y;
	   int height;
	   map<string,int> properties;
	   string notes;
	   Tile(int,int,int,map<string,int>);
	   Tile(string);
	   Tile(); // create empty tile as place holder
};



int tile_tests();

#endif
 
