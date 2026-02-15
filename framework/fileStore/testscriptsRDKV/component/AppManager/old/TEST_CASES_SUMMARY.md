# AppManager Test Cases Summary

## Overview
This document lists all 34 AppManager test cases for RDKV (RDK Video) component. Each test file follows the naming pattern `RDKV_AppManager_XX_<ApiName>_<TestType>.py` and contains XML metadata defining the test case details.

**Total Test Count: 34 tests**
**API Interface: org.rdk.AppManager.1.***
**Test Stub Interface: librdkservicesstub.so**
**Supported Box Types: RPI-Client, Video_Accelerator**
**RDK Version: RDK2.0**

---

## Test Cases by Category

### 1. Plugin Activation (1 test)

| # | Test ID | Test Case Name | File Name | Type | API Method | Test Objective |
|---|---------|----------------|-----------|------|------------|-----------------|
| 01 | TC_AppManager_activate | RDKV_AppManager_01_Activate | RDKV_AppManager_01_Activate.py | Activation | org.rdk.AppManager.1.activate | Test AppManager activate API - Activation scenarios |

**Key Assertions:** activate API should return appropriate responses for Activation scenarios

---

### 2. App Launching (4 tests)

| # | Test ID | Test Case Name | File Name | Type | API Method | Test Objective |
|---|---------|----------------|-----------|------|------------|-----------------|
| 02 | TC_AppManager_launchApp | RDKV_AppManager_02_LaunchApp_Positive | RDKV_AppManager_02_LaunchApp_Positive.py | Positive | org.rdk.AppManager.1.launchApp | Test AppManager launchApp API - Positive scenarios |
| 03 | TC_AppManager_launchApp | RDKV_AppManager_03_LaunchApp_Negative | RDKV_AppManager_03_LaunchApp_Negative.py | Negative | org.rdk.AppManager.1.launchApp | Test AppManager launchApp API - Negative scenarios |

**Key Assertions:** 
- Positive: launchApp API should return appropriate responses for valid launch parameters
- Negative: launchApp API should handle error conditions and invalid parameters appropriately

---

### 3. App Preloading (2 tests)

| # | Test ID | Test Case Name | File Name | Type | API Method | Test Objective |
|---|---------|----------------|-----------|------|------------|-----------------|
| 04 | TC_AppManager_preloadApp | RDKV_AppManager_04_PreloadApp_Positive | RDKV_AppManager_04_PreloadApp_Positive.py | Positive | org.rdk.AppManager.1.preloadApp | Test AppManager preloadApp API - Positive scenarios |
| 05 | TC_AppManager_preloadApp | RDKV_AppManager_05_PreloadApp_Negative | RDKV_AppManager_05_PreloadApp_Negative.py | Negative | org.rdk.AppManager.1.preloadApp | Test AppManager preloadApp API - Negative scenarios |

**Key Assertions:**
- Positive: preloadApp API should return appropriate responses for preloading apps
- Negative: preloadApp API should handle invalid apps and error conditions

---

### 4. App Closing (2 tests)

| # | Test ID | Test Case Name | File Name | Type | API Method | Test Objective |
|---|---------|----------------|-----------|------|------------|-----------------|
| 06 | TC_AppManager_closeApp | RDKV_AppManager_06_CloseApp_Positive | RDKV_AppManager_06_CloseApp_Positive.py | Positive | org.rdk.AppManager.1.closeApp | Test AppManager closeApp API - Positive scenarios |
| 07 | TC_AppManager_closeApp | RDKV_AppManager_07_CloseApp_Negative | RDKV_AppManager_07_CloseApp_Negative.py | Negative | org.rdk.AppManager.1.closeApp | Test AppManager closeApp API - Negative scenarios |

**Key Assertions:**
- Positive: closeApp API should successfully close running apps
- Negative: closeApp API should handle non-existent or already-closed apps

---

### 5. App Termination (2 tests)

| # | Test ID | Test Case Name | File Name | Type | API Method | Test Objective |
|---|---------|----------------|-----------|------|------------|-----------------|
| 08 | TC_AppManager_terminateApp | RDKV_AppManager_08_TerminateApp_Positive | RDKV_AppManager_08_TerminateApp_Positive.py | Positive | org.rdk.AppManager.1.terminateApp | Test AppManager terminateApp API - Positive scenarios |
| 09 | TC_AppManager_terminateApp | RDKV_AppManager_09_TerminateApp_Negative | RDKV_AppManager_09_TerminateApp_Negative.py | Negative | org.rdk.AppManager.1.terminateApp | Test AppManager terminateApp API - Negative scenarios |

**Key Assertions:**
- Positive: terminateApp API should forcefully terminate apps
- Negative: terminateApp API should handle invalid app IDs and error conditions

---

### 6. App Killing (2 tests)

| # | Test ID | Test Case Name | File Name | Type | API Method | Test Objective |
|---|---------|----------------|-----------|------|------------|-----------------|
| 10 | TC_AppManager_killApp | RDKV_AppManager_10_KillApp_Positive | RDKV_AppManager_10_KillApp_Positive.py | Positive | org.rdk.AppManager.1.killApp | Test AppManager killApp API - Positive scenarios |
| 11 | TC_AppManager_killApp | RDKV_AppManager_11_KillApp_Negative | RDKV_AppManager_11_KillApp_Negative.py | Negative | org.rdk.AppManager.1.killApp | Test AppManager killApp API - Negative scenarios |

**Key Assertions:**
- Positive: killApp API should immediately kill running apps
- Negative: killApp API should handle non-existent apps and invalid parameters

---

### 7. Installation Status (2 tests)

| # | Test ID | Test Case Name | File Name | Type | API Method | Test Objective |
|---|---------|----------------|-----------|------|------------|-----------------|
| 12 | TC_AppManager_isInstalled | RDKV_AppManager_12_IsInstalled_Positive | RDKV_AppManager_12_IsInstalled_Positive.py | Positive | org.rdk.AppManager.1.isInstalled | Test AppManager isInstalled API - Positive scenarios |
| 13 | TC_AppManager_isInstalled | RDKV_AppManager_13_IsInstalled_Negative | RDKV_AppManager_13_IsInstalled_Negative.py | Negative | org.rdk.AppManager.1.isInstalled | Test AppManager isInstalled API - Negative scenarios |

**Key Assertions:**
- Positive: isInstalled API should correctly identify installed apps
- Negative: isInstalled API should return false for non-existent apps

---

### 8. App Enumeration/Query (2 tests)

| # | Test ID | Test Case Name | File Name | Type | API Method | Test Objective |
|---|---------|----------------|-----------|------|------------|-----------------|
| 14 | TC_AppManager_getInstalledApps | RDKV_AppManager_14_GetInstalledApps | RDKV_AppManager_14_GetInstalledApps.py | Query | org.rdk.AppManager.1.getInstalledApps | Test AppManager getInstalledApps API - Query scenarios |
| 15 | TC_AppManager_getLoadedApps | RDKV_AppManager_15_GetLoadedApps | RDKV_AppManager_15_GetLoadedApps.py | Query | org.rdk.AppManager.1.getLoadedApps | Test AppManager getLoadedApps API - Query scenarios |

**Key Assertions:**
- getInstalledApps: Should return list of all installed applications with proper structure
- getLoadedApps: Should return list of currently loaded/running applications

---

### 9. Intent Sending (2 tests)

| # | Test ID | Test Case Name | File Name | Type | API Method | Test Objective |
|---|---------|----------------|-----------|------|------------|-----------------|
| 16 | TC_AppManager_sendIntent | RDKV_AppManager_16_SendIntent_Positive | RDKV_AppManager_16_SendIntent_Positive.py | Positive | org.rdk.AppManager.1.sendIntent | Test AppManager sendIntent API - Positive scenarios |
| 17 | TC_AppManager_sendIntent | RDKV_AppManager_17_SendIntent_Negative | RDKV_AppManager_17_SendIntent_Negative.py | Negative | org.rdk.AppManager.1.sendIntent | Test AppManager sendIntent API - Negative scenarios |

**Key Assertions:**
- Positive: sendIntent API should send intents to apps successfully
- Negative: sendIntent API should handle invalid intents and non-existent apps

---

### 10. System App Management (4 tests)

| # | Test ID | Test Case Name | File Name | Type | API Method | Test Objective |
|---|---------|----------------|-----------|------|------------|-----------------|
| 18 | TC_AppManager_startSystemApp | RDKV_AppManager_18_StartSystemApp_Positive | RDKV_AppManager_18_StartSystemApp_Positive.py | Positive | org.rdk.AppManager.1.startSystemApp | Test AppManager startSystemApp API - Positive scenarios |
| 19 | TC_AppManager_startSystemApp | RDKV_AppManager_19_StartSystemApp_Negative | RDKV_AppManager_19_StartSystemApp_Negative.py | Negative | org.rdk.AppManager.1.startSystemApp | Test AppManager startSystemApp API - Negative scenarios |
| 20 | TC_AppManager_stopSystemApp | RDKV_AppManager_20_StopSystemApp_Positive | RDKV_AppManager_20_StopSystemApp_Positive.py | Positive | org.rdk.AppManager.1.stopSystemApp | Test AppManager stopSystemApp API - Positive scenarios |
| 21 | TC_AppManager_stopSystemApp | RDKV_AppManager_21_StopSystemApp_Negative | RDKV_AppManager_21_StopSystemApp_Negative.py | Negative | org.rdk.AppManager.1.stopSystemApp | Test AppManager stopSystemApp API - Negative scenarios |

**Key Assertions:**
- startSystemApp Positive: Should start system apps successfully
- startSystemApp Negative: Should handle invalid system apps and error conditions
- stopSystemApp Positive: Should stop system apps successfully
- stopSystemApp Negative: Should handle invalid system apps and error conditions

---

### 11. App Data Management (3 tests)

| # | Test ID | Test Case Name | File Name | Type | API Method | Test Objective |
|---|---------|----------------|-----------|------|------------|-----------------|
| 22 | TC_AppManager_clearAppData | RDKV_AppManager_22_ClearAppData_Positive | RDKV_AppManager_22_ClearAppData_Positive.py | Positive | org.rdk.AppManager.1.clearAppData | Test AppManager clearAppData API - Positive scenarios |
| 23 | TC_AppManager_clearAppData | RDKV_AppManager_23_ClearAppData_Negative | RDKV_AppManager_23_ClearAppData_Negative.py | Negative | org.rdk.AppManager.1.clearAppData | Test AppManager clearAppData API - Negative scenarios |
| 24 | TC_AppManager_clearAllAppData | RDKV_AppManager_24_ClearAllAppData | RDKV_AppManager_24_ClearAllAppData.py | Query | org.rdk.AppManager.1.clearAllAppData | Test AppManager clearAllAppData API - Query scenarios |

**Key Assertions:**
- clearAppData Positive: Should clear app-specific data successfully
- clearAppData Negative: Should handle invalid apps and error conditions
- clearAllAppData: Should clear all app data from the system

---

### 12. App Metadata (2 tests)

| # | Test ID | Test Case Name | File Name | Type | API Method | Test Objective |
|---|---------|----------------|-----------|------|------------|-----------------|
| 25 | TC_AppManager_getAppMetadata | RDKV_AppManager_25_GetAppMetadata_Positive | RDKV_AppManager_25_GetAppMetadata_Positive.py | Positive | org.rdk.AppManager.1.getAppMetadata | Test AppManager getAppMetadata API - Positive scenarios |
| 26 | TC_AppManager_getAppMetadata | RDKV_AppManager_26_GetAppMetadata_Negative | RDKV_AppManager_26_GetAppMetadata_Negative.py | Negative | org.rdk.AppManager.1.getAppMetadata | Test AppManager getAppMetadata API - Negative scenarios |

**Key Assertions:**
- Positive: getAppMetadata should retrieve app metadata (name, version, icon, etc.)
- Negative: getAppMetadata should handle non-existent apps appropriately

---

### 13. App Properties (2 tests)

| # | Test ID | Test Case Name | File Name | Type | API Method | Test Objective |
|---|---------|----------------|-----------|------|------------|-----------------|
| 27 | TC_AppManager_getAppProperty | RDKV_AppManager_27_GetAppProperty_Positive | RDKV_AppManager_27_GetAppProperty_Positive.py | Positive | org.rdk.AppManager.1.getAppProperty | Test AppManager getAppProperty API - Positive scenarios |
| 28 | TC_AppManager_getAppProperty | RDKV_AppManager_28_GetAppProperty_Negative | RDKV_AppManager_28_GetAppProperty_Negative.py | Negative | org.rdk.AppManager.1.getAppProperty | Test AppManager getAppProperty API - Negative scenarios |

**Key Assertions:**
- getAppProperty Positive: Should retrieve app properties (state, priority, etc.)
- getAppProperty Negative: Should handle invalid properties and non-existent apps

---

### 14. App Property Setting (2 tests)

| # | Test ID | Test Case Name | File Name | Type | API Method | Test Objective |
|---|---------|----------------|-----------|------|------------|-----------------|
| 29 | TC_AppManager_setAppProperty | RDKV_AppManager_29_SetAppProperty_Positive | RDKV_AppManager_29_SetAppProperty_Positive.py | Positive | org.rdk.AppManager.1.setAppProperty | Test AppManager setAppProperty API - Positive scenarios |
| 30 | TC_AppManager_setAppProperty | RDKV_AppManager_30_SetAppProperty_Negative | RDKV_AppManager_30_SetAppProperty_Negative.py | Negative | org.rdk.AppManager.1.setAppProperty | Test AppManager setAppProperty API - Negative scenarios |

**Key Assertions:**
- Positive: setAppProperty should set app properties successfully
- Negative: setAppProperty should handle invalid properties and values

---

### 15. Resource Limit Properties (4 tests)

| # | Test ID | Test Case Name | File Name | Type | API Method | Test Objective |
|---|---------|----------------|-----------|------|------------|-----------------|
| 31 | TC_AppManager_getMaxRunningApps | RDKV_AppManager_31_GetMaxRunningApps | RDKV_AppManager_31_GetMaxRunningApps.py | Property | org.rdk.AppManager.1.getMaxRunningApps | Test AppManager getMaxRunningApps API - Property scenarios |
| 32 | TC_AppManager_getMaxHibernatedApps | RDKV_AppManager_32_GetMaxHibernatedApps | RDKV_AppManager_32_GetMaxHibernatedApps.py | Property | org.rdk.AppManager.1.getMaxHibernatedApps | Test AppManager getMaxHibernatedApps API - Property scenarios |
| 33 | TC_AppManager_getMaxHibernatedFlashUsage | RDKV_AppManager_33_GetMaxHibernatedFlashUsage | RDKV_AppManager_33_GetMaxHibernatedFlashUsage.py | Property | org.rdk.AppManager.1.getMaxHibernatedFlashUsage | Test AppManager getMaxHibernatedFlashUsage API - Property scenarios |
| 34 | TC_AppManager_getMaxInactiveRamUsage | RDKV_AppManager_34_GetMaxInactiveRamUsage | RDKV_AppManager_34_GetMaxInactiveRamUsage.py | Property | org.rdk.AppManager.1.getMaxInactiveRamUsage | Test AppManager getMaxInactiveRamUsage API - Property scenarios |

**Key Assertions:**
- getMaxRunningApps: Should return the maximum number of apps that can run simultaneously
- getMaxHibernatedApps: Should return the maximum number of hibernated apps
- getMaxHibernatedFlashUsage: Should return the maximum hibernation flash storage limit
- getMaxInactiveRamUsage: Should return the maximum inactive RAM usage limit

---

## Test Type Distribution

| Test Type | Count | Purpose |
|-----------|-------|---------|
| **Positive** | 16 | Verify normal operation with valid inputs |
| **Negative** | 12 | Verify error handling with invalid inputs |
| **Query** | 3 | Retrieve information from the system |
| **Property** | 4 | Test read-only or system property APIs |
| **Activation** | 1 | Test plugin activation/initialization |
| **TOTAL** | **36** | - |

---

## API Method Coverage

| API Method | Count | Types | Status |
|------------|-------|-------|--------|
| **activate** | 1 | Activation | Core |
| **launchApp** | 2 | Positive, Negative | Core |
| **preloadApp** | 2 | Positive, Negative | Core |
| **closeApp** | 2 | Positive, Negative | Core |
| **terminateApp** | 2 | Positive, Negative | Core |
| **killApp** | 2 | Positive, Negative | Core |
| **isInstalled** | 2 | Positive, Negative | Query |
| **getInstalledApps** | 1 | Query | Query |
| **getLoadedApps** | 1 | Query | Query |
| **sendIntent** | 2 | Positive, Negative | IPC |
| **startSystemApp** | 2 | Positive, Negative | System Apps |
| **stopSystemApp** | 2 | Positive, Negative | System Apps |
| **clearAppData** | 2 | Positive, Negative | Data Mgmt |
| **clearAllAppData** | 1 | Query | Data Mgmt |
| **getAppMetadata** | 2 | Positive, Negative | Metadata |
| **getAppProperty** | 2 | Positive, Negative | Properties |
| **setAppProperty** | 2 | Positive, Negative | Properties |
| **getMaxRunningApps** | 1 | Property | Resources |
| **getMaxHibernatedApps** | 1 | Property | Resources |
| **getMaxHibernatedFlashUsage** | 1 | Property | Resources |
| **getMaxInactiveRamUsage** | 1 | Property | Resources |

---

## Common Test Validations

All test cases follow a standardized validation approach:

1. **Response Structure Verification**: Ensures API returns properly formatted responses
2. **Error Handling**: Validates appropriate error responses for invalid inputs
3. **State Verification**: Confirms app state changes after API calls
4. **Data Integrity**: Validates returned data accuracy and completeness
5. **Status Codes**: Verifies correct success/failure status codes

---

## Prerequisites for All Tests

1. TDK Agent should be up and running
2. AppManager plugin should be available and activated
3. Device should have required applications installed
4. RDK device with AppManager plugin enabled (RPI-Client or Video_Accelerator)
5. Test stub interface (librdkservicesstub.so) available

---

## Test Execution Information

- **Execution Time**: 60 seconds per test (default)
- **Long Duration Tests**: None (all standard 60s)
- **Advanced Scripts**: None (all use basic tdklib)
- **Skip Status**: No tests are skipped by default
- **Release Version**: M128

---

## Summary Statistics

- **Total Test Files**: 34
- **Total Test Cases**: 34
- **Coverage APIs**: 21 unique APIs
- **Positive Tests**: 16
- **Negative Tests**: 12
- **Query/Property Tests**: 6
- **Activation Tests**: 1
- **Test Interface**: RdkService_Test

