## TestCase ID
RDKV_PERFORMANCE_142
## TestCase Name
RDKV_CERT_PVS_Functional_ResourceUsage_HtmlApp_Launch_StandbyToOn
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that CPU load and memory usage are within acceptable ranges when HtmlApp is launched after transitioning the device from Standby to On power state.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|HtmlApp plugin should be available in the device build.|
|3|`org.rdk.System` plugin should be available for power state management.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Set Device to Standby | Set power state to Standby: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.System.1.setPowerState","params":{"powerState":"STANDBY","standbyReason":"TDKTest"}}` | Device in Standby state. |
| 3 | Capture Baseline Resource Usage | Record CPU and memory usage in Standby state. | Baseline recorded. |
| 4 | Set Device to On | Transition device from Standby to On: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.System.1.setPowerState","params":{"powerState":"ON","standbyReason":""}}` | Device power state changed to On. |
| 5 | Launch HtmlApp | Activate HtmlApp plugin: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.activate","params":{"callsign":"HtmlApp"}}` | HtmlApp launched. |
| 6 | Capture Resource Usage After Launch | Record CPU and memory usage after HtmlApp launch following standby-to-on transition. | Resource data captured. |
| 7 | Validate Resource Usage | Verify CPU load and memory usage are within acceptable limits. | CPU load and memory usage after HtmlApp launch following Standby-to-On transition are within the expected limits. |
| 8 | Revert Plugin Status | Restore original plugin state. | Plugin reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M115<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
