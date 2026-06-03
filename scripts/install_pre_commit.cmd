@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0install_pre_commit.ps1" %*
exit /b %ERRORLEVEL%
