## TestCase ID
RDKV_PERFORMANCE_82
## TestCase Name
RDKV_CERT_PVS_Browser_Strike_720_resolution
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the browser performance score using the Strike benchmark tool at 720p resolution is within the expected range.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|WebKitBrowser plugin should be available and activatable on the device.|
|3|Strike benchmark test URL for 720p resolution must be configured in `BrowserPerformanceVariables`.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Check Pre-conditions | Verify and set plugin states — activate WebKitBrowser, deactivate Cobalt: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@WebKitBrowser"}` | Plugins confirmed in required state. |
| 3 | Get Current URL | Query the current WebKitBrowser URL: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"WebKitBrowser.1.url"}` | Current URL retrieved. |
| 4 | Load Strike 720p Benchmark URL | Set the Strike benchmark URL configured for 720p resolution: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"WebKitBrowser.1.url","params":{"url":"<strike_720p_url>"}}` | Strike 720p benchmark URL loaded. |
| 5 | Wait for Benchmark Completion | Wait for Strike test to complete and collect the benchmark score. | Strike benchmark completes and score is retrieved. |
| 6 | Validate Strike 720p Score | Compare the Strike 720p score against configured threshold in `BrowserPerformanceVariables`. | Strike 720p score is within the expected range. |
| 7 | Revert Plugin Status | Restore original plugin states and URL. | Plugins and URL reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M97<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
