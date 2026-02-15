# Enhanced RDK Device Validation - Quick Guide

## What's New

The validation scripts now **automatically check and start Thunder services** if they're not running. This makes validation much more reliable!

---

## Quick Commands on RDK Device

### Option 1: Auto-Setup and Validate (Recommended)
```bash
# SSH into device
ssh root@192.168.29.164

# Download and run setup script
bash setup_and_validate.sh --auto-start --verbose

# This will:
# - Check Thunder service status
# - Auto-start if not running
# - Wait for service initialization
# - Test JSONRPC connectivity
# - List available plugins
# - Test PackageManager API
# - Generate status report
```

### Option 2: Manual Validation (No Auto-Start)
```bash
# SSH into device
ssh root@192.168.29.164

# Run validation script
./validate_packagemanager_plugins.sh --verbose
```

### Option 3: Check Status Only (No Validation)
```bash
# Check if Thunder is running
systemctl status wpeframework

# Start if not running
sudo systemctl start wpeframework

# Enable auto-start on boot
sudo systemctl enable wpeframework
```

---

## From Windows - Deploy and Run

### Using PowerShell
```powershell
cd D:\Project\TDK\testCodeRepo\tdk-core\framework\fileStore\testscriptsRDKV\component\DAC01\local_testing

# Deploy and run validation
bash ./validate_packagemanager_plugins.sh --deploy-to-device root@192.168.29.164 --verbose
```

### Using Git Bash
```bash
cd /d/Project/TDK/testCodeRepo/tdk-core/framework/fileStore/testscriptsRDKV/component/DAC01/local_testing

bash ./validate_packagemanager_plugins.sh --deploy-to-device root@192.168.29.164 --verbose
```

---

## What Gets Validated

### Service Status
- ✅ WPEFramework service status
- ✅ Auto-start if stopped
- ✅ Wait for initialization

### JSONRPC Connectivity
- ✅ Connection to 127.0.0.1:9998
- ✅ Valid response format
- ✅ System version retrieval

### Plugins
- ✅ org.rdk.PackageManagerRDKEMS availability
- ✅ org.rdk.PackageManager availability
- ✅ Plugin activation capability

### APIs
- ✅ getList API
- ✅ getStorageDetails API
- ✅ packageState API

---

## Output Files

### On RDK Device
```bash
# Status report
cat /tmp/rdk_device_status_report.txt

# Validation report (if run locally)
cat /tmp/plugin_validation_report.txt
```

### On Windows PC
```powershell
# Validation report retrieved from device
cat plugin_validation_report_device.txt

# Status report (if transferred)
cat rdk_device_status_report.txt
```

---

## Common Scenarios

### Scenario 1: First Time Setup
```bash
# On RDK Device
ssh root@192.168.29.164

# Run complete setup
bash setup_and_validate.sh --auto-start

# Enable auto-start for future boots
sudo systemctl enable wpeframework
```

### Scenario 2: Service Crashed, Need to Restart
```bash
# On RDK Device
ssh root@192.168.29.164

# Quick restart
sudo systemctl restart wpeframework

# Wait for startup
sleep 5

# Validate
./validate_packagemanager_plugins.sh
```

### Scenario 3: Deploy from Windows and Validate
```powershell
# From Windows PowerShell
cd local_testing
bash ./validate_packagemanager_plugins.sh --deploy-to-device root@192.168.29.164
```

---

## Enhanced Script Features

### New: Automatic Service Check
```bash
# validate_packagemanager_plugins.sh now includes:
# 1. Check if WPEFramework is running
# 2. If not: attempt to start it
# 3. Wait for initialization
# 4. Continue with validation
```

### New: Setup and Validate Script
```bash
# setup_and_validate.sh provides:
# 1. Service status checking
# 2. Auto-start capability
# 3. Plugin listing
# 4. API testing
# 5. Device status report
```

---

## Troubleshooting

### If services won't start
```bash
# Check service status
systemctl status wpeframework

# Check logs for errors
journalctl -u wpeframework -n 50 --no-pager

# Check if already running
ps aux | grep -i wpe

# Manual kill and restart
sudo killall WPEFramework
sudo systemctl start wpeframework
```

### If JSONRPC won't respond
```bash
# Check if listening on port 9998
netstat -tlnp | grep 9998
ss -tlnp | grep 9998

# Test connectivity
curl http://127.0.0.1:9998/jsonrpc

# Check network
ifconfig
ip addr show
```

### If plugin not found
```bash
# List available plugins
curl -X POST http://127.0.0.1:9998/jsonrpc \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"Controller.1.plugins","params":{}}'

# Check plugin directory
ls -la /usr/lib/wpeframework/plugins/ | grep -i package

# Check logs
journalctl -u wpeframework -f
```

---

## Script Files Summary

| File | Purpose | On Device |
|------|---------|-----------|
| validate_packagemanager_plugins.sh | Main validator (auto-starts services) | Run locally or deploy via SSH |
| setup_and_validate.sh | Complete setup + validation | Run locally on device |
| validate_packagemanager_local.py | Local environment checks | Run on Windows/Linux |
| run_validation.ps1 | Windows PowerShell launcher | Run on Windows |
| run_validation.bat | Windows batch launcher | Run on Windows |

---

## Command Reference

### Quick Validation (Auto)
```bash
bash setup_and_validate.sh --auto-start
```

### Verbose Validation
```bash
./validate_packagemanager_plugins.sh --verbose
```

### Service Check Only
```bash
systemctl status wpeframework
```

### Check and Auto-Start
```bash
sudo systemctl start wpeframework
sudo systemctl enable wpeframework
```

### View Reports
```bash
cat /tmp/rdk_device_status_report.txt
cat /tmp/plugin_validation_report.txt
```

### Deploy from Windows
```powershell
bash ./validate_packagemanager_plugins.sh --deploy-to-device root@192.168.29.164 --verbose
```

---

## Expected Output - Success

```
================================================
RDK Device Setup & Validation v1.0
================================================

ℹ Options: Auto-Start=true, Verbose=false

================================================
Checking Thunder/WPE Services
================================================

ℹ WPEFramework service found
✓ WPEFramework is RUNNING

================================================
Testing JSONRPC Connectivity
================================================

ℹ Testing connection to 127.0.0.1:9998...
✓ JSONRPC connection OK
ℹ System Version: lib32-application-test-image-RPI4-20251231114511

================================================
Testing PackageManager API
================================================

ℹ Testing getList API...
✓ getList API is functional

================================================
Generating Report
================================================

✓ Report saved to: /tmp/rdk_device_status_report.txt

================================================
Setup & Validation Complete
================================================

✓ Device is ready for PackageManager testing!
```

---

## Next Steps

1. **Quick Test**
   ```bash
   bash setup_and_validate.sh --auto-start
   ```

2. **Review Report**
   ```bash
   cat /tmp/rdk_device_status_report.txt
   ```

3. **Enable Auto-Start**
   ```bash
   sudo systemctl enable wpeframework
   ```

4. **Run Full TDK Tests**
   - Use test scripts in PackageManager directory
   - Or run via TDK framework

---

**Last Updated:** 2026-01-14  
**Script Version:** 1.0 with Auto-Service Management
