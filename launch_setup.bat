@echo off
REM Launch the First-Run Setup Wizard
REM Use this to reconfigure the Universal Knowledge Assistant

cd /d "%~dp0"

echo.
echo ================================
echo  Universal Knowledge Assistant
echo  Setup Wizard
echo ================================
echo.

pythonw.exe first_run_setup.pyw
