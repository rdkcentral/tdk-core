## TestCase ID
RDKV_PERFORMANCE_02
## TestCase Name
RDKV_CERT_PVS_Apps_TimeTo_Launch
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to launch a Lightning application in WebKitBrowser is within the expected performance threshold.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|WebKitBrowser, Cobalt, and DeviceInfo plugins should be available in the build.|
|3|The Lightning application URL must be configured in `PerformanceTestVariables`.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Check Pre-conditions | Verify and set plugin states — activate WebKitBrowser, deactivate Cobalt: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@WebKitBrowser"}` | Plugin state confirmed. |
| 3 | Record Launch Start Time | Record current UTC timestamp immediately before loading the application URL. | Start time recorded. |
| 4 | Load Application URL | Set the Lightning application URL in WebKitBrowser: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"WebKitBrowser.1.url","params":{"url":"<app_url>"}}` | URL set successfully. |
| 5 | Detect Application Ready | Monitor WebKitBrowser for the URL change event or page load completion. Record the ready timestamp. | Application ready state detected. |
| 6 | Calculate and Validate Launch Time | Calculate launch time = ready timestamp - start timestamp. Compare against the configured threshold from device config. | Launch time is within the expected threshold. |
| 7 | Revert Plugin Status | Restore original plugin states. | Plugins reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 6

**Priority** : High

**Release Version** : M82<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
