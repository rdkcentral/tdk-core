## TestCase ID
RDKV_STABILITY_28
## TestCase Name
RDKV_CERT_RVS_MoveToBack
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate the RDKShell moveToBack functionality by launching both Cobalt and WebKitBrowser plugins and repeatedly moving them to the back of the z-order for moveto_operation_max_count iterations, verifying the z-order changes correctly and CPU/memory usage remains within expected limits.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Both Cobalt and WebKitBrowser plugins must be available in the supported plugins list.|
|3|moveto_operation_max_count must be configured in StabilityTestVariables.|
|4|webkit_url (e.g., https://www.google.com/) must be configured in StabilityTestVariables.|
|5|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using applicable API calls. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of Cobalt, WebKitBrowser, and DeviceInfo plugins. Set required states: Cobalt=deactivated, WebKitBrowser=deactivated, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Launch Cobalt and WebKitBrowser | Launch Cobalt via applicable API calls. Launch WebKitBrowser via applicable API calls. Set webkit_url in WebKitBrowser: `{"jsonrpc":"2.0","id":1234567890,"method":"WebKitBrowser.1.url","params":{"value":"<webkit_url>"}}` | Both Cobalt and WebKitBrowser should launch successfully. |
| 4 | Get initial z-order | Get the current z-order list via `org.rdk.RDKShell.1.getZOrder`. Identify exclude_from_zorder plugins (system plugins to skip). | Z-order should be retrieved with Cobalt and WebKitBrowser present. |
| 5 | MoveToBack loop (repeat for moveto_operation_max_count iterations) | For each iteration: <br>Get current z-order via `org.rdk.RDKShell.1.getZOrder`. <br>Determine which plugin is currently at the back of the z-order. <br>Move the frontmost plugin to back: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.moveToBack","params":{"client":"<plugin>"}}` <br>Get z-order again to verify the plugin moved to back. <br>Validate CPU load and memory usage via applicable API calls. | Plugin should be moved to the back of the z-order successfully. Z-order verification should confirm the change. CPU load and memory usage should remain within expected limits. |
| 6 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all iteration data. |
| 7 | Revert plugins | Restore plugins to their original state using applicable API calls. | Plugins should be reverted to their pre-test states. |
| 8 | Check device state post-condition | Verify the device is still in a stable state after completing the test using applicable API calls. | Device should remain stable after the moveToBack stress test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 720

**Priority** : High

**Release Version** : M88<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
