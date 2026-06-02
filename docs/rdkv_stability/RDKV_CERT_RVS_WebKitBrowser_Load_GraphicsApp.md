## TestCase ID
RDKV_STABILITY_36
## TestCase Name
RDKV_CERT_RVS_WebKitBrowser_Load_GraphicsApp
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that resource usage (CPU and memory) remains within acceptable limits while playing a graphics application URL in a Lightning app installed via AppManager for a minimum of 6 hours.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|`graphics_app_url` must be configured in StabilityTestVariables with a valid graphics/animation app URL (e.g., `http://<TM-IP>:8080/rdk-test-tool/fileStore/lightning-apps/tdkobjectanimations/build/index.html?count=100&showfps=false&object=Rect&autotest=true&duration=21600`).|
|3|`animation_graphics_app_download_url` must be configured in MediaValidationVariables with the full `.bolt` package URL for the animation/graphics app to be downloaded and installed on the device.|
|4|`bolt_packages_base_path` must be configured in MediaValidationVariables with the base URL of the bolt package repository (e.g., `http://<TM_IP>:8443/images/`).|
|5|`load_graphics_app_test_duration` is configured in StabilityTestVariables as 360 minutes (6 hours) by default.|
|6|DeviceInfo and org.rdk.PersistentStore plugins must be available in the build and accessible via WPEFramework Controller.|
|7|org.rdk.DownloadManager, org.rdk.PackageManagerRDKEMS, and org.rdk.AppManager plugins must be available in the build for app installation.|
|8|Device should be rebooted before test execution if `PRE_REQ_REBOOT` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Pre-requisite Reboot | Conditionally reboot the device before the test. `pre_requisite_reboot()` reads the `PRE_REQ_REBOOT` key from the device-specific config file. If set to "Yes", the device is rebooted via `Controller.1.harakiri` and the script waits 150 seconds for it to come back online. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.harakiri"} | Device should come back online successfully if reboot was triggered. |
| 2 | Check Device Pre-condition State | Validate initial CPU and memory resource usage before the test begins using `check_device_state()`. Activates DeviceInfo plugin if not active, invokes `rdkservice_validateResourceUsage`, then reverts DeviceInfo plugin state. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@DeviceInfo"}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "rdkservice_validateResourceUsage"} | CPU and memory usage should be within the expected range before the test starts. |
| 3 | Check and Activate Required Plugins | Read the current status of DeviceInfo and org.rdk.PersistentStore plugins. If either is not in the required state (`activated`), activate them and save the original statuses for revert on exit. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@DeviceInfo"}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.PersistentStore"}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.PersistentStore"}} | Both DeviceInfo and org.rdk.PersistentStore plugins should be in activated state. |
| 4 | Set Graphics App URL in PersistentStore | Store the configured `graphics_app_url` (from StabilityTestVariables) into the `lightningURL` key of the `MVS` namespace in PersistentStore. This makes the URL available to the Lightning app on launch. <br>{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.PersistentStore.setValue", "params": {"namespace": "MVS", "key": "lightningURL", "value": "<graphics_app_url>"}} | The graphics app URL should be set successfully in PersistentStore under namespace `MVS`, key `lightningURL`. |
| 5 | Check if Graphics App is Installed | Query PackageManagerRDKEMS for the list of installed packages to determine whether the animation/graphics app (derived from `animation_graphics_app_download_url`) is already installed on the device. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"} | Package list should be retrieved successfully. If the app is already installed, the installation steps are skipped. |
| 6 | Activate App Manager Plugins (if app not installed) | If the graphics app is not installed, check the status of org.rdk.DownloadManager, org.rdk.PackageManagerRDKEMS, and org.rdk.AppManager plugins and activate them if not already activated. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.DownloadManager"}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.AppManager"}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DownloadManager"}}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.PackageManagerRDKEMS"}}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.AppManager"}} | All three app management plugins should be in activated state before download and install. |
| 7 | Download Graphics App Bundle | Download the animation/graphics app `.bolt` package from `animation_graphics_app_download_url` using DownloadManager. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<animation_graphics_app_download_url>"}} | Download should complete successfully and return a download ID. |
| 8 | Install Graphics App Bundle | Install the downloaded `.bolt` package using PackageManagerRDKEMS with the app ID derived from the bundle filename, version 0.1.0, and the file locator path from the download result. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "<app_id>", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<download_path>"}} | App should be installed successfully and appear in the installed package list. |
| 9 | Launch Graphics App via AppManager | Launch the installed animation/graphics app using AppManager. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "<app_id>", "intent": "", "launchArgs": ""}} | App should launch successfully. The test waits 60 seconds for the app to fully start before beginning resource monitoring. |
| 10 | Monitor App and Validate Resource Usage | For 360 minutes (6 hours), at 30-second intervals: check that the app is still in `APP_STATE_ACTIVE` state via `org.rdk.AppManager.getLoadedApps`, then invoke `rdkservice_validateResourceUsage` to record CPU load and memory usage. If the app is not found in the loaded apps list, the test fails immediately. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.getLoadedApps"}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "rdkservice_validateResourceUsage"} | The graphics app should remain in `APP_STATE_ACTIVE` state throughout the test and CPU/memory usage should stay within expected limits at every 30-second checkpoint. |
| 11 | Save Resource Usage Log | After all monitoring iterations complete, write all per-iteration CPU load and memory usage readings to a JSON log file (`CPUMemoryInfo.json`) in the test execution log path. | JSON log file should be created with all recorded CPU and memory data points from the 6-hour test. |
| 12 | Terminate Graphics App | Terminate the graphics app using AppManager after the test duration completes. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<app_id>"}} | The app should be terminated successfully. |
| 13 | Revert Plugin Statuses | If any plugins (DeviceInfo, org.rdk.PersistentStore) were changed from their original state in Step 3, revert them back to their original states using `set_plugins_status`. | Plugin states should be restored to their pre-test values. |
| 14 | Check Device Post-condition State | Validate CPU and memory resource usage after the test completes using `check_device_state()` to confirm the device remains in a healthy state. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "rdkservice_validateResourceUsage"} | CPU and memory usage should be within the expected range after the 6-hour graphics app playback test completes. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 370

**Priority** : High

**Release Version** : M89<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
