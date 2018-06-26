@echo off
echo Compiling
python3 -V >nul 2>&1
if errorlevel 1 (
  set PY=python
) else (
  set PY=python3
)
coconut -t 3.4 example.coco --mypy --python-version 3.4 --python-executable $PY
coconut -t 3.4 -p rese/ --mypy --python-version 3.4 --python-executable $PY
echo Running tests (this may take a few minutes)...
%PY% example.py
