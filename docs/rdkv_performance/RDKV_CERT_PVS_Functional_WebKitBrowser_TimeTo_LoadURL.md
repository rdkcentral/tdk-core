## TestCase ID
RDKV_PERFORMANCE_09
## TestCase Name
RDKV_CERT_PVS_Functional_WebKitBrowser_TimeTo_LoadURL
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to load a URL in WebKitBrowser is within the expected performance threshold.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|WebKitBrowser plugin should be available in the device build.|
|3|Test URL must be configured in `PerformanceTestVariables`.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Activate WebKitBrowser | Activate WebKitBrowser plugin: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.activate","params":{"callsign":"WebKitBrowser"}}` | WebKitBrowser activated. |
| 3 | Record Load URL Start Time | Record UTC timestamp before setting the URL. | Start time recorded. |
| 4 | Load URL in WebKitBrowser | Set the test URL: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"WebKitBrowser.1.url","params":{"url":"<test_url>"}}` | URL load request sent. |
| 5 | Record URL Loaded Time | Record UTC timestamp when the URL is fully loaded (page ready). | End time recorded. |
| 6 | Validate Time | Calculate URL load time = end timestamp - start timestamp. Compare against threshold. | Time to load URL in WebKitBrowser is within the expected threshold. |
| 7 | Revert Plugin Status | Restore original plugin state. | Plugin reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 6

**Priority** : High

**Release Version** : M83<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
