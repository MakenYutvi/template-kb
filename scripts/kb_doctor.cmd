@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0kb_doctor.ps1" %*
exit /b %ERRORLEVEL%
