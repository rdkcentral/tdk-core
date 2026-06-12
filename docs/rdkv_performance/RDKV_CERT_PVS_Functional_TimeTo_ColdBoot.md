## TestCase ID
RDKV_PERFORMANCE_93
## TestCase Name
RDKV_CERT_PVS_Functional_TimeTo_ColdBoot
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken for the device to cold boot and become fully operational is within the expected performance threshold.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|Device must be capable of cold boot (power off and power on).|
|2|WPEFramework process should be up and running after reboot.|
|3|`COLD_BOOT_TIME_THRESHOLD` must be configured in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Record Cold Boot Start Time | Record UTC timestamp when device power is cycled (cold boot started). | Start time recorded. |
| 2 | Power Cycle Device | Perform a cold boot on the device (power off, then power on). | Device powers off then begins booting. |
| 3 | Wait for Device to Come Online | Monitor the device until WPEFramework is up and responding. | Device online and WPEFramework running. |
| 4 | Record Boot Complete Time | Record UTC timestamp when the device is fully operational. | End time recorded. |
| 5 | Validate Cold Boot Time | Calculate cold boot time = end timestamp - start timestamp. Compare against threshold. | Device cold boot time is within the expected threshold. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 360

**Priority** : High

**Release Version** : M96<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
