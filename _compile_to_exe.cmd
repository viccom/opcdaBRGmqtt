@echo off
setlocal EnableDelayedExpansion & cd /d "%~dp0"

rmdir /S /Q __pycache__
rmdir /S /Q build
rmdir /S /Q dist

::G:\mycode\opcdaBRGmqtt\venv\Scripts\pyinstaller.exe -F --hiddenimport opcdabrg.app --uac-admin main.py

%cd%\venv\Scripts\pyinstaller.exe -F %cd%\opcdabrgconfig.spec

move dist\main.exe opcdaBRGmqtt.exe

rmdir /S /Q __pycache__
rmdir /S /Q build
pause & exit