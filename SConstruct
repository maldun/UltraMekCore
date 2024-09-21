import distutils.sysconfig
import os
import shutil

cpp = Environment(CCFLAGS=['-Wall'],LIBPATH=['UltraMekCPP'])
cfiles = ["test/unittests.cpp","UltraMekCPP/helpers.cpp","UltraMekCPP/geometry.cpp","UltraMekCPP/ultramek.cpp"]
hfiles = [f.replace(".cpp",".hpp") for f in cfiles]

cpp.SharedLibrary("UltraMekCPP/ultramek",cfiles,include=hfiles)
unittests = cpp.Program("test/unittests",cfiles, include=hfiles, LIBPATH='UltraMekCPP',LIBS=["ultramek"])

swig_env = Environment(SWIGFLAGS=["-c++","-python"],
                   CPPPATH=[distutils.sysconfig.get_python_inc()],
                   SHLIBPREFIX="",
                   LIBPATH=['UltraMekCPP'],
                   CCFLAGS=['-Wall'])

swig_files = ["UltraMekCPP/ultramek.cpp","UltraMekCPP/helpers.cpp","UltraMekCPP/geometry.cpp"] 
swig_include = [f.replace(".cpp",".hpp") for f in swig_files]
swig_files += ["UltraMekCPP/UltraMekCPP.i"]

swig_env.SharedLibrary("UltraMekCPP/_ultramek.so",swig_files,include=swig_include)

def copyme(target,source,env):
    shutil.copy2(source,target)

#swig_env.Command("UltraMekCPP/_ultramek.so","UltraMekPy/_ultramek.so", copyme)
#swig_env.Command("UltraMekCPP/ultramek.py","UltraMekPy/ultramek.py", copyme)

