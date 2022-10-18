#!/bin/bash

rm -rf ../innarow-build
mkdir -p ../innarow-build
cp -r frontend ../innarow-build
mkdir -p ../innarow-build/backend
cp backend/*.py ../innarow-build/backend
cp backend/setupenv.sh ../innarow-build/backend
cp backend/requirements.txt ../innarow-build/backend
