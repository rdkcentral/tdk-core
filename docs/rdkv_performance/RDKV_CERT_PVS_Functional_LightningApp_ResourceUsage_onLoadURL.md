## TestCase ID
RDKV_PERFORMANCE_78
## TestCase Name
RDKV_CERT_PVS_Functional_LightningApp_ResourceUsage_onLoadURL
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that CPU load and memory usage are within acceptable ranges when a URL is loaded in LightningApp.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|LightningApp plugin should be available in the device build.|
|3|Test URL must be configured in `PerformanceTestVariables`.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Activate LightningApp | Activate LightningApp plugin: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.activate","params":{"callsign":"LightningApp"}}` | LightningApp activated. |
| 3 | Load URL in LightningApp | Load the test URL: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"LightningApp.1.url","params":{"url":"<test_url>"}}` | URL loading started. |
| 4 | Capture Resource Usage | Record CPU and memory usage during URL loading. | Resource data captured. |
| 5 | Validate Resource Usage | Verify CPU load and memory usage during URL load are within acceptable limits. | CPU load and memory usage are within the expected limits. |
| 6 | Revert Plugin Status | Restore original plugin state. | Plugin reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 2

**Priority** : High

**Release Version** : M94<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
