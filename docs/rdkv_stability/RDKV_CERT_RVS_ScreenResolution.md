## TestCase ID
RDKV_STABILITY_13
## TestCase Name
RDKV_CERT_RVS_ScreenResolution
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate device stability by repeatedly changing the screen resolution via RDKShell for change_resolution_max_count iterations across all supported resolutions, verifying each resolution is applied correctly and CPU/memory usage remains within expected limits.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|WebKitBrowser plugin must be launched; Cobalt must be deactivated; DeviceInfo must be activated.|
|3|resolutions_list and change_resolution_max_count must be configured in StabilityTestVariables.|
|4|org.rdk.RDKShell plugin must be available on the device.|
|5|Optionally, org.rdk.ScreenCapture plugin may be available if SC_VALIDATION_NEEDED is set to Yes.|
|6|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using `check_device_state`. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of WebKitBrowser, Cobalt, and DeviceInfo plugins. Set required states: WebKitBrowser=deactivated (to be launched), Cobalt=deactivated, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Launch WebKitBrowser and set URL | Launch WebKitBrowser via `launch_plugin`. If SC_VALIDATION_NEEDED is Yes, activate org.rdk.ScreenCapture plugin. Get current WebKitBrowser URL and save as initial. Set the webkit_url for testing. | WebKitBrowser should launch and URL should be set. |
| 4 | Change resolution loop (repeat for change_resolution_max_count iterations cycling through resolutions_list) | For each iteration and for each resolution in resolutions_list: <br>Set screen resolution via RDKShell: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.setScreenResolution","params":{"client":"WebKitBrowser","w":<width>,"h":<height>}}` <br>If SC_VALIDATION_NEEDED: Capture screenshot via `org.rdk.ScreenCapture.1.uploadScreenCapture` and verify it. <br>Validate CPU load and memory usage via `rdkservice_validateResourceUsage`. | Screen resolution should be set successfully. Screenshot capture (if configured) should succeed. CPU load and memory usage should remain within expected limits. |
| 5 | Restore original URL | Set WebKitBrowser URL back to the original URL retrieved before the test. | Original URL should be restored. |
| 6 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all iteration data. |
| 7 | Revert plugins | Restore plugins to their original state using `rdkservice_setPluginStatus`. | Plugins should be reverted to their pre-test states. |
| 8 | Check device state post-condition | Verify the device is still in a stable state after completing the test using `check_device_state`. | Device should remain stable after the screen resolution stress test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, RPI-HYB, Video_Accelerator

**Estimated duration** : 720

**Priority** : High

**Release Version** : M85<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
