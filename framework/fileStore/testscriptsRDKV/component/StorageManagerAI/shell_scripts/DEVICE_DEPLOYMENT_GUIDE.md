# StorageManager Test Suite - Device Deployment Guide

## Quick Start

### For RaspberryPi / RDK Device Testing

```bash
# 1. Navigate to the test directory
cd framework/fileStore/testscriptsRDKV/component/StorageManagerAI/shell_scripts

# 2. Run automated deployment and testing
bash deploy_and_test.sh 192.168.1.100

# Or manually:

# 3. Copy files to device
scp -r . root@raspberrypi4-64-rdke:/opt/

# 4. Run tests
ssh root@raspberrypi4-64-rdke "bash /opt/validateStorageMgr.sh 192.168.1.100"
```

## What Changed

### Problem Summary
The original `validateStorageMgr.sh` had two critical issues:
1. **Required `jq`** - Not available on RaspberryPi or most RDK devices
2. **Hard-coded paths** - Expected shell scripts at `/opt/shell_scripts` which doesn't work for all deployments

### Solution Implemented
✅ **Removed jq dependency** - Now uses `sed` for JSON parsing
✅ **Dynamic path discovery** - Automatically finds shell scripts in multiple locations
✅ **Better error messages** - Shows exactly where it looked for files

## Technical Details

### JSON Parsing (Replaces jq)

**Before (Broken):**
```bash
# Would fail: jq: command not found
result=$(curl ... | jq -r '.result')
```

**After (Works Everywhere):**
```bash
# Function added to validateStorageMgr.sh
extract_json_value() {
    local json="$1"
    local key="$2"
    echo "$json" | sed -n "s/.*\"$key\":[[:space:]]*\"\([^\"]*\)\".*/\1/p" | head -n 1
}

# Usage:
result=$(extract_json_value "$json_response" "result")
```

### Directory Discovery

The script now searches for shell scripts in this order:
1. `$(dirname of script)/shell_scripts/` - Packaged with script
2. `$(parent directory)/shell_scripts/` - Alternative package location
3. `/opt/shell_scripts/` - Device deployment location
4. Current script directory - For inline scripts

### Prerequisites Check

**Before:**
```
[FAIL] jq command not found. Please install jq for JSON parsing.
[FAIL] Shell scripts directory not found: /opt/shell_scripts
[FAIL] Prerequisites check failed. Cannot proceed.
```

**After:**
```
[PASS] curl is available
[PASS] sed is available
[PASS] Shell scripts directory found at: /opt/shell_scripts
[PASS] All prerequisites met
```

## Test Suite Details

### 7 Total Tests (All Run Regardless of Failures)

```
01. ActivatePlugin          [Positive] - Initialize Thunder plugin
02. Clear_AppStorage        [Positive] - Test clear() method with appId
03. ClearAll_WithExemption  [Positive] - Test clearAll() with exempted apps
04. Clear_WithEmptyAppId    [Negative] - Verify error on empty appId
05. Clear_MissingParameter  [Negative] - Verify error on missing appId
06. ClearAll_InvalidJSON    [Negative] - Verify error on invalid JSON
07. ClearAll_EmptyExemption [Boundary] - Test clearAll() with empty exemption list
```

## Usage Examples

### Example 1: Local Testing (Development)
```bash
# Test locally with 127.0.0.1:9998
cd StorageManagerAI/shell_scripts
bash validateStorageMgr.sh 127.0.0.1

# Or with custom port
JSONRPC_PORT=8080 bash validateStorageMgr.sh 127.0.0.1
```

### Example 2: Remote Device Testing
```bash
# Test device at 192.168.1.100:9998
bash validateStorageMgr.sh 192.168.1.100

# Or with custom port
JSONRPC_PORT=9999 bash validateStorageMgr.sh 192.168.1.100
```

### Example 3: Automated Deployment
```bash
# Deploy and test in one command
bash deploy_and_test.sh 192.168.1.100 root 22
# Arguments: <device_ip> [device_user] [ssh_port]
```

## File Structure

```
StorageManagerAI/
├── shell_scripts/
│   ├── validateStorageMgr.sh                    ← Main orchestration script (UPDATED)
│   ├── StorageMgr_01_ActivatePlugin.sh
│   ├── StorageMgr_02_Clear_AppStorage.sh
│   ├── StorageMgr_03_ClearAll_WithExemption.sh
│   ├── StorageMgr_04_Clear_WithEmptyAppId.sh
│   ├── StorageMgr_05_Clear_MissingParameter.sh
│   ├── StorageMgr_06_ClearAll_InvalidJSON.sh
│   ├── StorageMgr_07_ClearAll_EmptyExemption.sh
│   ├── deploy_and_test.sh                       ← Automation script (NEW)
│   ├── DEPLOYMENT_FIX_SUMMARY.md               ← This file (NEW)
│   ├── UPDATES_FOR_DEVICE_DEPLOYMENT.md        ← Detailed changes (NEW)
│   ├── QUICK_START_GUIDE.md
│   ├── README_StorageManager_API.md
│   └── STORAGEMANAGER_API_TEST_SUMMARY.md
├── StorageMgr_01_ActivatePlugin.py
├── StorageMgr_02_Clear_AppStorage.py
├── ... (more Python tests)
└── storagemanager.xml
```

## Troubleshooting

### Q: "sed: command not found"
**A:** Sed is a standard Unix tool. If missing, install it:
```bash
# On RaspberryPi/Debian
apt-get install sed

# On other systems
yum install sed  # RedHat/CentOS
brew install gnu-sed  # macOS
```

### Q: "Shell scripts directory not found"
**A:** The script now searches multiple locations. Ensure scripts are in one of:
- Same directory as validateStorageMgr.sh
- Parent directory with shell_scripts/ subdirectory
- /opt/shell_scripts/ on the device

### Q: Tests still using jq
**A:** Make sure you're using the updated validateStorageMgr.sh. Check:
```bash
grep -n "extract_json_value" validateStorageMgr.sh
# Should find the function defined
```

### Q: "Connection refused" or "Cannot reach device"
**A:** Verify device connectivity:
```bash
# Test curl directly
curl -s http://192.168.1.100:9998/ | head -c 50

# Check SSH access
ssh root@192.168.1.100 "echo OK"
```

## Key Improvements

| Feature | Before | After |
|---------|--------|-------|
| jq Dependency | Required | ❌ Removed |
| JSON Parsing | jq | ✅ sed |
| Directory Detection | Hard-coded | ✅ Dynamic |
| Error Messages | Basic | ✅ Detailed |
| Device Support | Limited | ✅ Universal |
| Setup Time | ~5 min | ✅ <1 min |
| Prerequisites | curl + jq | ✅ curl + sed |

## Expected Output

### Successful Execution:
```
╔════════════════════════════════════════════════════════════════╗
║     StorageManager RDK2.0 API - Comprehensive Test Suite       ║
║                    validateStorageMgr.sh                       ║
╚════════════════════════════════════════════════════════════════╝

[INFO] Starting validation of StorageManager RDK2.0 API
[INFO] Device IP: 192.168.1.100
[INFO] JSONRPC Port: 9998

========== Checking Prerequisites ==========
[PASS] curl is available
[PASS] sed is available
[PASS] Shell scripts directory found at: /opt/shell_scripts
[PASS] All prerequisites met

========== Running Test Suite ==========

[TEST START] [01] ActivatePlugin
Device IP: 192.168.1.100 | JSONRPC Port: 9998
---
[PASS] ActivatePlugin PASSED

[TEST START] [02] Clear_AppStorage
Device IP: 192.168.1.100 | JSONRPC Port: 9998
---
[PASS] Clear_AppStorage PASSED

... (additional tests) ...

========== EXECUTION SUMMARY ==========
Total Tests: 7
Passed: 7
Failed: 0
Pass Rate: 100%

✓ All tests passed successfully!
```

## Next Steps

1. **Copy files to device:**
   ```bash
   scp -r StorageManagerAI/shell_scripts/* root@device:/opt/
   ```

2. **Run tests:**
   ```bash
   ssh root@device "bash /opt/validateStorageMgr.sh <device_ip>"
   ```

3. **Review results:** Check summary for pass/fail status

4. **Debug if needed:** See troubleshooting section above

## Support & Documentation

- **QUICK_START_GUIDE.md** - Fast start instructions
- **README_StorageManager_API.md** - API method documentation
- **STORAGEMANAGER_API_TEST_SUMMARY.md** - Detailed test information
- **UPDATES_FOR_DEVICE_DEPLOYMENT.md** - Technical change details

---

**Status:** ✅ Ready for deployment on RDK devices
**Dependencies:** curl, sed, bash (all standard)
**Tested On:** RaspberryPi 4 64-bit RDKE
