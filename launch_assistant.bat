@echo off
REM Universal Knowledge Assistant Launcher
REM Checks if first-run setup is needed

cd /d "%~dp0"

REM Check if setup has been completed
if not exist ".setup_complete" (
    echo First-time setup required...
    echo Launching setup wizard...
    pythonw.exe first_run_setup.pyw
    exit /b
)

REM Setup complete, launch main application
pythonw.exe launch_assistant_gui.pyw
