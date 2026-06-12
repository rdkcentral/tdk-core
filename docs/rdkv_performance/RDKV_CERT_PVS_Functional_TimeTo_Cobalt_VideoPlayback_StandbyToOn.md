## TestCase ID
RDKV_PERFORMANCE_35
## TestCase Name
RDKV_CERT_PVS_Functional_TimeTo_Cobalt_VideoPlayback_StandbyToOn
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken for Cobalt video playback to start after a Standby-to-On power state transition is within the expected performance threshold.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Cobalt plugin must be available in the device build.|
|3|`org.rdk.System` plugin must be available for power state management.|
|4|Video URL must be configured in `PerformanceTestVariables`.|
|5|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Activate Cobalt and Start Video Playback | Activate Cobalt and begin video playback. | Video playing. |
| 3 | Set Device to Standby | Set power state to Standby: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.System.1.setPowerState","params":{"powerState":"STANDBY","standbyReason":"TDKTest"}}` | Device enters Standby. |
| 4 | Record Standby-to-On Start Time | Record UTC timestamp before transitioning to On. | Start time recorded. |
| 5 | Set Device to On | Transition device to On state: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.System.1.setPowerState","params":{"powerState":"ON","standbyReason":""}}` | Transition to On initiated. |
| 6 | Record Video Playback Start Time | Record UTC timestamp when video playback resumes on Cobalt. | Video playback resumed. |
| 7 | Validate Time | Calculate elapsed time = video start time - transition start time. Compare against threshold. | Time to resume Cobalt video playback from Standby-to-On is within the expected threshold. |
| 8 | Revert Plugin Status | Restore original plugin state. | Plugin reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M87<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
