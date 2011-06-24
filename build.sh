#!/bin/bash
# Copyright (C) 2006-2011 Mathias Weber <mathew.weber@gmail.com>

if [ -d build ]; then
    echo "Clear old build directory."
    rm -rf build
fi

mkdir build
cp * -rf build
cd build

find . -name "*pyc" -exec rm -rf '{}' ';' 

dpkg-buildpackage

