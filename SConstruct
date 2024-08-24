cpp = Environment(CCFLAGS=['-Wall'],LIBPATH=['Map'])
#SConscript(['Map/Sconscript'])
unittests = cpp.Program("unittests",["unittests.cpp","Map/Tile.cpp"],include=["Map/Tile.hpp"])
