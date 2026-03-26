# 🚀 Quick Start - Run Validation on RDK Device

## For Windows Users (Fastest Way)

### Option A: Using PowerShell (Recommended)
```powershell
# Set device IP
$env:RDK_DEVICE_IP = "192.168.29.164"

# Run validation
.\run_validation.ps1

# Or with specific IP
.\run_validation.ps1 -DeviceIP 192.168.29.164
```

### Option B: Using Command Prompt (Batch)
```cmd
# Navigate to script directory
cd D:\Project\TDK\testCodeRepo\tdk-core\framework\fileStore\testscriptsRDKV\component\DAC01\local_testing

# Run with device IP
run_validation.bat 192.168.29.164

# Or set environment variable first
set RDK_DEVICE_IP=192.168.29.164
run_validation.bat
```

### Option C: Using Git Bash
```bash
# If you have Git Bash installed
cd /d/Project/TDK/testCodeRepo/tdk-core/framework/fileStore/testscriptsRDKV/component/DAC01/local_testing

# Deploy to device
bash ./validate_packagemanager_plugins.sh --deploy-to-device root@192.168.29.164
```

---

## What Happens

1. ✅ Checks network connectivity to device
2. ✅ Verifies SSH is available
3. ✅ Copies script to device via SCP
4. ✅ Makes script executable
5. ✅ Executes validation on device
6. ✅ Retrieves results back to Windows
7. ✅ Displays validation report
8. ✅ Cleans up temporary files

---

## Output

After successful validation, you'll see:
- Console output showing validation progress
- `plugin_validation_report_device.txt` - Detailed validation results

---

## Troubleshooting

### If PowerShell Script Won't Run
```powershell
# Allow execution of unsigned scripts (one-time)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try again
.\run_validation.ps1 -DeviceIP 192.168.29.164
```

### If "ssh: command not found"
```powershell
# Check if SSH is available
ssh -V

# If not found:
# - Windows 10+: Update system (SSH is built-in)
# - Older Windows: Install Git Bash from https://git-scm.com/download/win
```

### If Device Not Reachable
```powershell
# Test connectivity
ping 192.168.29.164

# Test SSH directly
ssh root@192.168.29.164 "echo test"
```

### For Verbose Debugging
```powershell
# PowerShell version
.\run_validation.ps1 -DeviceIP 192.168.29.164 -Verbose

# Bash version
bash ./validate_packagemanager_plugins.sh --deploy-to-device root@192.168.29.164 --verbose
```

---

## Device IP Reference

**Common RDK Device IPs:**
- `192.168.1.100` - Typical home network
- `192.168.29.164` - Example from user
- `192.168.0.x` - Alternative home network
- `localhost:9998` - Local device
- Check device settings or ask your admin for actual IP

---

## File Structure

```
local_testing/
├── validate_packagemanager_plugins.sh    ← Main validation script
├── validate_packagemanager_local.py      ← Local environment checks
├── run_validation.ps1                    ← PowerShell launcher (Windows)
├── run_validation.bat                    ← Batch launcher (Windows)
├── RUN_ON_RDK_DEVICE.md                 ← Detailed guide
└── plugin_validation_report_device.txt   ← Output report (generated)
```

---

## One-Liners

```powershell
# PowerShell: Set IP and run
$env:RDK_DEVICE_IP="192.168.29.164"; .\run_validation.ps1

# Bash: Deploy to device
bash ./validate_packagemanager_plugins.sh --deploy-to-device root@192.168.29.164
```

---

## Next Steps After Validation

1. **If All Checks Pass** ✅
   - PackageManager is ready for testing
   - Run individual test scripts from PackageManager directory
   - Deploy full TDK test suite if available

2. **If Some Checks Fail** ⚠️
   - Review report for specific errors
   - Check device logs for details
   - Run with `--verbose` flag for more info

3. **For Full Testing**
   - Use TDK test framework for comprehensive testing
   - Scripts in PackageManager directory
   - Contact device admin for support

---

## Getting Help

1. **Check Report**: `plugin_validation_report_device.txt`
2. **Read Guide**: `RUN_ON_RDK_DEVICE.md`
3. **Detailed Info**: `README_VALIDATION_SCRIPTS.md`
4. **More Examples**: `INDEX.md`

---

**Estimated Time:** 30-60 seconds per validation run

**Last Updated:** 2026-01-14
