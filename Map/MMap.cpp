#include "Tile.hpp"
#include "MMap.hpp"

const string SIZE_KEY = "size";  



MMap::MMap(int x, int y, vector<vector<Tile>> mapd)
{
	dim_x = x;
    dim_y = y;
    map_data = mapd;
}

MMap::MMap(string filename)
{
    ifstream file(filename); 
  
    // String to store each line of the file. 
    string line;
    vector<string> tokens;
  
    if (file.is_open()) { 
        // Read each line from the file and store it in the 
        // 'line' variable. 
        while (getline(file, line)) { 
            size_t found = line.rfind(SIZE_KEY);
            if(found != string::npos)
            {
                tokens = tokenizer(line,' ');
                dim_x = stoi(tokens[1]);
                dim_y = stoi(tokens[2]);
                Tile emptyt = Tile();
                map_data = vector<vector<Tile>>(dim_y,vector<Tile>(dim_x,emptyt));
            }
            cout << line << endl; 
        } 
  
        // Close the file stream once all lines have been 
        // read. 
        file.close(); 
    } 
    else 
    { 
           throw runtime_error("Error! File not fond!");
    } 
}

int test_mmap_creation()
{
  int x = 1;
  int y = 1;
  Tile t = Tile();
  vector<vector<Tile>> tt(1,vector<Tile>(1,t));
  MMap mm = MMap(x,y,tt);
  
  if(!(mm.dim_x == x) || !(mm.dim_y == y) || !(mm.map_data[0][0].height == t.height))
   {
     cout << "MMap creation failed!" << endl;
     return 1;
   }
  return 0;
}

int test_mmap_creation_from_file()
{
  string filename = "Map/samples/test.board";
  MMap mm = MMap(filename);
  if(!(mm.dim_x == 16) || !(mm.dim_y == 17))
   {
     cout << "MMap creation from file failed!" << endl;
     return 1;
   }
  return 0;
}

int mmap_tests()
{
  if(test_mmap_creation() != 0)
   {
      throw invalid_argument("MMap Creation failed");   
   }
   if(test_mmap_creation_from_file() != 0)
   {
      throw invalid_argument("MMap Creation from file failed");   
   }
  cout << "All MMap Tests passed!" << endl;
  return 0;    
}
