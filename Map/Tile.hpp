#ifndef MMap_H
#define MMap_H
#include<vector>
#include<map>
#include<iostream>
#include<string>

using namespace std;

class Tile
{
   public:
	   int pos_x;
	   int pos_y;
	   int height;
	   
	   map<string,int> properties;
	   string notes;
	   Tile(int,int,int);
};



int tile_tests();

#endif
 
