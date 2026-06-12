## TestCase ID
RDKV_PERFORMANCE_122
## TestCase Name
RDKV_CERT_PVS_Browser_SmashCat
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the average FPS value from the SmashCat browser performance benchmark is within the expected range.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|WebKitBrowser plugin should be available and activatable on the device.|
|3|SmashCat benchmark test URL must be configured in `BrowserPerformanceVariables`.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Check Pre-conditions | Verify and set plugin states — activate WebKitBrowser, deactivate Cobalt: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@WebKitBrowser"}` | Plugins confirmed in required state. |
| 3 | Get Current URL | Query the current WebKitBrowser URL: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"WebKitBrowser.1.url"}` | Current URL retrieved. |
| 4 | Load SmashCat Benchmark URL | Set the SmashCat benchmark URL in WebKitBrowser: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"WebKitBrowser.1.url","params":{"url":"<smashcat_test_url>"}}` | SmashCat benchmark URL loaded. |
| 5 | Wait for Benchmark Completion | Wait for SmashCat test to complete and collect the average FPS score. | SmashCat benchmark completes and FPS score is retrieved. |
| 6 | Validate FPS Score | Compare SmashCat FPS score against configured threshold in `BrowserPerformanceVariables`. | SmashCat FPS score is within the expected range. |
| 7 | Revert Plugin Status | Restore original plugin states and URL. | Plugins and URL reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 5

**Priority** : High

**Release Version** : M101<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
