cpp = Environment(CCFLAGS=['-Wall'],LIBPATH=['UltraMekCPP'])
#SConscript(['Map/Sconscript'])
cfiles = ["test/unittests.cpp","UltraMekCPP/helpers.cpp"]
hfiles = [f.replace(".cpp",".hpp") for f in cfiles]

cpp.SharedLibrary("UltraMekCPP/ultramek",cfiles,include=hfiles)
#Library("mmap",cfiles,include=hfiles)
unittests = cpp.Program("test/unittests",cfiles, include=hfiles, LIBPATH='UltraMekCPP',LIBS=["ultramek"])
