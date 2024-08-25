#include "unittests.hpp"
#include "Map/Tile.hpp"
#include "Map/MMap.hpp"

int main(int argc, char *argv[])
{
    tile_tests();
    mmap_tests();
    cout << "All tests passed!" << endl;
    return 0;
} 
