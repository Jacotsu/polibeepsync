#!/bin/sh
sphinx-apidoc -f -o docs/source/ polibeepsync/
make html -C docs/
