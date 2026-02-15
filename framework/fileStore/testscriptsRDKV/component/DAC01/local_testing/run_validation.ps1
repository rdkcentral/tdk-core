#!/usr/bin/env pwsh
# ====================================================================
# PackageManager Plugin Validator - PowerShell Helper
# 
# Purpose: Deploy and validate plugins on RDK device from PowerShell
# Usage: .\run_validation.ps1 -DeviceIP 192.168.29.164
# Or: $env:RDK_DEVICE_IP = "192.168.29.164"; .\run_validation.ps1
# ====================================================================

param(
    [Parameter(Mandatory=$false)]
    [string]$DeviceIP = $env:RDK_DEVICE_IP,
    
    [Parameter(Mandatory=$false)]
    [string]$SSHUser = "root",
    
    [Parameter(Mandatory=$false)]
    [switch]$Verbose = $false,
    
    [Parameter(Mandatory=$false)]
    [switch]$Help = $false
)

# Display help
if ($Help -or [string]::IsNullOrEmpty($DeviceIP)) {
    Write-Host ""
    Write-Host "=====================================================" -ForegroundColor Cyan
    Write-Host "PackageManager Plugin Validator - PowerShell Launcher" -ForegroundColor Cyan
    Write-Host "=====================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  .\run_validation.ps1 -DeviceIP 192.168.29.164" -ForegroundColor Gray
    Write-Host "  .\run_validation.ps1 -DeviceIP 192.168.29.164 -Verbose" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Or use environment variable:" -ForegroundColor Yellow
    Write-Host "  `$env:RDK_DEVICE_IP = '192.168.29.164'" -ForegroundColor Gray
    Write-Host "  .\run_validation.ps1" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Parameters:" -ForegroundColor Yellow
    Write-Host "  -DeviceIP    Device IP address (required)" -ForegroundColor Gray
    Write-Host "  -SSHUser     SSH username (default: root)" -ForegroundColor Gray
    Write-Host "  -Verbose     Enable verbose output" -ForegroundColor Gray
    Write-Host "  -Help        Show this help message" -ForegroundColor Gray
    Write-Host ""
    exit 0
}

# Colors
$colorSuccess = "Green"
$colorError = "Red"
$colorWarning = "Yellow"
$colorInfo = "Cyan"

# Functions
function Write-Success {
    param([string]$Message)
    Write-Host "✓ $Message" -ForegroundColor $colorSuccess
}

function Write-Error {
    param([string]$Message)
    Write-Host "✗ $Message" -ForegroundColor $colorError
}

function Write-Warning {
    param([string]$Message)
    Write-Host "⚠ $Message" -ForegroundColor $colorWarning
}

function Write-Info {
    param([string]$Message)
    Write-Host "ℹ $Message" -ForegroundColor $colorInfo
}

function Write-Header {
    param([string]$Title)
    Write-Host ""
    Write-Host "=====================================================" -ForegroundColor Cyan
    Write-Host $Title -ForegroundColor Cyan
    Write-Host "=====================================================" -ForegroundColor Cyan
    Write-Host ""
}

# Main script
Write-Header "PackageManager Plugin Validator"

Write-Info "Device IP: $DeviceIP"
Write-Info "SSH User: $SSHUser"
Write-Info "Verbose: $Verbose"
Write-Host ""

# Check Bash
Write-Info "Checking for Bash..."
$bashPath = (Get-Command bash -ErrorAction SilentlyContinue)
if ($null -eq $bashPath) {
    Write-Error "Bash is not available"
    Write-Info "Please install: Git Bash, WSL, or MinGW"
    exit 1
}
Write-Success "Bash is available"

# Check SSH
Write-Info "Checking for SSH..."
$sshPath = (Get-Command ssh -ErrorAction SilentlyContinue)
if ($null -eq $sshPath) {
    Write-Warning "SSH is not available - device deployment may fail"
    Write-Info "For Windows 10+, SSH is built-in (may need system update)"
    Write-Info "For older Windows, install: Git Bash or PuTTY"
} else {
    Write-Success "SSH is available"
}

# Check device connectivity
Write-Info "Checking device connectivity..."
$pingTest = Test-Connection -ComputerName $DeviceIP -Count 1 -Quiet
if ($pingTest) {
    Write-Success "Device is reachable"
} else {
    Write-Warning "Cannot ping device at $DeviceIP"
    Write-Info "Device may still be available via SSH"
}

# Find script
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$validatorScript = Join-Path $scriptDir "validate_packagemanager_plugins.sh"

if (-not (Test-Path $validatorScript)) {
    Write-Error "Validator script not found at $validatorScript"
    Write-Info "Run this script from the same directory as validate_packagemanager_plugins.sh"
    exit 1
}
Write-Success "Validator script found"

# Run deployment
Write-Header "Deploying to Device"

Write-Info "Target: $SSHUser@$DeviceIP"
Write-Info "Executing validation script..."
Write-Host ""

$sshTarget = "$SSHUser@$DeviceIP"
if ($Verbose) {
    bash $validatorScript --deploy-to-device $sshTarget --verbose
} else {
    bash $validatorScript --deploy-to-device $sshTarget
}

$exitCode = $LASTEXITCODE

# Handle results
Write-Host ""
if ($exitCode -eq 0) {
    Write-Header "Validation Completed Successfully"
    
    $reportPath = Join-Path $scriptDir "plugin_validation_report_device.txt"
    if (Test-Path $reportPath) {
        Write-Success "Report saved to: $reportPath"
        Write-Host ""
        
        # Ask to open report
        Write-Host "Report contents:" -ForegroundColor Cyan
        Write-Host "======================" -ForegroundColor Cyan
        Get-Content $reportPath
        Write-Host "======================" -ForegroundColor Cyan
        Write-Host ""
        
        $response = Read-Host "Open report in Notepad? (y/n)"
        if ($response -eq "y" -or $response -eq "Y") {
            notepad $reportPath
        }
    }
} else {
    Write-Header "Validation Failed"
    Write-Error "Validation script exited with code: $exitCode"
    Write-Host ""
    Write-Info "Troubleshooting:"
    Write-Info "  1. Check device IP: $DeviceIP"
    Write-Info "  2. Verify device is powered on and on network"
    Write-Info "  3. Test connectivity: Test-Connection -ComputerName $DeviceIP"
    Write-Info "  4. Test SSH: ssh $sshTarget 'echo test'"
    Write-Info "  5. For more help, see: RUN_ON_RDK_DEVICE.md"
    Write-Info "  6. Run with -Verbose flag for detailed output"
    Write-Host ""
    exit 1
}

Write-Host "Done!" -ForegroundColor Green
