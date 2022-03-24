#!/bin/bash
echo WARNING: This program may need to be run with sudo or as root
echo Beginning Installation...

echo Installing Python Modules...

pip install oauth2client
pip install gspread

echo Done

rm change_permissions.py
rm Installer.bat
rm Installer.sh