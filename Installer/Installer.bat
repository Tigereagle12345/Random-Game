@echo off
echo WARNING: This program may need to be run with administrator privelidges.
echo Beginning Installation...

echo Installing Python Modules...

pip install oauth2client
pip install gspread

echo Done

python change_permissions.py

del change_permissions.py
del installer.bat