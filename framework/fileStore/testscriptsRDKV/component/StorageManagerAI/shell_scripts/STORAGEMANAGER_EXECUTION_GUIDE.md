# StorageManager Test Execution Guide

## Device Information
- **IP Address**: 192.168.29.164
- **Device Type**: Raspberry Pi 4 (RPI-Client) - aarch64 Linux
- **Status**: ✓ SSH accessible, network connectivity confirmed (ping to www.google.com successful)
- **Available Tools**: curl, bash shell, tar

## Environment Status
- ❌ Python not installed on device (no Python 2/3 found)
- ✓ TDK test framework location: `/opt/` (various test scripts present)
- ✓ Shell scripts available: 
  - `/opt/validateStorageMgr.sh` - Main validation script (already on device)
  - `/opt/testDownloadManager.sh`
  - `/opt/dac01Test.sh`
  - `/opt/verifyLifecycleMgr.sh`
  - `/opt/collectLogs.sh`

## StorageManager Test Components

### Available Python Test Scripts (Local Development)
Located at: `d:\Project\TDK\testCodeRepo\tdk-core\framework\fileStore\testscriptsRDKV\component\StorageManagerAI\`

1. **StorageMgr_01_ActivatePlugin.py** - Activate StorageManager plugin
2. **StorageMgr_02_Clear_AppStorage.py** - Clear application storage
3. **StorageMgr_03_ClearAll_WithExemption.py** - Clear all with exemption list
4. **StorageMgr_04_Clear_WithEmptyAppId.py** - Negative test: empty appId
5. **StorageMgr_05_Clear_MissingParameter.py** - Negative test: missing parameter
6. **StorageMgr_06_ClearAll_InvalidJSON.py** - Negative test: invalid JSON
7. **StorageMgr_07_ClearAll_EmptyExemption.py** - Boundary test: empty exemption
8. **StorageMgr_08_Clear_InvalidAppId.py** - Negative test: invalid appId
9. **StorageMgr_09_ClearAll_MissingParameter.py** - Negative test: clearAll missing parameter
10. **StorageMgr_10_ClearAll_MultipleExemptions.py** - Multiple exemptions
11. **StorageMgr_11_Clear_LongAppId.py** - Long appId test
12. **StorageManagerUtils.py** - Utility functions for all tests

### Shell Script Available on Device
**`/opt/validateStorageMgr.sh`** - Self-contained validation script (does NOT require Python)
- All tests run regardless of individual failures
- Uses curl and sed for JSON parsing
- Tests covered:
  1. ActivatePlugin
  2. Clear AppStorage
  3. ClearAll WithExemption
  4. Clear WithEmptyAppId (Negative)
  5. Clear MissingParameter (Negative)
  6. ClearAll InvalidJSON (Negative)
  7. ClearAll EmptyExemption (Boundary)

## Execution Methods

### Method 1: Execute Shell Script on Remote Device (RECOMMENDED)
```bash
ssh root@192.168.29.164 "/opt/validateStorageMgr.sh 192.168.29.164"
```

**Advantages**:
- No Python dependency required
- Self-contained validation
- All test logic embedded in script
- Comprehensive test coverage
- Color-coded output with summary

**Requirements**:
- curl (✓ available)
- bash shell (✓ available)
- sed (standard utility)

### Method 2: Run Python Tests Locally (Requires TDK Framework)
These scripts require the TDK (Thunder Development Kit) framework to be set up locally with proper Python environment.

```bash
# From local machine with Python and TDK framework:
cd d:\Project\TDK\testCodeRepo\tdk-core\framework\fileStore\testscriptsRDKV\component\StorageManagerAI
python StorageMgr_01_ActivatePlugin.py 192.168.29.164 9998
python StorageMgr_02_Clear_AppStorage.py 192.168.29.164 9998
# ... etc for each test
```

### Method 3: Manual JSONRPC Calls
Direct API testing without scripts:

```bash
# Test 1: Check plugin status
ssh root@192.168.29.164 'curl -s -H "Content-Type: application/json" \
  --data "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"Controller.status@org.rdk.StorageManager\",\"params\":{}}" \
  "http://localhost:9998/jsonrpc"'

# Test 2: Activate plugin
ssh root@192.168.29.164 'curl -s -H "Content-Type: application/json" \
  --data "{\"jsonrpc\":\"2.0\",\"id\":2,\"method\":\"Controller.activate@org.rdk.StorageManager\",\"params\":{}}" \
  "http://localhost:9998/jsonrpc"'

# Test 3: Clear AppStorage
ssh root@192.168.29.164 'curl -s -H "Content-Type: application/json" \
  --data "{\"jsonrpc\":\"2.0\",\"id\":3,\"method\":\"org.rdk.StorageManager.clear\",\"params\":{\"appId\":\"com.example.testapp\"}}" \
  "http://localhost:9998/jsonrpc"'

# Test 4: ClearAll with exemption
ssh root@192.168.29.164 'curl -s -H "Content-Type: application/json" \
  --data "{\"jsonrpc\":\"2.0\",\"id\":4,\"method\":\"org.rdk.StorageManager.clearAll\",\"params\":{\"exempt\":[\"org.rdk.system\"]}}" \
  "http://localhost:9998/jsonrpc"'
```

## JSONRPC Service Connectivity

**Important**: The JSONRPC service must be running on the device at `http://localhost:9998/jsonrpc`

To verify service is running:
```bash
ssh root@192.168.29.164 "ss -tlnp | grep 9998" # or "netstat -tlnp | grep 9998"
ssh root@192.168.29.164 "ps aux | grep -i thunder"
```

## Expected Response Examples

### Successful Plugin Status
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "state": "ACTIVATED",
    "success": true
  }
}
```

### Clear Operation Success
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "success": true,
    "description": "Storage cleared for com.example.testapp"
  }
}
```

### Error Response (Missing Parameter)
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32602,
    "message": "Invalid params - appId is required"
  }
}
```

## Test Coverage Summary

| Test # | Name | Type | Purpose |
|--------|------|------|---------|
| 01 | ActivatePlugin | Positive | Activate StorageManager plugin |
| 02 | Clear_AppStorage | Positive | Clear specific app storage |
| 03 | ClearAll_WithExemption | Positive | Clear all except exempt apps |
| 04 | Clear_WithEmptyAppId | Negative | Test empty appId handling |
| 05 | Clear_MissingParameter | Negative | Test missing appId parameter |
| 06 | ClearAll_InvalidJSON | Negative | Test invalid JSON handling |
| 07 | ClearAll_EmptyExemption | Boundary | Test empty exemption array |
| 08 | Clear_InvalidAppId | Negative | Test invalid appId |
| 09 | ClearAll_MissingParameter | Negative | Test missing exempt parameter |
| 10 | ClearAll_MultipleExemptions | Positive | Test multiple exemptions |
| 11 | Clear_LongAppId | Boundary | Test long appId string |

## Troubleshooting

### Issue: "Connection refused" on port 9998
**Solution**: Verify Thunder/JSONRPC service is running on the device
```bash
ssh root@192.168.29.164 "systemctl status thunder" # or check relevant service
```

### Issue: "StorageManager plugin not found"
**Solution**: Check plugin is deployed and available
```bash
ssh root@192.168.29.164 "ls -la /usr/lib/rdk/plugins/" # Or appropriate plugin path
```

### Issue: SSH banner delays
**Solution**: The device outputs a welcome banner which may delay responses. This is normal.

### Issue: Python not available on device
**Solution**: Use the shell script method (`validateStorageMgr.sh`) which doesn't require Python

## Next Steps

1. **Execute validation script**:
   ```bash
   ssh root@192.168.29.164 "/opt/validateStorageMgr.sh 192.168.29.164"
   ```

2. **Review output** for test results and any failures

3. **Investigate failures** using manual JSONRPC calls (Method 3) for debugging

4. **Collect logs** if needed:
   ```bash
   ssh root@192.168.29.164 "/opt/collectLogs.sh"
   ```

## Files Reference

- Main validation script: [validateStorageMgr.sh](./validateStorageMgr.sh)
- Python test utilities: [StorageManagerUtils.py](../StorageManagerUtils.py)
- API coverage docs: [STORAGE_MANAGER_API_COVERAGE.md](../STORAGE_MANAGER_API_COVERAGE.md)

## Python Scripts Status

All Python test scripts have been verified for:
- ✓ Correct syntax - No syntax errors
- ✓ TDK placeholders - Properly configured with `ip = <ipaddress>` and `port = <port>`
- ✓ Required imports - All dependencies properly imported
- ✓ Logical flow - Scripts follow correct test execution patterns
- ✓ Error handling - Proper exception handling implemented

The scripts are ready for execution within the TDK framework.

---
**Generated**: January 1, 2026
**Device**: RPI-Client (192.168.29.164)
**Status**: Ready for execution
