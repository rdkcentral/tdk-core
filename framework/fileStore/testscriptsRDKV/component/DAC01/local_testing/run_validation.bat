@echo off
REM ====================================================================
REM PackageManager Plugin Validator - Windows Helper
REM 
REM Purpose: Simple way to deploy and validate plugins on RDK device
REM Usage: run_validation.bat [device-ip]
REM Example: run_validation.bat 192.168.29.164
REM ====================================================================

setlocal enabledelayedexpansion

echo.
echo ====================================================
echo PackageManager Plugin Validator - Windows Launcher
echo ====================================================
echo.

REM Check if device IP provided
if "%1"=="" (
    echo Usage: run_validation.bat [device-ip]
    echo Example: run_validation.bat 192.168.29.164
    echo.
    echo Or set as environment variable:
    echo set RDK_DEVICE_IP=192.168.29.164
    echo run_validation.bat
    echo.
    
    REM Try to use environment variable
    if not "!RDK_DEVICE_IP!"=="" (
        set DEVICE_IP=!RDK_DEVICE_IP!
        echo Using RDK_DEVICE_IP from environment: !DEVICE_IP!
    ) else (
        echo Device IP not provided. Exiting.
        pause
        exit /b 1
    )
) else (
    set DEVICE_IP=%1
)

echo Device IP: %DEVICE_IP%
echo.

REM Check if Bash is available
where bash >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Bash is not available in PATH
    echo.
    echo Please install one of the following:
    echo   1. Git Bash: https://git-scm.com/download/win
    echo   2. Windows Subsystem for Linux (WSL)
    echo   3. MinGW/MSYS2
    echo.
    pause
    exit /b 1
)

echo Checking Bash availability... OK
echo.

REM Check if SSH is available
where ssh >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo WARNING: SSH is not available in PATH
    echo.
    echo For device deployment, you need SSH client:
    echo   - Windows 10+: Already installed (update system if needed)
    echo   - Older Windows: Install Git Bash or PuTTY
    echo.
    echo You can still run local validation, but device deployment won't work.
    echo.
)

REM Check device connectivity
echo Checking device connectivity...
ping -n 1 %DEVICE_IP% >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo WARNING: Cannot ping device at %DEVICE_IP%
    echo   - Check device is powered on
    echo   - Check device IP is correct
    echo   - Check network connectivity
    echo.
)

REM Find script location
set SCRIPT_PATH=%~dp0validate_packagemanager_plugins.sh
if not exist "%SCRIPT_PATH%" (
    echo ERROR: Script not found at %SCRIPT_PATH%
    echo.
    echo Please run this from the same directory as validate_packagemanager_plugins.sh
    pause
    exit /b 1
)

echo Script found: %SCRIPT_PATH%
echo.

REM Run deployment
echo ====================================================
echo Starting validation on device: %DEVICE_IP%
echo ====================================================
echo.

REM Execute with SSH deployment
bash "%SCRIPT_PATH%" --deploy-to-device root@%DEVICE_IP%

REM Check result
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ====================================================
    echo Validation completed successfully!
    echo ====================================================
    echo.
    echo Report saved to:
    echo %~dp0plugin_validation_report_device.txt
    echo.
    
    REM Try to open report
    if exist "%~dp0plugin_validation_report_device.txt" (
        echo.
        set /p OPEN_REPORT="Open report in notepad? (y/n): "
        if /i "!OPEN_REPORT!"=="y" (
            notepad "%~dp0plugin_validation_report_device.txt"
        )
    )
) else (
    echo.
    echo ====================================================
    echo Validation failed!
    echo ====================================================
    echo.
    echo Troubleshooting:
    echo   1. Check device IP: %DEVICE_IP%
    echo   2. Verify device is reachable: ping %DEVICE_IP%
    echo   3. Verify SSH is available: ssh -V
    echo   4. Test SSH manually: ssh root@%DEVICE_IP%
    echo.
    echo For more details, see: RUN_ON_RDK_DEVICE.md
    echo.
    pause
    exit /b 1
)

REM Cleanup
pause
