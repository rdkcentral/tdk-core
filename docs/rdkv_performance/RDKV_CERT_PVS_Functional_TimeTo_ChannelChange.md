## TestCase ID
RDKV_PERFORMANCE_10
## TestCase Name
RDKV_CERT_PVS_Functional_TimeTo_ChannelChange
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to change from one channel/stream to another is within the expected performance threshold.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|A media playback plugin (e.g., WebKitBrowser or Cobalt) must be available.|
|3|Source and destination channel/stream URLs must be configured in `PerformanceTestVariables`.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Start Current Channel Playback | Start playback on the first stream/channel URL. | First channel playing. |
| 3 | Record Channel Change Start Time | Record UTC timestamp before issuing channel change. | Start time recorded. |
| 4 | Switch to Next Channel | Set the URL to the second channel/stream. | Channel change request sent. |
| 5 | Record Channel Change End Time | Record UTC timestamp after new channel begins playback. | End time recorded. |
| 6 | Validate Channel Change Time | Calculate channel change time = end timestamp - start timestamp. Compare against threshold. | Time to change channel is within the expected threshold. |
| 7 | Revert Plugin Status | Restore original plugin state. | Plugin reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M83<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
