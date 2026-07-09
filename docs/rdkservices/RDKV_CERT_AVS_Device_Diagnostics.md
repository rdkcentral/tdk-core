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

## Objective

The **DeviceDiagnostics** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.DeviceDiagnostics` (version 1)

## Plugin Pre-conditions

### Plugin Pre-condition 1: Activate_DeviceDiagnostics_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of DeviceDiagnostics plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DeviceDiagnostics"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate DeviceDiagnostics plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DeviceDiagnostics"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of DeviceDiagnostics plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DeviceDiagnostics"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 2: Register_And_Listen_Events

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Subscribe to the onAVDecoderStatusChanged event | Register a WebSocket event listener for `onAVDecoderStatusChanged` to capture AV decoder status change notifications.<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DeviceDiagnostics.1.register", "params": {"event": "onAVDecoderStatusChanged", "id": "client.events.1"}}` | Event subscription should be established successfully and the event listener should be active |
| 2 | Subscribe to the statechange event | Register a WebSocket event listener for `statechange` to capture plugin state change notifications.<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.register", "params": {"event": "statechange", "id": "client.events.1"}}` | Event subscription should be established successfully and the event listener should be active |
| 3 | Subscribe to the all event | Register a WebSocket event listener for `all` to capture all system event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.register", "params": {"event": "all", "id": "client.events.1"}}` | Event subscription should be established successfully and the event listener should be active |

### Plugin Pre-condition 3: Configure_Device_Parameter

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Configure RFC params | `DEVICE_DIAGNOSTICS_RFC_PARAMS` must be set to the RFC parameter names to query | The `DEVICE_DIAGNOSTICS_RFC_PARAMS` value should be correctly configured in the device-specific config file |
| 2 | Configure prerequisite plugins | `DEVICE_DIAGNOSTICS_PREREQ_PLUGINS` must be set to the plugin callsigns to activate as prerequisites for Device Diagnostics testing | The `DEVICE_DIAGNOSTICS_PREREQ_PLUGINS` value should be correctly configured in the device-specific config file |
| 3 | Configure unified player app name | `DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME` must be set to the package/app ID of the unified player application to be installed | The `DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME` value should be correctly configured in the device-specific config file |
| 4 | Configure unified player app hosted URL | `DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_HOSTEDURL` must be set to the hosted download URL of the unified player application/package | The `DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_HOSTEDURL` value should be correctly configured in the device-specific config file |
| 5 | Configure unified player MD5 checksum value | `DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_MD5SUM_VALUE` must be set to the expected MD5 checksum of the unified player application/package for download integrity verification | The `DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_MD5SUM_VALUE` value should be correctly configured in the device-specific config file |
| 6 | Configure playback URL | `DEVICE_DIAGNOSTICS_PLAYBACK_URL` must be set to the media playback URL used by the unified player for Device Diagnostics testing | The `DEVICE_DIAGNOSTICS_PLAYBACK_URL` value should be correctly configured in the device-specific config file |
## Test Cases

<a id="devicediagnostics_get_configurations"></a>
### TestCase Name
DeviceDiagnostics_Get_Configurations

### TestCase ID
DD_01

### TestCase Objective
Gets value of provided property names

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get property configuration | Invoke getConfiguration on org.rdk.DeviceDiagnostics with names: "<DEVICE_DIAGNOSTICS_RFC_PARAMS>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DeviceDiagnostics.1.getConfiguration", "params": {"names": "<DEVICE_DIAGNOSTICS_RFC_PARAMS>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that configuration values are returned for the requested property names |

---

<a id="devicediagnostics_deactivate_activate_stress"></a>
### TestCase Name
DeviceDiagnostics_Deactivate_Activate_Stress

### TestCase ID
DD_02

### TestCase Objective
Deactivate and activate the device diagnostics plugin in a loop and check the CPU load

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Deactivate DeviceDiagnostics plugin | *(Stress loop: Repeated `<STRESS_TEST_REPEAT_COUNT>` times as configured)*<br>Invoke deactivate on Controller with callsign: "org.rdk.DeviceDiagnostics"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.DeviceDiagnostics"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is deactivated successfully |
| 2 | Activate DeviceDiagnostics plugin | *(Stress loop: Repeated `<STRESS_TEST_REPEAT_COUNT>` times as configured)*<br>Invoke activate on Controller with callsign: "org.rdk.DeviceDiagnostics"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DeviceDiagnostics"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Get CPU load | *(Stress loop: Repeated `<STRESS_TEST_REPEAT_COUNT>` times as configured)*<br>Invoke systeminfo on DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.systeminfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that the CPU load is retrieved and validated successfully |

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

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | *(Loop: Iterates for each plugin listed in <DEVICE_DIAGNOSTICS_PREREQ_PLUGINS>)*<br>Check plugin active status<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status", "params": {"plugin": "<DEVICE_DIAGNOSTICS_PREREQ_PLUGINS>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate <value> plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check plugin active status<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status", "params": {"plugin": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

#### TestCase Pre-condition 2: Check_Existing_Package_Before_Install

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check existing package | Get packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Verify that the package list is returned successfully |
| 2 | Uninstall existing package | *(Conditional statement executed only if package/app is currently present)*<br>Uninstall on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Download valid parameters | Download on DownloadManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that a valid downloadId is returned |
| 4 | Install package on device | Install on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.install", "params": {"packageId": "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "fileLocator": "<DOWNLOADED_FILE_LOCATOR_URL>", "name": "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", "value": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 5 | Verify installed package | Get packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Confirm that the installed package is present in the package list |

#### TestCase Pre-condition 3: PersistentStore_Set_and_Get_Value

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set value in PersistentStore | Set value on PersistentStore<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setValue", "params": {"namespace": "MVS", "key": "lightningURL", "value": "<DEVICE_DIAGNOSTICS_PLAYBACK_URL>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the value is set successfully |
| 2 | Get value from PersistentStore | Get value from PersistentStore<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getValue", "params": {"namespace": "MVS", "key": "lightningURL"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the stored playback URL matches the expected value `<DEVICE_DIAGNOSTICS_PLAYBACK_URL>` from the device config file  |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get AV decoder status | Invoke getAVDecoderStatus on org.rdk.DeviceDiagnostics<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DeviceDiagnostics.1.getAVDecoderStatus"}' http://127.0.0.1:9998/jsonrpc` | Verify that the AV decoder status is `"idle"`, indicating no active decoding  |
| 2 | Launch app valid params | Invoke launchApp on org.rdk.AppManager with appId: "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Check app launched | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |
| 4 | Get AV decoder status | Invoke getAVDecoderStatus on org.rdk.DeviceDiagnostics<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DeviceDiagnostics.1.getAVDecoderStatus"}' http://127.0.0.1:9998/jsonrpc` | Verify that the AV decoder status is `"active"`, indicating video/audio decoding is in progress  |
| 5 | Terminate app valid param | Invoke terminateApp on org.rdk.AppManager with appId: "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 6 | Get AV decoder status | Invoke getAVDecoderStatus on org.rdk.DeviceDiagnostics<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DeviceDiagnostics.1.getAVDecoderStatus"}' http://127.0.0.1:9998/jsonrpc` | Verify that the AV decoder status is `"idle"`, indicating no active decoding  |

### TestCase Post-condition

#### TestCase Post-condition 1: Terminate_Application

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check loaded apps | Get loaded apps from AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |
| 2 | Terminate app valid param | *(Conditional statement executed only if package/app is currently present)*<br>Terminate app on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Check package info | Get packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Verify that the package list is returned successfully |
| 4 | Uninstall existing package (conditional) | *(Conditional statement executed only if package/app is currently present)*<br>Uninstall on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

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

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | *(Loop: Iterates for each plugin listed in <DEVICE_DIAGNOSTICS_PREREQ_PLUGINS>)*<br>Check plugin active status<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status", "params": {"plugin": "<DEVICE_DIAGNOSTICS_PREREQ_PLUGINS>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate <value> plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check plugin active status<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status", "params": {"plugin": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

#### TestCase Pre-condition 2: Check_Existing_Package_Before_Install

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check existing package | Get packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Verify that the package list is returned successfully |
| 2 | Uninstall existing package | *(Conditional statement executed only if package/app is currently present)*<br>Uninstall on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Download valid parameters | Download on DownloadManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that a valid downloadId is returned |
| 4 | Install package on device | Install on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.install", "params": {"packageId": "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "fileLocator": "<DOWNLOADED_FILE_LOCATOR_URL>", "name": "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", "value": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 5 | Verify installed package | Get packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Confirm that the installed package is present in the package list |

#### TestCase Pre-condition 3: PersistentStore_Set_and_Get_Value

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set value in PersistentStore | Set value on PersistentStore<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.setValue", "params": {"namespace": "MVS", "key": "lightningURL", "value": "<DEVICE_DIAGNOSTICS_PLAYBACK_URL>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the value is set successfully |
| 2 | Get value from PersistentStore | Get value from PersistentStore<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PersistentStore.1.getValue", "params": {"namespace": "MVS", "key": "lightningURL"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the stored playback URL matches the expected value `<DEVICE_DIAGNOSTICS_PLAYBACK_URL>` from the device config file  |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get AV decoder status | Invoke getAVDecoderStatus on org.rdk.DeviceDiagnostics<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DeviceDiagnostics.1.getAVDecoderStatus"}' http://127.0.0.1:9998/jsonrpc` | Verify that the AV decoder status is `"idle"`, indicating no active decoding  |
| 2 | Launch app valid params | Invoke launchApp on org.rdk.AppManager with appId: "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Check app launched | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |
| 4 | Check onAVDecoderStatusChanged event | Listen for Event_OnAVDecoder_Status_Changed event (timeout: 60s) | Ensure the `onAVDecoderStatusChanged` event is received with `AVDecoderStatus` as `active` |
| 5 | Terminate app valid param | Invoke terminateApp on org.rdk.AppManager with appId: "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 6 | Check onAVDecoderStatusChanged event | Listen for Event_OnAVDecoder_Status_Changed event (timeout: 30s) | Ensure the `onAVDecoderStatusChanged` event is received with `AVDecoderStatus` as `idle` |

### TestCase Post-condition

#### TestCase Post-condition 1: Terminate_Application

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check loaded apps | Get loaded apps from AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |
| 2 | Terminate app valid param | *(Conditional statement executed only if package/app is currently present)*<br>Terminate app on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Check package info | Get packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Verify that the package list is returned successfully |
| 4 | Uninstall existing package (conditional) | *(Conditional statement executed only if package/app is currently present)*<br>Uninstall on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<DEVICE_DIAGNOSTICS_UNIFIED_PLAYER_APP_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="devicediagnostics_activatedeactivate_event_test"></a>
### TestCase Name
DeviceDiagnostics_ActivateDeactivate_Event_Test

### TestCase ID
DD_05

### TestCase Objective
Validates statechange event on activating/deactivating the plugin

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of DeviceDiagnostics plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DeviceDiagnostics"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate DeviceDiagnostics plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DeviceDiagnostics"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of DeviceDiagnostics plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DeviceDiagnostics"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Deactivate DeviceDiagnostics plugin | Invoke deactivate on Controller with callsign: "org.rdk.DeviceDiagnostics"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.DeviceDiagnostics"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is deactivated successfully |
| 2 | Check state change event | Listen for Event_Controller_State_Changed event (timeout: 2s) | Verify that the `statechange` event is received for callsign `org.rdk.DeviceDiagnostics` with state `deactivated` |
| 3 | Check plugin active status | Invoke status on Controller for org.rdk.DeviceDiagnostics<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DeviceDiagnostics"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |
| 4 | Activate DeviceDiagnostics plugin | Invoke activate on Controller with callsign: "org.rdk.DeviceDiagnostics"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DeviceDiagnostics"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 5 | Check state change event | Listen for Event_Controller_State_Changed event (timeout: 2s) | Verify that the `statechange` event is received for callsign `org.rdk.DeviceDiagnostics` with state `activated` |
| 6 | Check plugin active status | Invoke status on Controller for org.rdk.DeviceDiagnostics<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DeviceDiagnostics"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

---

<a id="devicediagnostics_activatedeactivate_all_event_test"></a>
### TestCase Name
DeviceDiagnostics_ActivateDeactivate_All_Event_Test

### TestCase ID
DD_06

### TestCase Objective
Validates all event on activating/deactivating the plugin

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of DeviceDiagnostics plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DeviceDiagnostics"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate DeviceDiagnostics plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DeviceDiagnostics"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of DeviceDiagnostics plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DeviceDiagnostics"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Deactivate DeviceDiagnostics plugin | Invoke deactivate on Controller with callsign: "org.rdk.DeviceDiagnostics"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.DeviceDiagnostics"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is deactivated successfully |
| 2 | Check all event | Listen for Event_Controller_All event (timeout: 2s) | Verify that the `all` event is received for callsign `org.rdk.DeviceDiagnostics` with state `deactivated` |
| 3 | Check plugin active status | Invoke status on Controller for org.rdk.DeviceDiagnostics<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DeviceDiagnostics"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |
| 4 | Activate DeviceDiagnostics plugin | Invoke activate on Controller with callsign: "org.rdk.DeviceDiagnostics"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DeviceDiagnostics"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 5 | Check all event | Listen for Event_Controller_All event (timeout: 2s) | Verify that the `all` event is received for callsign `org.rdk.DeviceDiagnostics` with state `activated` |
| 6 | Check plugin active status | Invoke status on Controller for org.rdk.DeviceDiagnostics<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DeviceDiagnostics"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

## Plugin Post-conditions

### Plugin Post-condition 1: Unregister_Events

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Unsubscribe from the onAVDecoderStatusChanged event | Unregister the WebSocket event listener for `onAVDecoderStatusChanged` to stop capturing AV decoder status change notifications.<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DeviceDiagnostics.1.unregister", "params": {"event": "onAVDecoderStatusChanged", "id": "client.events.1"}}` | Event unsubscription should be completed successfully and the event listener should be inactive |
| 2 | Unsubscribe from the statechange event | Unregister the WebSocket event listener for `statechange` to stop capturing plugin state change notifications.<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.unregister", "params": {"event": "statechange", "id": "client.events.1"}}` | Event unsubscription should be completed successfully and the event listener should be inactive |
| 3 | Unsubscribe from the all event | Unregister the WebSocket event listener for `all` to stop capturing all system event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.unregister", "params": {"event": "all", "id": "client.events.1"}}` | Event unsubscription should be completed successfully and the event listener should be inactive |

## Test Attributes

**Supported Models** : Video_Accelerator, RPI-Client

**Estimated duration** : 20 mins

**Priority** : High

**Release Version** : M81

<div align="right"><a href="#testscript-name">Go to Top</a></div>
