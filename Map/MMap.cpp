#include "Tile.hpp"
#include "MMap.hpp"

const string SIZE_KEY = "size";  
const string HEX_KEY = "hex";  



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
    int pos_x;
    int pos_y;
    unsigned int counter = 0;
  
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
                map_data = vector<vector<Tile>>(dim_x,vector<Tile>(dim_y,emptyt));
            }
            
            size_t foundh = line.rfind(HEX_KEY);
            if(foundh != string::npos)
            {
                pos_x = counter%dim_x;
                pos_y = counter/dim_x;
                map_data[pos_x][pos_y] = convertMMLine2Tile(line,pos_x,pos_y);
                
                counter++;
            }
            //cout << line << endl; 
            
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

Tile MMap::convertMMLine2Tile(string line,int pos_x,int pos_y)
{
    vector<string> spair;
    vector<string> tokens = tokenizer(line,' ');
    
    int h = stoi(tokens[2]);
    string typestr = "";
    vector<string> props;
    if(tokens[3].size() > 2)
    {
        string token = trim(tokens[3]);
        token = remove_closure(token);
        vector<string> sub_tokens = tokenizer(token,';');
        for(long unsigned int i=0;i<sub_tokens.size();i++)
        {
           props.push_back(sub_tokens[i]);   
        }
    }
    typestr = remove_closure(trim(tokens[4]));
    return Tile(pos_x,pos_y,h,props,typestr);
}

MMap::~MMap()
{
  vector<vector<Tile>>().swap(map_data);
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
  if(!(mm.dim_x == 16) or !(mm.dim_y == 17) or (mm.map_data[13][0].height != 0) or (mm.map_data[13][0].properties[0]!="woods:2") 
      or (mm.map_data[15][0].properties[0]!="water:1") or  (mm.map_data[15][16].properties[1] !="foliage_elev:2"))
   {
     cout << "MMap creation from file failed!" << endl;
     return 1;
   }
   filename = "Map/samples/snow.board";
   mm = MMap(filename);
   if(!(mm.dim_x == 16) or !(mm.dim_y == 17) or (mm.map_data[15][16].typestring !="snow"))
   {
     cout << "MMap creation from snow file failed!" << endl;
     return 2;
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
