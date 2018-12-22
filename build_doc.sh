#!/bin/sh
sphinx-apidoc -f -o docs-build/source/ polibeepsync/
make dirhtml -C docs-build/
cp -rf docs-build/build/* docs
rm -rf docs-build/build
