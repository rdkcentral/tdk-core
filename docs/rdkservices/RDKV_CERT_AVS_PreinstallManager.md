## TestScript Name
RDKV_CERT_AVS_PreinstallManager

## Table of Contents

1. [Objective](#objective)
2. [Plugin Pre-conditions](#plugin-pre-conditions)
3. [Test Cases](#test-cases)
   - [PreinstallManager_StartPreInstall_ForceInstall_True](#preinstallmanager_startpreinstall_forceinstall_true)
   - [PreinstallManager_StartPreInstall_ForceInstall_False](#preinstallmanager_startpreinstall_forceinstall_false)
   - [PreinstallManager_StartPreInstall_Empty](#preinstallmanager_startpreinstall_empty)
   - [PreinstallManager_StartPreInstall_Invalid_String](#preinstallmanager_startpreinstall_invalid_string)
   - [PreinstallManager_StartPreInstall_Number](#preinstallmanager_startpreinstall_number)
   - [PreinstallManager_StartPreInstall_Without_Parameter](#preinstallmanager_startpreinstall_without_parameter)
   - [PreinstallManager_StartPreInstall_Special_Characters](#preinstallmanager_startpreinstall_special_characters)
   - [PreinstallManager_StartPreInstall_Very_Long_String](#preinstallmanager_startpreinstall_very_long_string)
   - [PreinstallManager_StartPreInstall_Null_Parameter](#preinstallmanager_startpreinstall_null_parameter)
   - [PreinstallManager_StartPreInstall_CaseSensitive](#preinstallmanager_startpreinstall_casesensitive)
   - [PreinstallManager_GetPreInstallState](#preinstallmanager_getpreinstallstate)
   - [Preinstall_Check_On_AppInstallationStatus_Event_StartPreInstall_True](#preinstall_check_on_appinstallationstatus_event_startpreinstall_true)
   - [Preinstall_Check_On_AppInstallationStatus_Event_StartPreInstall_False](#preinstall_check_on_appinstallationstatus_event_startpreinstall_false)
4. [Plugin Post-conditions](#plugin-post-conditions)
5. [Test Attributes](#test-attributes)

---

## Objective

The **PreinstallManager** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.PreinstallManager` (version 1)

**API Coverage**

- **Lifecycle / Control APIs**: `startPreinstall`

## APIs Under Test

| API | Description |
|-----|-------------|
| `startPreinstall` | Checks the preinstall directory for packages to be preinstalled and installs them as needed |

---

## Plugin Pre-conditions

### Plugin Pre-condition 1: Activate_AppStorageManager_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Check Active Status of AppStorageManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.AppStorageManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate AppStorageManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.AppStorageManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is currently deactivated)*<br>Check Active Status of AppStorageManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.AppStorageManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Plugin Pre-condition 2: Activate_DownloadManager_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Check Active Status of DownloadManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DownloadManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate DownloadManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DownloadManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is currently deactivated)*<br>Check Active Status of DownloadManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DownloadManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Plugin Pre-condition 3: Activate_PackageManagerRDKEMS_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Check Active Status of PackageManagerRDKEMS Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate PackageManagerRDKEMS Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.PackageManagerRDKEMS"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is currently deactivated)*<br>Check Active Status of PackageManagerRDKEMS Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Plugin Pre-condition 4: Activate_AppManager_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Check Active Status of AppManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.AppManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate AppManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.AppManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is currently deactivated)*<br>Check Active Status of AppManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.AppManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Plugin Pre-condition 5: Activate_PreinstallManager_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Check Active Status of PreinstallManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PreinstallManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate PreinstallManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.PreinstallManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is currently deactivated)*<br>Check Active Status of PreinstallManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PreinstallManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

## Test Cases

<a id="preinstallmanager_startpreinstall_forceinstall_true"></a>
### TestCase Name
PreinstallManager_StartPreInstall_ForceInstall_True

### TestCase ID
PIM_01

### TestCase Objective
Check StartPreInstall method behavior when forceInstall is true

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | StartPreInstall ForceInstall True | Invoke startPreinstall on org.rdk.PreinstallManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PreinstallManager.1.startPreinstall", "params": {"forceInstall": true}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="preinstallmanager_startpreinstall_forceinstall_false"></a>
### TestCase Name
PreinstallManager_StartPreInstall_ForceInstall_False

### TestCase ID
PIM_02

### TestCase Objective
Check StartPreInstall method behavior when forceInstall is false

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | StartPreInstall ForceInstall False | Invoke startPreinstall on org.rdk.PreinstallManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PreinstallManager.1.startPreinstall", "params": {"forceInstall": false}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="preinstallmanager_startpreinstall_empty"></a>
### TestCase Name
PreinstallManager_StartPreInstall_Empty

### TestCase ID
PIM_03

### TestCase Objective
Check StartPreInstall method behavior when forceInstall is empty

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | StartPreInstall Empty | Invoke startPreinstall on org.rdk.PreinstallManager with forceInstall: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PreinstallManager.1.startPreinstall", "params": {"forceInstall": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="preinstallmanager_startpreinstall_invalid_string"></a>
### TestCase Name
PreinstallManager_StartPreInstall_Invalid_String

### TestCase ID
PIM_04

### TestCase Objective
Check StartPreInstall method behavior when forceInstall is an invalid string

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | StartPreInstall Invalid String | Invoke startPreinstall on org.rdk.PreinstallManager with forceInstall: "invalid_string"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PreinstallManager.1.startPreinstall", "params": {"forceInstall": "invalid_string"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="preinstallmanager_startpreinstall_number"></a>
### TestCase Name
PreinstallManager_StartPreInstall_Number

### TestCase ID
PIM_05

### TestCase Objective
Check StartPreInstall method behavior when forceInstall is a number

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | StartPreInstall Number | Invoke startPreinstall on org.rdk.PreinstallManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PreinstallManager.1.startPreinstall", "params": {"forceInstall": 123}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="preinstallmanager_startpreinstall_without_parameter"></a>
### TestCase Name
PreinstallManager_StartPreInstall_Without_Parameter

### TestCase ID
PIM_06

### TestCase Objective
Check StartPreInstall method behavior when called without parameter

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | StartPreInstall Without Parameter | Invoke startPreinstall on org.rdk.PreinstallManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PreinstallManager.1.startPreinstall"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="preinstallmanager_startpreinstall_special_characters"></a>
### TestCase Name
PreinstallManager_StartPreInstall_Special_Characters

### TestCase ID
PIM_07

### TestCase Objective
Check StartPreInstall method behavior with special characters

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | StartPreInstall Special Characters | Invoke startPreinstall on org.rdk.PreinstallManager with forceInstall: "()^*!"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PreinstallManager.1.startPreinstall", "params": {"forceInstall": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="preinstallmanager_startpreinstall_very_long_string"></a>
### TestCase Name
PreinstallManager_StartPreInstall_Very_Long_String

### TestCase ID
PIM_08

### TestCase Objective
Check StartPreInstall method behavior with very long string parameter

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | StartPreInstall Very Long String | Invoke startPreinstall on org.rdk.PreinstallManager with forceInstall: "this_is_a_very_long_string_that_exceeds_normal_parameter_length_to_test_buffer_overflow_or_length_validation_mechanisms"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PreinstallManager.1.startPreinstall", "params": {"forceInstall": "this_is_a_very_long_string_that_exceeds_normal_parameter_length_to_test_buffer_overflow_or_length_validation_mechanisms"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="preinstallmanager_startpreinstall_null_parameter"></a>
### TestCase Name
PreinstallManager_StartPreInstall_Null_Parameter

### TestCase ID
PIM_09

### TestCase Objective
Check StartPreInstall method behavior when forceInstall parameter is null

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | StartPreInstall Null Parameter | Invoke startPreinstall on org.rdk.PreinstallManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PreinstallManager.1.startPreinstall", "params": {"forceInstall": null}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="preinstallmanager_startpreinstall_casesensitive"></a>
### TestCase Name
PreinstallManager_StartPreInstall_CaseSensitive

### TestCase ID
PIM_10

### TestCase Objective
Check StartPreInstall method behavior with case variations of boolean

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | StartPreInstall CaseSensitive TRUE | Invoke startPreinstall on org.rdk.PreinstallManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PreinstallManager.1.startPreinstall", "params": {"forceInstall": true}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="preinstallmanager_getpreinstallstate"></a>
### TestCase Name
PreinstallManager_GetPreInstallState

### TestCase ID
PIM_11

### TestCase Objective
Check getPreinstallState method behavior

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PreInstallState | Invoke getPreinstallState on org.rdk.PreinstallManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PreinstallManager.1.getPreinstallState"}' http://127.0.0.1:9998/jsonrpc` | Expected: `NOT_STARTED,IN_PROGRESS,COMPLETED` |

---

<a id="preinstall_check_on_appinstallationstatus_event_startpreinstall_true"></a>
### TestCase Name
Preinstall_Check_On_AppInstallationStatus_Event_StartPreInstall_True

### TestCase ID
PIM_12

### TestCase Objective
Check onAppInstallationStatus event behavior when startPreinstall is called with true

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | StartPreInstall ForceInstall True | Invoke startPreinstall on org.rdk.PreinstallManager with forceInstall: "true"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PreinstallManager.1.startPreinstall", "params": {"forceInstall": true}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Check On AppInstallationStatus Event | Listen for `Event_On_AppInstallationStatus` event (timeout: 60s) | Verify that the event is received and validated successfully |

---

<a id="preinstall_check_on_appinstallationstatus_event_startpreinstall_false"></a>
### TestCase Name
Preinstall_Check_On_AppInstallationStatus_Event_StartPreInstall_False

### TestCase ID
PIM_13

### TestCase Objective
Check onAppInstallationStatus event behavior when startPreinstall is called with false

### TestCase Pre-condition

#### TestCase Pre-condition 1: Preinstall_Apps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | StartPreInstall ForceInstall True | Start Preinstall on PreinstallManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PreinstallManager.1.startPreinstall", "params": {"forceInstall": true}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Check On AppInstallationStatus Event | Check On AppInstallationStatus Event | Verify that the event is received and validated successfully |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | StartPreInstall ForceInstall False | Invoke startPreinstall on org.rdk.PreinstallManager with forceInstall: "false"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PreinstallManager.1.startPreinstall", "params": {"forceInstall": false}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Check On AppInstallationStatus Event | Listen for `Event_On_AppInstallationStatus` event (timeout: 60s) | Verify that the event is received and validated successfully |

---

---

## Plugin Post-conditions

_No plugin-level post-conditions defined_

---

## Test Attributes

| Attribute | Value |
|-----------|-------|
| Supported Models | Video Accelerator, RPI Client |
| Estimated Duration | 20 minutes |
| Priority | Medium |
| TDK Release Version | M147 |
