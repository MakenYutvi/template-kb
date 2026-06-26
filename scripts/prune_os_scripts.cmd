@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0prune_os_scripts.ps1" %*
exit /b %ERRORLEVEL%
