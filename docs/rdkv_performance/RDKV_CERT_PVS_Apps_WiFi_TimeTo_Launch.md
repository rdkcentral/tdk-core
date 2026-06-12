## TestCase ID
RDKV_PERFORMANCE_28
## TestCase Name
RDKV_CERT_PVS_Apps_WiFi_TimeTo_Launch
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to launch a Lightning application via WebKitBrowser while connected to a Wi-Fi network is within the expected performance threshold.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|WebKitBrowser, Cobalt, and DeviceInfo plugins should be available in the build.|
|3|Device must be connected to a Wi-Fi Access Point.|
|4|`app_url` must be configured in `PerformanceTestVariables`.|
|5|`WIFI_SSID` and `WIFI_PASSPHRASE` must be configured in device config.|
|6|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Connect to Wi-Fi | Ensure device is connected to the Wi-Fi SSID configured in device config. | Device connected to Wi-Fi. |
| 3 | Check Plugin Status | Check and activate WebKitBrowser and DeviceInfo, deactivate Cobalt. | Plugins confirmed in required state. |
| 4 | Record Launch Start Time | Record current UTC timestamp immediately before loading the application URL. | Start time recorded. |
| 5 | Load Application URL via Wi-Fi | Set the Lightning application URL in WebKitBrowser: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"WebKitBrowser.1.url","params":{"url":"<app_url>"}}` | URL set successfully. |
| 6 | Detect Application Ready | Monitor WebKitBrowser for the URL load completion event. Record the ready timestamp. | Application ready state detected. |
| 7 | Calculate and Validate Launch Time | Calculate launch time = ready timestamp - start timestamp. Compare against the configured threshold. | Launch time over Wi-Fi is within the expected threshold. |
| 8 | Revert Plugin Status | Restore original plugin states. | Plugins reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 17

**Priority** : High

**Release Version** : M86<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
