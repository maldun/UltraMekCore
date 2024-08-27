cpp = Environment(CCFLAGS=['-Wall'],LIBPATH=['Map'])
#SConscript(['Map/Sconscript'])
cfiles = ["unittests.cpp","Map/Tile.cpp","Map/MMap.cpp","Etc/helpers.cpp"]
hfiles = [f.replace(".cpp",".hpp") for f in cfiles]

SharedLibrary("mmap",cfiles,include=hfiles)
Library("mmap",cfiles,include=hfiles)
unittests = cpp.Program("unittests",LIBS=["mmap"],LIBPATH='.',include=hfiles)
