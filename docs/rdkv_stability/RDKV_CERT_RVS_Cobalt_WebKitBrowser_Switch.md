## TestCase ID
RDKV_STABILITY_41
## TestCase Name
RDKV_CERT_RVS_Cobalt_WebKitBrowser_Switch
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate device stability by alternating between Cobalt video playback and WebKitBrowser URL loading for lifecycle_max_count iterations using the Home key to switch focus, verifying CPU and memory usage remains within expected limits throughout.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Both Cobalt and WebKitBrowser plugins must be available in the supported plugins list.|
|3|cobalt_test_url, webkit_test_url, and lifecycle_max_count must be configured in StabilityTestVariables.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using `check_device_state`. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of Cobalt, WebKitBrowser, and DeviceInfo plugins. Set required states: Cobalt=deactivated, WebKitBrowser=deactivated, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Cobalt-WebKitBrowser switch loop (repeat for lifecycle_max_count iterations) | For each iteration: <br>Launch Cobalt via `org.rdk.RDKShell.1.launch`. <br>Set video URL in Cobalt via deeplink: `{"jsonrpc":"2.0","id":1234567890,"method":"Cobalt.1.deeplink","params":{"url":"<cobalt_test_url>"}}` <br>Validate video is playing via `rdkservice_validateProcEntry`. <br>Press Home key to switch focus: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.generateKey","params":{"keyCode":36,"modifiers":[],"client":"Cobalt"}}` <br>Launch WebKitBrowser via `org.rdk.RDKShell.1.launch`. <br>Set URL in WebKitBrowser: `{"jsonrpc":"2.0","id":1234567890,"method":"WebKitBrowser.1.url","params":{"value":"<webkit_test_url>"}}` <br>Verify URL is set: `{"jsonrpc":"2.0","id":1234567890,"method":"WebKitBrowser.1.url"}` <br>Press Home key to switch back: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.generateKey","params":{"keyCode":36,"modifiers":[],"client":"WebKitBrowser"}}` <br>Validate CPU load and memory usage via `rdkservice_validateResourceUsage`. | Cobalt should play video and WebKitBrowser should load URL successfully in each iteration. CPU load and memory usage should remain within expected limits. |
| 4 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all iteration data. |
| 5 | Revert plugins | Restore plugins to their original state using `rdkservice_setPluginStatus`. | Plugins should be reverted to their pre-test states. |
| 6 | Check device state post-condition | Verify the device is still in a stable state after completing the test using `check_device_state`. | Device should remain stable after the stress test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, RPI-HYB, Video_Accelerator

**Estimated duration** : 5000

**Priority** : High

**Release Version** : M90<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
