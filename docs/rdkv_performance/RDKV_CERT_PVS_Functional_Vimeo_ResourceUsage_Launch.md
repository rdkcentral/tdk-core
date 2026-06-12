## TestCase ID
RDKV_PERFORMANCE_128
## TestCase Name
RDKV_CERT_PVS_Functional_Vimeo_ResourceUsage_Launch
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that CPU load and memory usage are within acceptable ranges when the Vimeo application is launched.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|The application plugin used for Vimeo (e.g., Cobalt, HtmlApp, or WebKitBrowser) must be available in the build.|
|3|Vimeo app URL or configuration must be set in `PerformanceTestVariables`.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Capture Baseline Resource Usage | Record CPU and memory usage before launching Vimeo. | Baseline recorded. |
| 3 | Launch Vimeo Application | Activate the application plugin and navigate to the Vimeo URL. | Vimeo application launched. |
| 4 | Capture Resource Usage After Launch | Record CPU and memory usage after Vimeo launch. | Resource data captured. |
| 5 | Validate Resource Usage | Verify CPU load and memory usage during Vimeo launch are within acceptable limits. | CPU load and memory usage during Vimeo launch are within the expected limits. |
| 6 | Revert Plugin Status | Restore original plugin state. | Plugin reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 5

**Priority** : High

**Release Version** : M104<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
