# PackageManager API Corrections - Summary Report

## Overview
The original test script (`validate_all_packagemanager_apis_v2.sh`) was using an incorrect or outdated API specification. A corrected version has been created based on the official RDK Central PackageManager API documentation.

**Official Documentation References:**
- API Reference: https://rdkcentral.github.io/entservices-apis/#/apis/PackageManager
- Wiki: https://github.com/rdkcentral/entservices-infra/wiki/Package-Manager

---

## Critical Issues Found and Fixed

### 1. Incorrect Method Namespace ❌→✅
**Original Script:**
```json
"method": "org.rdk.PackageManagerRDKEMS.download"
"method": "org.rdk.PackageManagerRDKEMS.pause"
"method": "org.rdk.PackageManagerRDKEMS.listPackages"
```

**Corrected Script:**
```json
"method": "org.rdk.PackageManager.download"
"method": "org.rdk.PackageManager.pause"
"method": "org.rdk.PackageManager.listPackages"
```

**Impact:** The "RDKEMS" suffix was not part of the real API. This caused all method calls to fail with "Unknown method" errors.

---

### 2. Non-existent and Misnaming Methods

#### a) `downloadLimit` → `rateLimit`
**Original:**
```json
{
    "method": "org.rdk.PackageManagerRDKEMS.downloadLimit",
    "params": {
        "limit": 512
    }
}
```

**Corrected:**
```json
{
    "method": "org.rdk.PackageManager.rateLimit",
    "params": {
        "downloadId": "handle123",
        "limit": 512
    }
}
```

**Changes:**
- Method name: `downloadLimit` → `rateLimit`
- Added required `downloadId` parameter
- Rate limit applies per download, not globally

#### b) `getProgress` with `downloadId` parameter issue
**The API has TWO different methods:**

1. **`progress`** - Takes `downloadId` parameter (for monitoring ongoing downloads)
2. **`getProgress`** - Takes `handle` parameter (for monitoring install/uninstall operations)

**Original Script used:**
```json
{
    "method": "org.rdk.PackageManagerRDKEMS.getProgress",
    "params": {
        "downloadId": "1012"
    }
}
```

**Corrected Script uses:**
```json
{
    "method": "org.rdk.PackageManager.progress",
    "params": {
        "downloadId": "handle123"
    }
}
```

---

### 3. Parameter Name and Type Changes

#### a) Download method returns `handle` not `downloadId`
**Original Script Expected:**
```json
{
    "result": {
        "downloadId": "1012"
    }
}
```

**Actual API Returns:**
```json
{
    "result": {
        "handle": "abc123def456"
    }
}
```

**Impact:** Script was looking for wrong field name, causing variable extraction failures.

#### b) Cancel method uses `handle` parameter, not `downloadId`
**Original:**
```json
{
    "method": "org.rdk.PackageManager.cancel",
    "params": {
        "downloadId": "1012"
    }
}
```

**Corrected:**
```json
{
    "method": "org.rdk.PackageManager.cancel",
    "params": {
        "handle": "abc123def456"
    }
}
```

#### c) Delete method uses `fileLocator` parameter, not `downloadId`
**Original:**
```json
{
    "method": "org.rdk.PackageManagerRDKEMS.delete",
    "params": {
        "downloadId": "1012"
    }
}
```

**Corrected:**
```json
{
    "method": "org.rdk.PackageManager.delete",
    "params": {
        "fileLocator": "/opt/CDL/package123"
    }
}
```

**Impact:** Delete operations were failing because the parameter was completely wrong.

---

### 4. Install Method Parameter Changes
**Original:**
```json
{
    "method": "org.rdk.PackageManagerRDKEMS.install",
    "params": {
        "packageId": "com.rdkcentral.cobalt",
        "version": "0.1.0",
        "fileLocator": "/opt/CDL/package1012"
    }
}
```

**Corrected:**
```json
{
    "method": "org.rdk.PackageManager.install",
    "params": {
        "type": "",
        "id": "com.rdkcentral.cobalt",
        "version": "0.1.0",
        "url": "/opt/CDL/package123",
        "appName": "Cobalt",
        "category": "media"
    }
}
```

**Changes:**
- `packageId` → `id`
- Added required `type` parameter (empty string for default)
- `fileLocator` → `url`
- Added required `appName` parameter
- Added required `category` parameter

---

### 5. Uninstall Method Parameter Changes
**Original:**
```json
{
    "method": "org.rdk.PackageManagerRDKEMS.uninstall",
    "params": {
        "packageId": "com.rdkcentral.cobalt"
    }
}
```

**Corrected:**
```json
{
    "method": "org.rdk.PackageManager.uninstall",
    "params": {
        "type": "",
        "id": "com.rdkcentral.cobalt",
        "version": "0.1.0",
        "uninstallType": "normal"
    }
}
```

**Changes:**
- `packageId` → `id`
- Added required `type` parameter
- Added required `version` parameter
- Added required `uninstallType` parameter

---

### 6. Lock/Unlock Methods Parameter Changes
**Original Lock:**
```json
{
    "method": "org.rdk.PackageManagerRDKEMS.lock",
    "params": {
        "packageId": "com.rdkcentral.cobalt"
    }
}
```

**Corrected Lock:**
```json
{
    "method": "org.rdk.PackageManager.lock",
    "params": {
        "type": "",
        "id": "com.rdkcentral.cobalt",
        "version": "0.1.0",
        "reason": "Launch",
        "owner": "AppManager"
    }
}
```

**Original Unlock (incorrect):**
```json
{
    "method": "org.rdk.PackageManagerRDKEMS.unlock",
    "params": {
        "packageId": "com.rdkcentral.cobalt"
    }
}
```

**Corrected Unlock:**
```json
{
    "method": "org.rdk.PackageManager.unlock",
    "params": {
        "handle": ""
    }
}
```

Note: Unlock uses a handle, not packageId.

---

### 7. Config Method Parameters
**Original:**
```json
{
    "method": "org.rdk.PackageManagerRDKEMS.config",
    "params": {
        "packageId": "com.rdkcentral.cobalt",
        "configKey": "testKey",
        "configValue": "testValue"
    }
}
```

**Corrected:**
```json
{
    "method": "org.rdk.PackageManager.config",
    "params": {
        "packageId": "com.rdkcentral.cobalt",
        "version": "0.1.0"
    }
}
```

**Impact:** Config retrieves configuration, not sets it. The original semantics were wrong.

---

### 8. GetConfigForPackage Method
**Original:**
```json
{
    "method": "org.rdk.PackageManagerRDKEMS.getConfigForPackage",
    "params": {
        "packageId": "com.rdkcentral.cobalt"
    }
}
```

**Corrected:**
```json
{
    "method": "org.rdk.PackageManager.getConfigForPackage",
    "params": {
        "fileLocator": "/opt/CDL/package123"
    }
}
```

**Changes:**
- Parameter changed from `packageId` to `fileLocator`
- This method requires the file path, not the package ID

---

## Summary of API Method Fixes

| Original Method | Corrected Method | Parameter Changes |
|---|---|---|
| `downloadLimit` | `rateLimit` | Added `downloadId`, kept `limit` |
| `getProgress` (with downloadId) | `progress` | Changed param from `downloadId` to proper download ID |
| `delete` | `delete` | Changed param from `downloadId` to `fileLocator` |
| `install` | `install` | `packageId`→`id`, `fileLocator`→`url`, added `type`, `appName`, `category` |
| `uninstall` | `uninstall` | `packageId`→`id`, added `type`, `version`, `uninstallType` |
| `lock` | `lock` | `packageId`→`id`, added `type`, `version`, `reason`, `owner` |
| `unlock` | `unlock` | Changed from `packageId` to `handle` |
| `getLockedInfo` | `getLockedInfo` | Kept `packageId` and `version` |
| `config` | `config` | Added required `version` parameter |
| `getConfigForPackage` | `getConfigForPackage` | `packageId`→`fileLocator` |
| All methods | All methods | Removed "RDKEMS" from namespace |

---

## Files

1. **Original (Broken):** `validate_all_packagemanager_apis_v2.sh`
2. **Corrected:** `validate_packagemanager_apis_corrected.sh`

## Next Steps

1. Use the corrected script for testing: `validate_packagemanager_apis_corrected.sh`
2. Verify the device has the correct PackageManager service running
3. Check service logs for any issues: `journalctl -u wpeframework-packagemanager.service`
4. Review error messages from failed tests to identify any remaining issues

---

## API Discovery Command

To verify available PackageManager methods on your device:

```bash
curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": "2.0", "id": 0, "method": "ServiceManager.getServiceDetails", "params": {"service": "org.rdk.PackageManager"}}' http://127.0.0.1:9998/jsonrpc
```

This will show all available methods in the actual API running on your device.
