@echo off
echo WARNING: Do not close this window or game will break
start /wait cmd /c "game.bat" | echo N
python log_off.py
pause