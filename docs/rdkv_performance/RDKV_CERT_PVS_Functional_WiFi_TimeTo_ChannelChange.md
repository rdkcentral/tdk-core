## TestCase ID
RDKV_PERFORMANCE_25
## TestCase Name
RDKV_CERT_PVS_Functional_WiFi_TimeTo_ChannelChange
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to perform a channel change during WiFi-connected video playback is within the expected performance threshold.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Device must be connected to a WiFi network.|
|3|Source and destination channel/stream URLs must be configured in `PerformanceTestVariables`.|
|4|`WIFI_CHANNEL_CHANGE_THRESHOLD` must be configured in device config.|
|5|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Verify WiFi Connection | Confirm device is connected to WiFi. | WiFi connection confirmed. |
| 3 | Start Current Channel Playback | Start playback on the first stream/channel URL over WiFi. | First channel playing. |
| 4 | Record Channel Change Start Time | Record UTC timestamp before issuing channel change. | Start time recorded. |
| 5 | Switch to Next Channel | Set the URL to the second channel/stream. | Channel change request sent. |
| 6 | Record Channel Change End Time | Record UTC timestamp after new channel begins playback. | End time recorded. |
| 7 | Validate Channel Change Time | Calculate channel change time = end timestamp - start timestamp. Compare against threshold. | Time to change channel over WiFi is within the expected threshold. |
| 8 | Revert Plugin Status | Restore original plugin state. | Plugin reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 12

**Priority** : High

**Release Version** : M85<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
