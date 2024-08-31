#!/bin/bash
scons
export LD_LIBRARY_PATH=$(pwd)/UltraMekCPP:$(LD_LIBRARY_PATH)

printf "\n"
printf "==================================== CPP Tests =====================================\n"
printf "\n"
test/unittests

printf "\n"
printf "==================================== Python Tests =====================================\n"
printf "\n"
python test/unittests.py
printf "\n"
printf "==================================== Cleanup =====================================\n"
printf "\n"
scons -c
