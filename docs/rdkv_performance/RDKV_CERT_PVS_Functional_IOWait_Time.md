## TestCase ID
RDKV_PERFORMANCE_134
## TestCase Name
RDKV_CERT_PVS_Functional_IOWait_Time
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the device CPUs are not waiting for a significant amount of time for the disk subsystem, confirming IOWait time is within acceptable limits.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|`IOWAIT_TIME_THRESHOLD` must be configured in device config.|
|3|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Capture IOWait Data | Run `iostat` or equivalent command on the device to capture CPU IOWait percentage. | IOWait data captured. |
| 3 | Validate IOWait Time | Compare the IOWait percentage against `IOWAIT_TIME_THRESHOLD` configured in device config. | IOWait time is below the threshold, indicating CPUs are not significantly waiting for disk operations. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M107<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
