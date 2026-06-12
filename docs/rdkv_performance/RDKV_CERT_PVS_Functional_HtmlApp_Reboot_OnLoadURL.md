## TestCase ID
RDKV_PERFORMANCE_86
## TestCase Name
RDKV_CERT_PVS_Functional_HtmlApp_Reboot_OnLoadURL
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that HtmlApp remains stable and able to load a URL after a device reboot performed while a URL was loaded in HtmlApp.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|HtmlApp plugin should be available in the device build.|
|3|Test URL must be configured in `PerformanceTestVariables`.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Activate and Load URL in HtmlApp | Activate HtmlApp and load a URL: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"HtmlApp.1.url","params":{"url":"<test_url>"}}` | URL loaded successfully. |
| 3 | Reboot Device | Reboot the device while URL is loaded: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.harakiri"}` | Device reboots. |
| 4 | Wait for Device to Come Online | Wait for WPEFramework to restart. | Device online. |
| 5 | Verify HtmlApp Stability | After reboot, verify HtmlApp can be activated again. | HtmlApp plugin is available. |
| 6 | Load URL Again | Load the URL in HtmlApp again after reboot. | URL loaded successfully after reboot. |
| 7 | Validate Stability | Verify HtmlApp is stable with no crashes. | HtmlApp is stable and able to load URL after reboot. |
| 8 | Revert Plugin Status | Restore original plugin state. | Plugin reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 8

**Priority** : High

**Release Version** : M95<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
