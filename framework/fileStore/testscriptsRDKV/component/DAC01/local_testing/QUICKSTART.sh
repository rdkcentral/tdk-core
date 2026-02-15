#!/bin/bash

##########################################################################
# Quick Start Guide - PackageManager Plugin Validation
# 
# This script demonstrates basic usage of validation scripts
##########################################################################

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "=================================================="
echo "PackageManager Plugin Validation - Quick Start"
echo "=================================================="
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Available Validation Scripts:${NC}"
echo ""
echo "1. validate_packagemanager_local.py"
echo "   - Local environment validation (no device required)"
echo "   - Checks: configuration, scripts, dependencies, APIs"
echo ""
echo "2. validate_packagemanager_plugins.sh"
echo "   - Device-side plugin validation (requires RDK device)"
echo "   - Checks: connectivity, plugin activation, API functionality"
echo ""
echo "3. README_VALIDATION_SCRIPTS.md"
echo "   - Complete documentation with examples"
echo ""

echo -e "${BLUE}Quick Start Examples:${NC}"
echo ""

echo "Step 1: Validate local environment (No device needed)"
echo "  Run: python3 validate_packagemanager_local.py"
echo ""

echo "Step 2: Validate device plugins (Device required)"
echo "  Run: ./validate_packagemanager_plugins.sh -h <device-ip>"
echo ""

echo "Step 3: Review validation reports"
echo "  - plugin_validation_report_local.json"
echo "  - plugin_validation_report.txt"
echo ""

echo -e "${BLUE}Full Usage Examples:${NC}"
echo ""

echo "Local Validation:"
echo "  # All checks"
echo "  python3 validate_packagemanager_local.py"
echo ""
echo "  # Specific checks"
echo "  python3 validate_packagemanager_local.py --check-config"
echo "  python3 validate_packagemanager_local.py --check-scripts"
echo "  python3 validate_packagemanager_local.py --check-deps"
echo ""
echo "  # With verbose output"
echo "  python3 validate_packagemanager_local.py --verbose"
echo ""

echo "Device Validation:"
echo "  # Connect to localhost (default)"
echo "  ./validate_packagemanager_plugins.sh"
echo ""
echo "  # Connect to specific device"
echo "  ./validate_packagemanager_plugins.sh -h 192.168.1.100"
echo ""
echo "  # Custom port"
echo "  ./validate_packagemanager_plugins.sh -h 192.168.1.100 -p 9998"
echo ""
echo "  # Verbose output"
echo "  ./validate_packagemanager_plugins.sh -h 192.168.1.100 --verbose"
echo ""

echo -e "${GREEN}=================================================="
echo "For more details, see: README_VALIDATION_SCRIPTS.md"
echo "==================================================${NC}"
