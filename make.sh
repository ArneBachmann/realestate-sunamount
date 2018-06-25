#!/bin/bash
echo Compiling
if [ -z `which python3` ]; then
  export PY=`which python`;
else
  export PY=`which python3`;
fi
echo Using $PY
coconut -t 3.4 example.coco --mypy --python-version 3.4 --python-executable $PY
coconut -t 3.4 -p rese/ --mypy --python-version 3.4 --python-executable $PY
echo Running tests - (this may take a few minutes)...
$PY example.py
