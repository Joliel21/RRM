@echo off
cd /d "%~dp0"
echo Project folder: %CD%
echo.
echo Available npm scripts:
call npm run
echo.
pause
