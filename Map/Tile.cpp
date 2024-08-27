#include "Tile.hpp" 

Tile::Tile(int x, int y, int h,vector<string> props,string typestr)
{
    pos_x = x;
    pos_y = y;
    height = h;
    properties = props;
    typestring = typestr;
}

Tile::Tile()
{
    pos_x = -1;
    pos_y = -1;
    height = -100;
    typestring = "";
}

Tile::~Tile()
{
   properties.erase(properties.begin(),properties.end());   
}

int test_empty_tile_creation()
{
   
   Tile t = Tile();
   if((t.height != -100) || !(t.properties.empty()) || (t.pos_x != -1) || (t.pos_y != -1) || (t.typestring != ""))
   {
     cout << "Empty Tile creation failed!" << endl;
     return 1;
   }
   
   return 0;
}


int test_tile_creation()
{
   int x = 1;
   int y = 2;
   int h = 3;
   vector<string> props(1,"swamp:1"); 
   string typestr = "snow";
   Tile t = Tile(x,y,h,props,typestr);
   if(!(t.height == h) || !(t.properties == props) || !(t.pos_x == x) || !(t.pos_y == y) || (t.typestring != "snow")) 
   {
     cout << "Tile creation failed!" << endl;
     return 1;
   }
   
   return 0;
}

int tile_tests()
{
   if(test_tile_creation() != 0)
   {
      throw invalid_argument("Tile Creation failed");   
   }
   if(test_empty_tile_creation() != 0)
   {
      throw invalid_argument("Empty Tile Creation failed");   
   }
   cout << "All Tile Tests passed!" << endl;
   return 0;
     
}
