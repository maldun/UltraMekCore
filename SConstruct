cpp = Environment(CCFLAGS=['-Wall'],LIBPATH=['Map'])
#SConscript(['Map/Sconscript'])
cfiles = ["unittests.cpp","Map/Tile.cpp","Map/MMap.cpp","Etc/helpers.cpp"]
hfiles = [f.replace(".cpp",".hpp") for f in cfiles]
unittests = cpp.Program("unittests",cfiles,include=hfiles)
