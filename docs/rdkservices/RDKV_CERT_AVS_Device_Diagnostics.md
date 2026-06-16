## Table of Contents

1. [Objective](#objective)
2. [Pre-conditions](#pre-conditions)
3. [Test Cases](#test-cases)
   - [DeviceDiagnostics_Get_Configurations (DD_01)](#devicediagnostics_get_configurations-dd_01)
   - [DeviceDiagnostics_Deactivate_Activate_Stress (DD_02)](#devicediagnostics_deactivate_activate_stress-dd_02)
   - [DeviceDiagnostics_Check_AVDecoder_Idle_Active_State (DD_03)](#devicediagnostics_check_avdecoder_idle_active_state-dd_03)
   - [DeviceDiagnostics_Check_AVDecoder_StateChange_Event_Idle_Active (DD_04)](#devicediagnostics_check_avdecoder_statechange_event_idle_active-dd_04)
   - [DeviceDiagnostics_ActivateDeactivate_Event_Test (DD_05)](#devicediagnostics_activatedeactivate_event_test-dd_05)
   - [DeviceDiagnostics_ActivateDeactivate_All_Event_Test (DD_06)](#devicediagnostics_activatedeactivate_all_event_test-dd_06)
4. [Post-conditions](#post-conditions)
5. [Test Attributes](#test-attributes)

---

## Objective

The **DeviceDiagnostics** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.DeviceDiagnostics` (version 1)

**API Coverage:**

- **State / Query APIs**: `getAVDecoderStatus`, `getConfiguration`
- **Events**: `onAVDecoderStatusChanged`

### APIs Under Test

| API | Description |
|-----|-------------|
| `getAVDecoderStatus` | Gets the most active status of audio/video decoder/pipeline |
| `getConfiguration` | RDK API interface for the WebPA service |

### Events Under Test

| Event | Description |
|-------|-------------|
| `onAVDecoderStatusChanged` | Triggered when the most active status of audio/video decoder/pipeline changes |

---

## Pre-conditions

### Pre-condition 1: Activate_DeviceDiagnostics_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DeviceDiagnostics"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"org.rdk.DeviceDiagnostics"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DeviceDiagnostics"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DeviceDiagnostics"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Pre-condition 2: Register_And_Listen_Events

- Register and listen to event `Event_OnAVDecoder_Status_Changed` on `DeviceDiagnostics` plugin

- Register and listen to event `Event_Controller_State_Changed` on `Controller` plugin

- Register and listen to event `Event_Controller_All` on `Controller` plugin

---

## Test Cases

<a id="devicediagnostics_get_configurations-dd_01"></a>
### DeviceDiagnostics_Get_Configurations (DD_01)

**Objective:** Gets value of provided property names

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Configuration | Invoke `getConfiguration` on `org.rdk.DeviceDiagnostics` with `names`: `"<DEVICE_DIAGNOSTICS_RFC_PARAMS>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DeviceDiagnostics.1.getConfiguration", "params": {"names": "<DEVICE_DIAGNOSTICS_RFC_PARAMS>"}}' http://127.0.0.1:9998/jsonrpc` | Configuration values returned for requested property names |

---

<a id="devicediagnostics_deactivate_activate_stress-dd_02"></a>
### DeviceDiagnostics_Deactivate_Activate_Stress (DD_02)

**Objective:** Deactivate and activate the device diagnostics plugin in loop and checks the CPU load

**Test Steps:**

> **Stress Loop:** The step sequence below forms one iteration block. It is repeated **`<STRESS_TEST_REPEAT_COUNT>`** times as set in the device configuration file (key: `STRESS_TEST_REPEAT_COUNT`)

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate DeviceDiagnostics Plugin | Invoke `deactivate` on `Controller` with `callsign`: `"org.rdk.DeviceDiagnostics"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.DeviceDiagnostics"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 2 | Activate DeviceDiagnostics Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.DeviceDiagnostics"` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DeviceDiagnostics"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Get CPU Load | Invoke `systeminfo` on `DeviceInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.systeminfo"}' http://127.0.0.1:9998/jsonrpc` | CPU load is retrieved and validated successfully |

---

<a id="devicediagnostics_check_avdecoder_idle_active_state-dd_03"></a>
### DeviceDiagnostics_Check_AVDecoder_Idle_Active_State (DD_03)

**Objective:** Checks the AV decoder status in idle and active state on launching and terminating an app

**Pre-condition:**

#### Pre-condition 1: Activate_Dependent_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | *(Loop: iterates for each plugin listed in `<DEVICE_DIAGNOSTICS_PREREQ_PLUGINS>`)*<br>Invoke `status` on `Controller` with `plugin`: `"<DEVICE_DIAGNOSTICS_PREREQ_PLUGINS>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status", "params": {"plugin": "<DEVICE_DIAGNOSTICS_PREREQ_PLUGINS>"}}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin state requires action)*<br>Invoke `activate` on `Controller` with `callsign`: `"<value>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin state requires action)*<br>Invoke `status` on `Controller` with `plugin`: `"<value>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status", "params": {"plugin": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

#### Pre-condition 2: Check_Existing_Package_Before_Install

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Existing Package | Invoke `listPackages` on `org.rdk.PackageManagerRDKEMS`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Package list returned successfully |
| 2 | Uninstall Existing Package | *(Conditional: executed only if package/app is currently present)*<br>Invoke `uninstall` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"` (wait 10 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 3 | Download ValidParameters | Invoke `download` on `org.rdk.DownloadManager` with `url`: `"<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_HOSTEDURL>"` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Valid downloadId is returned successfully |
| 4 | Install | Invoke `install` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"`, `version`: `"<PACKAGEMANAGER_APPLICATION_VERSION>"`, `fileLocator`: `"<DOWNLOADED_FILE_LOCATOR_URL>"`, `name`: `"<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>"`, `value`: `"<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.install", "params": {"packageId": "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "fileLocator": "<DOWNLOADED_FILE_LOCATOR_URL>", "name": "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", "value": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 5 | Verify Installed Package | Invoke `listPackages` on `org.rdk.PackageManagerRDKEMS` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Installed package validation succeeds |

#### Pre-condition 3: PersistentStore_Set_and_Get_Value

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set Value | Invoke `setValue` on `org.rdk.PersistentStore` with `namespace`: `"MVS"`, `key`: `"lightningURL"`, `value`: `"<DEVICE_DIAGNOSTICS_PLAYBACK_URL>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setValue", "params": {"namespace": "MVS", "key": "lightningURL", "value": "<DEVICE_DIAGNOSTICS_PLAYBACK_URL>"}}' http://127.0.0.1:9998/jsonrpc` | Value set successfully |
| 2 | Get Value | Invoke `getValue` on `org.rdk.PersistentStore` with `namespace`: `"MVS"`, `key`: `"lightningURL"` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getValue", "params": {"namespace": "MVS", "key": "lightningURL"}}' http://127.0.0.1:9998/jsonrpc` | Expected: `<DEVICE_DIAGNOSTICS_PLAYBACK_URL>` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AVDecoder Status | Invoke `getAVDecoderStatus` on `org.rdk.DeviceDiagnostics`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DeviceDiagnostics.1.getAVDecoderStatus"}' http://127.0.0.1:9998/jsonrpc` | AV decoder status is `"idle"` |
| 2 | Launch App Valid Params | Invoke `launchApp` on `org.rdk.AppManager` with `appId`: `"<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 3 | Check App Launched | Invoke `getLoadedApps` on `org.rdk.AppManager` (wait 10 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Loaded apps information validated successfully |
| 4 | Get AVDecoder Status | Invoke `getAVDecoderStatus` on `org.rdk.DeviceDiagnostics` (wait 30 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DeviceDiagnostics.1.getAVDecoderStatus"}' http://127.0.0.1:9998/jsonrpc` | AV decoder status is `"active"` |
| 5 | Terminate App Valid Param | Invoke `terminateApp` on `org.rdk.AppManager` with `appId`: `"<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 6 | Get AVDecoder Status | Invoke `getAVDecoderStatus` on `org.rdk.DeviceDiagnostics` (wait 30 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DeviceDiagnostics.1.getAVDecoderStatus"}' http://127.0.0.1:9998/jsonrpc` | AV decoder status is `"idle"` |

**Post-condition:**

#### Post-condition 1: Terminate_Application

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Loaded apps information validated successfully |
| 2 | Terminate App Valid Param | *(Conditional: executed only if package/app is currently present)*<br>Invoke `terminateApp` on `org.rdk.AppManager` with `appId`: `"<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 3 | Check Package Info | Invoke `listPackages` on `org.rdk.PackageManagerRDKEMS`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Package list returned successfully |
| 4 | Uninstall Package | *(Conditional: executed only if package/app is currently present)*<br>Invoke `uninstall` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="devicediagnostics_check_avdecoder_statechange_event_idle_active-dd_04"></a>
### DeviceDiagnostics_Check_AVDecoder_StateChange_Event_Idle_Active (DD_04)

**Objective:** Checks the AV decoder status changed event in idle and active state

**Pre-condition:**

#### Pre-condition 1: Activate_Dependent_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | *(Loop: iterates for each plugin listed in `<DEVICE_DIAGNOSTICS_PREREQ_PLUGINS>`)*<br>Invoke `status` on `Controller` with `plugin`: `"<DEVICE_DIAGNOSTICS_PREREQ_PLUGINS>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status", "params": {"plugin": "<DEVICE_DIAGNOSTICS_PREREQ_PLUGINS>"}}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin state requires action)*<br>Invoke `activate` on `Controller` with `callsign`: `"<value>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin state requires action)*<br>Invoke `status` on `Controller` with `plugin`: `"<value>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status", "params": {"plugin": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

#### Pre-condition 2: Check_Existing_Package_Before_Install

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Existing Package | Invoke `listPackages` on `org.rdk.PackageManagerRDKEMS`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Package list returned successfully |
| 2 | Uninstall Existing Package | *(Conditional: executed only if package/app is currently present)*<br>Invoke `uninstall` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"` (wait 10 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 3 | Download ValidParameters | Invoke `download` on `org.rdk.DownloadManager` with `url`: `"<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_HOSTEDURL>"` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Valid downloadId is returned successfully |
| 4 | Install | Invoke `install` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"`, `version`: `"<PACKAGEMANAGER_APPLICATION_VERSION>"`, `fileLocator`: `"<DOWNLOADED_FILE_LOCATOR_URL>"`, `name`: `"<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>"`, `value`: `"<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.install", "params": {"packageId": "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "fileLocator": "<DOWNLOADED_FILE_LOCATOR_URL>", "name": "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", "value": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 5 | Verify Installed Package | Invoke `listPackages` on `org.rdk.PackageManagerRDKEMS` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Installed package validation succeeds |

#### Pre-condition 3: PersistentStore_Set_and_Get_Value

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set Value | Invoke `setValue` on `org.rdk.PersistentStore` with `namespace`: `"MVS"`, `key`: `"lightningURL"`, `value`: `"<DEVICE_DIAGNOSTICS_PLAYBACK_URL>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setValue", "params": {"namespace": "MVS", "key": "lightningURL", "value": "<DEVICE_DIAGNOSTICS_PLAYBACK_URL>"}}' http://127.0.0.1:9998/jsonrpc` | Value set successfully |
| 2 | Get Value | Invoke `getValue` on `org.rdk.PersistentStore` with `namespace`: `"MVS"`, `key`: `"lightningURL"` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getValue", "params": {"namespace": "MVS", "key": "lightningURL"}}' http://127.0.0.1:9998/jsonrpc` | Expected: `<DEVICE_DIAGNOSTICS_PLAYBACK_URL>` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AVDecoder Status | Invoke `getAVDecoderStatus` on `org.rdk.DeviceDiagnostics`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DeviceDiagnostics.1.getAVDecoderStatus"}' http://127.0.0.1:9998/jsonrpc` | AV decoder status is `"idle"` |
| 2 | Launch App Valid Params | Invoke `launchApp` on `org.rdk.AppManager` with `appId`: `"<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 3 | Check App Launched | Invoke `getLoadedApps` on `org.rdk.AppManager` (wait 10 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Loaded apps information validated successfully |
| 4 | Check OnAVDecoder Status Changed Event | Listen for `Event_OnAVDecoder_Status_Changed` event (timeout: 60s) | `onAVDecoderStatusChanged` event received; `AVDecoderStatus` = `"active"` |
| 5 | Terminate App Valid Param | Invoke `terminateApp` on `org.rdk.AppManager` with `appId`: `"<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 6 | Check OnAVDecoder Status Changed Event | Listen for `Event_OnAVDecoder_Status_Changed` event (timeout: 30s) | `onAVDecoderStatusChanged` event received; `AVDecoderStatus` = `"idle"` |

**Post-condition:**

#### Post-condition 1: Terminate_Application

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Loaded apps information validated successfully |
| 2 | Terminate App Valid Param | *(Conditional: executed only if package/app is currently present)*<br>Invoke `terminateApp` on `org.rdk.AppManager` with `appId`: `"<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 3 | Check Package Info | Invoke `listPackages` on `org.rdk.PackageManagerRDKEMS`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Package list returned successfully |
| 4 | Uninstall Package | *(Conditional: executed only if package/app is currently present)*<br>Invoke `uninstall` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="devicediagnostics_activatedeactivate_event_test-dd_05"></a>
### DeviceDiagnostics_ActivateDeactivate_Event_Test (DD_05)

**Objective:** Validates statechange event on Activating/deactivating the plugin

**Pre-condition:**

#### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DeviceDiagnostics"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"org.rdk.DeviceDiagnostics"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DeviceDiagnostics"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DeviceDiagnostics"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate DeviceDiagnostics Plugin | Invoke `deactivate` on `Controller` with `callsign`: `"org.rdk.DeviceDiagnostics"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.DeviceDiagnostics"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 2 | Check State Change Event | Listen for `Event_Controller_State_Changed` event (timeout: 2s) | `statechange` event received; callsign = `org.rdk.devicediagnostics`, state = `"deactivated"` |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DeviceDiagnostics"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 4 | Activate DeviceDiagnostics Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.DeviceDiagnostics"` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DeviceDiagnostics"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 5 | Check State Change Event | Listen for `Event_Controller_State_Changed` event (timeout: 2s) | `statechange` event received; callsign = `org.rdk.devicediagnostics`, state = `"activated"` |
| 6 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DeviceDiagnostics"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

<a id="devicediagnostics_activatedeactivate_all_event_test-dd_06"></a>
### DeviceDiagnostics_ActivateDeactivate_All_Event_Test (DD_06)

**Objective:** Validates all event on Activating/deactivating the plugin

**Pre-condition:**

#### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DeviceDiagnostics"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"org.rdk.DeviceDiagnostics"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DeviceDiagnostics"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DeviceDiagnostics"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate DeviceDiagnostics Plugin | Invoke `deactivate` on `Controller` with `callsign`: `"org.rdk.DeviceDiagnostics"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.DeviceDiagnostics"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 2 | Check All Event | Listen for `Event_Controller_All` event (timeout: 2s) | Controller `all` event received; callsign = `org.rdk.devicediagnostics`, state = `"deactivated"` |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DeviceDiagnostics"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 4 | Activate DeviceDiagnostics Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.DeviceDiagnostics"` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DeviceDiagnostics"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 5 | Check All Event | Listen for `Event_Controller_All` event (timeout: 2s) | Controller `all` event received; callsign = `org.rdk.devicediagnostics`, state = `"activated"` |
| 6 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DeviceDiagnostics"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

---

## Post-conditions

_No plugin-level post-conditions defined_

---

## Test Attributes

| Attribute | Value |
|-----------|-------|
| Supported Models | Video Accelerator, RPI Client |
| Estimated Duration | 20 minutes |
| Priority | Medium |
| TDK Release Version | M81 |