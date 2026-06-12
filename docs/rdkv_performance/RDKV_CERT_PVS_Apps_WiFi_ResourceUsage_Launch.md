## TestCase ID
RDKV_PERFORMANCE_27
## TestCase Name
RDKV_CERT_PVS_Apps_WiFi_ResourceUsage_Launch
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that CPU load and memory usage are within acceptable ranges when a Lightning application is launched via WebKitBrowser while connected to a Wi-Fi network.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|WebKitBrowser, Cobalt, and DeviceInfo plugins should be available in the build.|
|3|Device must be connected to a Wi-Fi Access Point.|
|4|`app_url` (the Lightning application URL) must be configured in `PerformanceTestVariables`.|
|5|`WIFI_SSID` and `WIFI_PASSPHRASE` must be configured in device config.|
|6|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Connect to Wi-Fi | Ensure device is connected to the Wi-Fi SSID configured in device config. | Device connected to Wi-Fi. |
| 3 | Check Plugin Status | Check and activate WebKitBrowser and DeviceInfo, deactivate Cobalt. | Plugins confirmed in required state. |
| 4 | Launch Application over WiFi | Load the Lightning application URL in WebKitBrowser via Wi-Fi connection. | Application launches successfully over Wi-Fi. |
| 5 | Validate Resource Usage | Capture and validate CPU load and memory usage during application launch over Wi-Fi. | CPU load and memory usage during launch over Wi-Fi are within the expected acceptable limits. |
| 6 | Revert Plugin Status | Restore original plugin states. | Plugins reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 15

**Priority** : High

**Release Version** : M86<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
