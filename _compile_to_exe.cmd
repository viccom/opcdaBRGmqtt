@echo off
rmdir /S /Q __pycache__
rmdir /S /Q build
rmdir /S /Q dist

G:\mycode\opcdaBRGmqtt\venv\Scripts\pyinstaller.exe -F --hiddenimport opcdabrg.app --uac-admin main.py

move dist\main.exe opcdaBRGmqtt.exe

rmdir /S /Q __pycache__
rmdir /S /Q build
pause