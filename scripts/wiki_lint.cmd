@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0wiki_lint.ps1" %*
exit /b %ERRORLEVEL%
