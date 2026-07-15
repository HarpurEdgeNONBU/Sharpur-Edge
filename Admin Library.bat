@echo off
cd /d "%~dp0"
py manager\run.py
if errorlevel 1 python manager\run.py
pause
