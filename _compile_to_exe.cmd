@echo off
rmdir /S /Q __pycache__
rmdir /S /Q build
rmdir /S /Q dist

D:\Python36-32\Scripts\pyinstaller.exe -F --hiddenimport vnet.app --hiddenimport vspc.app --hiddenimport vspax.app --hiddenimport common.app --hiddenimport idna --uac-admin main.py

move dist\main.exe freeioe_Rprogramming.exe

rmdir /S /Q __pycache__
rmdir /S /Q build
pause