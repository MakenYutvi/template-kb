@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0new_kb_item.ps1" %*
exit /b %ERRORLEVEL%
