## TestCase ID
RDKV_PERFORMANCE_99
## TestCase Name
RDKV_CERT_PVS_Browser_Speedometer
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the responsiveness score of web applications measured by the Speedometer browser benchmark is within the expected range.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|WebKitBrowser plugin should be available and activatable on the device.|
|3|Speedometer benchmark test URL must be configured in `BrowserPerformanceVariables`.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Check Pre-conditions | Verify and set plugin states — activate WebKitBrowser, deactivate Cobalt: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@WebKitBrowser"}` | Plugins confirmed in required state. |
| 3 | Get Current URL | Query the current WebKitBrowser URL: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"WebKitBrowser.1.url"}` | Current URL retrieved. |
| 4 | Load Speedometer Benchmark URL | Set the Speedometer benchmark URL in WebKitBrowser: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"WebKitBrowser.1.url","params":{"url":"<speedometer_test_url>"}}` | Speedometer benchmark URL loaded. |
| 5 | Wait for Benchmark Completion | Wait for Speedometer test to complete (up to 40 minutes) and collect the final responsiveness score. | Speedometer benchmark completes and score is retrieved. |
| 6 | Validate Speedometer Score | Compare Speedometer score against configured threshold in `BrowserPerformanceVariables`. | Speedometer score is within the expected range. |
| 7 | Revert Plugin Status | Restore original plugin states and URL. | Plugins and URL reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 40

**Priority** : High

**Release Version** : M97<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
