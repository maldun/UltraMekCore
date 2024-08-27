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
	   vector<string> properties;
	   string typestring;
	   Tile(int,int,int,vector<string>,string);
	   Tile(string,int,int);
	   Tile(); // create empty tile as place holder
	   ~Tile();
};



int tile_tests();

#endif
 
