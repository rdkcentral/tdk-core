## Table of Contents

1. [Objective](#objective)
2. [Pre-conditions](#pre-conditions)
3. [Test Cases](#test-cases)
   - [PreinstallManager_StartPreInstall_ForceInstall_True (PIM_01)](#preinstallmanager_startpreinstall_forceinstall_true-pim_01)
   - [PreinstallManager_StartPreInstall_ForceInstall_False (PIM_02)](#preinstallmanager_startpreinstall_forceinstall_false-pim_02)
   - [PreinstallManager_StartPreInstall_Empty (PIM_03)](#preinstallmanager_startpreinstall_empty-pim_03)
   - [PreinstallManager_StartPreInstall_Invalid_String (PIM_04)](#preinstallmanager_startpreinstall_invalid_string-pim_04)
   - [PreinstallManager_StartPreInstall_Number (PIM_05)](#preinstallmanager_startpreinstall_number-pim_05)
   - [PreinstallManager_StartPreInstall_Without_Parameter (PIM_06)](#preinstallmanager_startpreinstall_without_parameter-pim_06)
   - [PreinstallManager_StartPreInstall_Special_Characters (PIM_07)](#preinstallmanager_startpreinstall_special_characters-pim_07)
   - [PreinstallManager_StartPreInstall_Very_Long_String (PIM_08)](#preinstallmanager_startpreinstall_very_long_string-pim_08)
   - [PreinstallManager_StartPreInstall_Null_Parameter (PIM_09)](#preinstallmanager_startpreinstall_null_parameter-pim_09)
   - [PreinstallManager_StartPreInstall_CaseSensitive (PIM_10)](#preinstallmanager_startpreinstall_casesensitive-pim_10)
4. [Post-conditions](#post-conditions)
5. [Test Attributes](#test-attributes)

---

## Objective

The **PreinstallManager** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.PreinstallManager` (version 1)

**API Coverage**

- **Lifecycle / Control APIs**: `startPreinstall`

### APIs Under Test

| API | Description |
|-----|-------------|
| `startPreinstall` | Checks the preinstall directory for packages to be preinstalled and installs them as needed |

---

## Pre-conditions

### Pre-condition 1: Activate_AppStorageManager_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.AppStorageManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.AppStorageManager"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.AppStorageManager"}}' http://127.0.0.1:9998/jsonrpc` | N/A |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.AppStorageManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Pre-condition 2: Activate_DownloadManager_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DownloadManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.DownloadManager"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DownloadManager"}}' http://127.0.0.1:9998/jsonrpc` | N/A |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DownloadManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Pre-condition 3: Activate_PackageManagerRDKEMS_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.PackageManagerRDKEMS"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.PackageManagerRDKEMS"}}' http://127.0.0.1:9998/jsonrpc` | N/A |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Pre-condition 4: Activate_AppManager_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.AppManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.AppManager"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.AppManager"}}' http://127.0.0.1:9998/jsonrpc` | N/A |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.AppManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Pre-condition 5: Activate_PreinstallManager_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PreinstallManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.PreinstallManager"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.PreinstallManager"}}' http://127.0.0.1:9998/jsonrpc` | N/A |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PreinstallManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

## Test Cases

<a id="preinstallmanager_startpreinstall_forceinstall_true-pim_01"></a>
### PreinstallManager_StartPreInstall_ForceInstall_True (PIM_01)

**Objective:** Check StartPreInstall method behavior when forceInstall is true

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | StartPreInstall ForceInstall True | Invoke `startPreinstall` on `org.rdk.PreinstallManager` with `forceInstall`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PreinstallManager.1.startPreinstall", "params": {"forceInstall": true}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="preinstallmanager_startpreinstall_forceinstall_false-pim_02"></a>
### PreinstallManager_StartPreInstall_ForceInstall_False (PIM_02)

**Objective:** Check StartPreInstall method behavior when forceInstall is false

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | StartPreInstall ForceInstall False | Invoke `startPreinstall` on `org.rdk.PreinstallManager` with `forceInstall`: `false`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PreinstallManager.1.startPreinstall", "params": {"forceInstall": false}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="preinstallmanager_startpreinstall_empty-pim_03"></a>
### PreinstallManager_StartPreInstall_Empty (PIM_03)

**Objective:** Check StartPreInstall method behavior when forceInstall is empty

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | StartPreInstall Empty | Invoke `startPreinstall` on `org.rdk.PreinstallManager` with `forceInstall`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PreinstallManager.1.startPreinstall", "params": {"forceInstall": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="preinstallmanager_startpreinstall_invalid_string-pim_04"></a>
### PreinstallManager_StartPreInstall_Invalid_String (PIM_04)

**Objective:** Check StartPreInstall method behavior when forceInstall is an invalid string

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | StartPreInstall Invalid String | Invoke `startPreinstall` on `org.rdk.PreinstallManager` with `forceInstall`: `"invalid_string"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PreinstallManager.1.startPreinstall", "params": {"forceInstall": "invalid_string"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="preinstallmanager_startpreinstall_number-pim_05"></a>
### PreinstallManager_StartPreInstall_Number (PIM_05)

**Objective:** Check StartPreInstall method behavior when forceInstall is a number

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | StartPreInstall Number | Invoke `startPreinstall` on `org.rdk.PreinstallManager` with `forceInstall`: `123`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PreinstallManager.1.startPreinstall", "params": {"forceInstall": 123}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="preinstallmanager_startpreinstall_without_parameter-pim_06"></a>
### PreinstallManager_StartPreInstall_Without_Parameter (PIM_06)

**Objective:** Check StartPreInstall method behavior when called without parameter

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | StartPreInstall Without Parameter | Invoke `startPreinstall` on `org.rdk.PreinstallManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PreinstallManager.1.startPreinstall"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="preinstallmanager_startpreinstall_special_characters-pim_07"></a>
### PreinstallManager_StartPreInstall_Special_Characters (PIM_07)

**Objective:** Check StartPreInstall method behavior with special characters

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | StartPreInstall Special Characters | Invoke `startPreinstall` on `org.rdk.PreinstallManager` with `forceInstall`: `"()^*!"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PreinstallManager.1.startPreinstall", "params": {"forceInstall": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="preinstallmanager_startpreinstall_very_long_string-pim_08"></a>
### PreinstallManager_StartPreInstall_Very_Long_String (PIM_08)

**Objective:** Check StartPreInstall method behavior with very long string parameter

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | StartPreInstall Very Long String | Invoke `startPreinstall` on `org.rdk.PreinstallManager` with `forceInstall`: `"this_is_a_very_long_string_that_exceeds_normal_parameter_length_to_test_buffer_overflow_or_length_validation_mechanisms"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PreinstallManager.1.startPreinstall", "params": {"forceInstall": "this_is_a_very_long_string_that_exceeds_normal_parameter_length_to_test_buffer_overflow_or_length_validation_mechanisms"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="preinstallmanager_startpreinstall_null_parameter-pim_09"></a>
### PreinstallManager_StartPreInstall_Null_Parameter (PIM_09)

**Objective:** Check StartPreInstall method behavior when forceInstall parameter is null

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | StartPreInstall Null Parameter | Invoke `startPreinstall` on `org.rdk.PreinstallManager` with `forceInstall`: `null`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PreinstallManager.1.startPreinstall", "params": {"forceInstall": null}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="preinstallmanager_startpreinstall_casesensitive-pim_10"></a>
### PreinstallManager_StartPreInstall_CaseSensitive (PIM_10)

**Objective:** Check StartPreInstall method behavior with case variations of boolean

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | StartPreInstall CaseSensitive TRUE | Invoke `startPreinstall` on `org.rdk.PreinstallManager` with `forceInstall`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PreinstallManager.1.startPreinstall", "params": {"forceInstall": true}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

---

## Post-conditions

_No plugin-level post-conditions defined._

---

## Test Attributes

| Attribute | Value |
|-----------|-------|
| Supported Models | Video Accelerator, RPI Client |
| Estimated Duration | 20 minutes |
| Priority | High |
| TDK Release Version | M147 |