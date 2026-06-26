## TestScript Name
RDKV_CERT_AVS_Device_Diagnostics

## Table of Contents

1. [Objective](#objective)
2. [Plugin Pre-conditions](#plugin-pre-conditions)
3. [Test Cases](#test-cases)
   - [DeviceDiagnostics_Get_Configurations](#devicediagnostics_get_configurations)
   - [DeviceDiagnostics_Deactivate_Activate_Stress](#devicediagnostics_deactivate_activate_stress)
   - [DeviceDiagnostics_Check_AVDecoder_Idle_Active_State](#devicediagnostics_check_avdecoder_idle_active_state)
   - [DeviceDiagnostics_Check_AVDecoder_StateChange_Event_Idle_Active](#devicediagnostics_check_avdecoder_statechange_event_idle_active)
   - [DeviceDiagnostics_ActivateDeactivate_Event_Test](#devicediagnostics_activatedeactivate_event_test)
   - [DeviceDiagnostics_ActivateDeactivate_All_Event_Test](#devicediagnostics_activatedeactivate_all_event_test)
4. [Plugin Post-conditions](#plugin-post-conditions)
5. [Test Attributes](#test-attributes)

---

## Objective

The **DeviceDiagnostics** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.DeviceDiagnostics` (version 1)

**API Coverage:**

- **State / Query APIs**: `getAVDecoderStatus`, `getConfiguration`
- **Events**: `onAVDecoderStatusChanged`

## APIs Under Test

| API | Description |
|-----|-------------|
| `getAVDecoderStatus` | Gets the most active status of audio/video decoder/pipeline |
| `getConfiguration` | RDK API interface for the WebPA service |

## Events Under Test

| Event | Description |
|-------|-------------|
| `onAVDecoderStatusChanged` | Triggered when the most active status of audio/video decoder/pipeline changes |

---

## Plugin Pre-conditions

### Plugin Pre-condition 1: Activate_DeviceDiagnostics_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Check Active Status of DeviceDiagnostics Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DeviceDiagnostics"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate DeviceDiagnostics Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DeviceDiagnostics"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is currently deactivated)*<br>Check Active Status of DeviceDiagnostics Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DeviceDiagnostics"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Plugin Pre-condition 2: Register_And_Listen_Events

- Register and listen to event `Event_OnAVDecoder_Status_Changed` on `DeviceDiagnostics` plugin

- Register and listen to event `Event_Controller_State_Changed` on `Controller` plugin

- Register and listen to event `Event_Controller_All` on `Controller` plugin

---

## Test Cases

<a id="devicediagnostics_get_configurations"></a>
### TestCase Name
DeviceDiagnostics_Get_Configurations

### TestCase ID
DD_01

### TestCase Objective
Gets value of provided property names

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Configuration | Invoke getConfiguration on org.rdk.DeviceDiagnostics with names: "<DEVICE_DIAGNOSTICS_RFC_PARAMS>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DeviceDiagnostics.1.getConfiguration", "params": {"names": "<DEVICE_DIAGNOSTICS_RFC_PARAMS>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that configuration values are returned for the requested property names |

---

<a id="devicediagnostics_deactivate_activate_stress"></a>
### TestCase Name
DeviceDiagnostics_Deactivate_Activate_Stress

### TestCase ID
DD_02

### TestCase Objective
Deactivate and activate the device diagnostics plugin in loop and checks the CPU load

### Test Steps

> **Stress Loop:** The step sequence below forms one iteration block. It is repeated **`<STRESS_TEST_REPEAT_COUNT>`** times as set in the device configuration file (key: `STRESS_TEST_REPEAT_COUNT`)

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate DeviceDiagnostics Plugin | Invoke deactivate on Controller with callsign: "org.rdk.DeviceDiagnostics"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.DeviceDiagnostics"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 2 | Activate DeviceDiagnostics Plugin | Invoke activate on Controller with callsign: "org.rdk.DeviceDiagnostics"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DeviceDiagnostics"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 3 | Get CPU Load | Invoke systeminfo on DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.systeminfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that the CPU load is retrieved and validated successfully |

---

<a id="devicediagnostics_check_avdecoder_idle_active_state"></a>
### TestCase Name
DeviceDiagnostics_Check_AVDecoder_Idle_Active_State

### TestCase ID
DD_03

### TestCase Objective
Checks the AV decoder status in idle and active state on launching and terminating an app

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Dependent_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | *(Loop: iterates for each plugin listed in <DEVICE_DIAGNOSTICS_PREREQ_PLUGINS>)*<br>Check Plugin Active Status<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status", "params": {"plugin": "<DEVICE_DIAGNOSTICS_PREREQ_PLUGINS>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin state requires action)*<br>Activate <value> Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin state requires action)*<br>Check Plugin Active Status<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status", "params": {"plugin": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

#### TestCase Pre-condition 2: Check_Existing_Package_Before_Install

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Existing Package | Get Packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Verify that the package list is returned successfully |
| 2 | Uninstall Existing Package | *(Conditional statement executed only if package/app is currently present)*<br>Uninstall on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Download ValidParameters | Download on DownloadManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that a valid downloadId is returned |
| 4 | Install | Install on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.install", "params": {"packageId": "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "fileLocator": "<DOWNLOADED_FILE_LOCATOR_URL>", "name": "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", "value": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 5 | Verify Installed Package | Get Packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Confirm that the installed package is present in the package list |

#### TestCase Pre-condition 3: PersistentStore_Set_and_Get_Value

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set Value | Set Value on PersistentStore<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setValue", "params": {"namespace": "MVS", "key": "lightningURL", "value": "<DEVICE_DIAGNOSTICS_PLAYBACK_URL>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the value is set successfully |
| 2 | Get Value | Get Value from PersistentStore<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getValue", "params": {"namespace": "MVS", "key": "lightningURL"}}' http://127.0.0.1:9998/jsonrpc` | Expected `<DEVICE_DIAGNOSTICS_PLAYBACK_URL>` |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AVDecoder Status | Invoke getAVDecoderStatus on org.rdk.DeviceDiagnostics<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DeviceDiagnostics.1.getAVDecoderStatus"}' http://127.0.0.1:9998/jsonrpc` | AV decoder status is `"idle"` |
| 2 | Launch App Valid Params | Invoke launchApp on org.rdk.AppManager with appId: "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Check App Launched | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |
| 4 | Get AVDecoder Status | Invoke getAVDecoderStatus on org.rdk.DeviceDiagnostics<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DeviceDiagnostics.1.getAVDecoderStatus"}' http://127.0.0.1:9998/jsonrpc` | AV decoder status is `"active"` |
| 5 | Terminate App Valid Param | Invoke terminateApp on org.rdk.AppManager with appId: "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 6 | Get AVDecoder Status | Invoke getAVDecoderStatus on org.rdk.DeviceDiagnostics<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DeviceDiagnostics.1.getAVDecoderStatus"}' http://127.0.0.1:9998/jsonrpc` | AV decoder status is `"idle"` |

### TestCase Post-condition

#### TestCase Post-condition 1: Terminate_Application

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Get Loaded Apps from AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |
| 2 | Terminate App Valid Param | *(Conditional statement executed only if package/app is currently present)*<br>Terminate App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Check Package Info | Get Packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Verify that the package list is returned successfully |
| 4 | Uninstall Package | *(Conditional statement executed only if package/app is currently present)*<br>Uninstall on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="devicediagnostics_check_avdecoder_statechange_event_idle_active"></a>
### TestCase Name
DeviceDiagnostics_Check_AVDecoder_StateChange_Event_Idle_Active

### TestCase ID
DD_04

### TestCase Objective
Checks the AV decoder status changed event in idle and active state

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Dependent_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | *(Loop: iterates for each plugin listed in <DEVICE_DIAGNOSTICS_PREREQ_PLUGINS>)*<br>Check Plugin Active Status<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status", "params": {"plugin": "<DEVICE_DIAGNOSTICS_PREREQ_PLUGINS>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin state requires action)*<br>Activate <value> Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin state requires action)*<br>Check Plugin Active Status<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status", "params": {"plugin": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

#### TestCase Pre-condition 2: Check_Existing_Package_Before_Install

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Existing Package | Get Packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Verify that the package list is returned successfully |
| 2 | Uninstall Existing Package | *(Conditional statement executed only if package/app is currently present)*<br>Uninstall on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Download ValidParameters | Download on DownloadManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that a valid downloadId is returned |
| 4 | Install | Install on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.install", "params": {"packageId": "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "fileLocator": "<DOWNLOADED_FILE_LOCATOR_URL>", "name": "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", "value": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 5 | Verify Installed Package | Get Packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Confirm that the installed package is present in the package list |

#### TestCase Pre-condition 3: PersistentStore_Set_and_Get_Value

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set Value | Set Value on PersistentStore<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setValue", "params": {"namespace": "MVS", "key": "lightningURL", "value": "<DEVICE_DIAGNOSTICS_PLAYBACK_URL>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the value is set successfully |
| 2 | Get Value | Get Value from PersistentStore<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getValue", "params": {"namespace": "MVS", "key": "lightningURL"}}' http://127.0.0.1:9998/jsonrpc` | Expected `<DEVICE_DIAGNOSTICS_PLAYBACK_URL>` |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AVDecoder Status | Invoke getAVDecoderStatus on org.rdk.DeviceDiagnostics<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DeviceDiagnostics.1.getAVDecoderStatus"}' http://127.0.0.1:9998/jsonrpc` | AV decoder status is `"idle"` |
| 2 | Launch App Valid Params | Invoke launchApp on org.rdk.AppManager with appId: "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Check App Launched | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |
| 4 | Check OnAVDecoder Status Changed Event | Listen for Event_OnAVDecoder_Status_Changed event (timeout: 60s) | `onAVDecoderStatusChanged` event received; `AVDecoderStatus` = `"active"` |
| 5 | Terminate App Valid Param | Invoke terminateApp on org.rdk.AppManager with appId: "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 6 | Check OnAVDecoder Status Changed Event | Listen for Event_OnAVDecoder_Status_Changed event (timeout: 30s) | `onAVDecoderStatusChanged` event received; `AVDecoderStatus` = `"idle"` |

### TestCase Post-condition

#### TestCase Post-condition 1: Terminate_Application

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Get Loaded Apps from AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |
| 2 | Terminate App Valid Param | *(Conditional statement executed only if package/app is currently present)*<br>Terminate App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Check Package Info | Get Packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Verify that the package list is returned successfully |
| 4 | Uninstall Package | *(Conditional statement executed only if package/app is currently present)*<br>Uninstall on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="devicediagnostics_activatedeactivate_event_test"></a>
### TestCase Name
DeviceDiagnostics_ActivateDeactivate_Event_Test

### TestCase ID
DD_05

### TestCase Objective
Validates statechange event on Activating/deactivating the plugin

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Check Active Status of DeviceDiagnostics Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DeviceDiagnostics"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate DeviceDiagnostics Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DeviceDiagnostics"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is currently deactivated)*<br>Check Active Status of DeviceDiagnostics Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DeviceDiagnostics"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate DeviceDiagnostics Plugin | Invoke deactivate on Controller with callsign: "org.rdk.DeviceDiagnostics"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.DeviceDiagnostics"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 2 | Check State Change Event | Listen for Event_Controller_State_Changed event (timeout: 2s) | `statechange` event received; callsign = `org.rdk.devicediagnostics`, state = `"deactivated"` |
| 3 | Check PluginActive Status | Invoke status on Controller for org.rdk.DeviceDiagnostics<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DeviceDiagnostics"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 4 | Activate DeviceDiagnostics Plugin | Invoke activate on Controller with callsign: "org.rdk.DeviceDiagnostics"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DeviceDiagnostics"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 5 | Check State Change Event | Listen for Event_Controller_State_Changed event (timeout: 2s) | `statechange` event received; callsign = `org.rdk.devicediagnostics`, state = `"activated"` |
| 6 | Check PluginActive Status | Invoke status on Controller for org.rdk.DeviceDiagnostics<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DeviceDiagnostics"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

<a id="devicediagnostics_activatedeactivate_all_event_test"></a>
### TestCase Name
DeviceDiagnostics_ActivateDeactivate_All_Event_Test

### TestCase ID
DD_06

### TestCase Objective
Validates all event on Activating/deactivating the plugin

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Check Active Status of DeviceDiagnostics Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DeviceDiagnostics"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate DeviceDiagnostics Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DeviceDiagnostics"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is currently deactivated)*<br>Check Active Status of DeviceDiagnostics Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DeviceDiagnostics"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate DeviceDiagnostics Plugin | Invoke deactivate on Controller with callsign: "org.rdk.DeviceDiagnostics"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.DeviceDiagnostics"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 2 | Check All Event | Listen for Event_Controller_All event (timeout: 2s) | Controller `all` event received; callsign = `org.rdk.devicediagnostics`, state = `"deactivated"` |
| 3 | Check PluginActive Status | Invoke status on Controller for org.rdk.DeviceDiagnostics<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DeviceDiagnostics"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 4 | Activate DeviceDiagnostics Plugin | Invoke activate on Controller with callsign: "org.rdk.DeviceDiagnostics"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DeviceDiagnostics"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 5 | Check All Event | Listen for Event_Controller_All event (timeout: 2s) | Controller `all` event received; callsign = `org.rdk.devicediagnostics`, state = `"activated"` |
| 6 | Check PluginActive Status | Invoke status on Controller for org.rdk.DeviceDiagnostics<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DeviceDiagnostics"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

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
| TDK Release Version | M81 |