@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0source_digest.ps1" %*
exit /b %ERRORLEVEL%
