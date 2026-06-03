@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0kb_python.ps1" %*
exit /b %ERRORLEVEL%
