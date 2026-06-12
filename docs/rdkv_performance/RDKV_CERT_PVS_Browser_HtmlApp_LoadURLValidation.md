## TestCase ID
RDKV_PERFORMANCE_137
## TestCase Name
RDKV_CERT_PVS_Browser_HtmlApp_LoadURLValidation
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that a URL is loaded correctly in the HtmlApp plugin by verifying the API response and comparing with the webinspect page content.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|HtmlApp plugin should be available and activatable on the device.|
|3|Test URL and webinspect port must be configured in `BrowserPerformanceVariables`.|
|4|`WEBINSPECT_PORT` must be configured in device config.|
|5|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Check Plugin Status | Verify and activate HtmlApp plugin: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@HtmlApp"}` | HtmlApp plugin is in activated state. |
| 3 | Load URL in HtmlApp | Set the test URL in HtmlApp: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"HtmlApp.1.url","params":{"url":"<test_url>"}}` | URL set successfully. |
| 4 | Validate API Response | Read back the URL from HtmlApp API and confirm it matches the set URL: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"HtmlApp.1.url"}` | API response matches the expected URL. |
| 5 | Validate via Webinspect | Connect to the webinspect endpoint on the configured port and verify the page content loaded. | Webinspect confirms the URL is loaded correctly. |
| 6 | Revert Plugin Status | Restore original plugin states. | Plugins reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M111<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
