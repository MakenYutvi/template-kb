@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0git_sync.ps1" %*
exit /b %ERRORLEVEL%
