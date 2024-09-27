#!/bin/sh

cd submodules/3dMCGlauber
git checkout electriCharge
./get_LHAPDF.sh
./compile.sh