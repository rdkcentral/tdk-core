## TestCase ID
RDKV_PERFORMANCE_60
## TestCase Name
RDKV_CERT_PVS_Functional_ValidateIPAddress
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the device is assigned a valid IP address on the active network interface.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Device must be connected to an active network (Ethernet or WiFi).|
|3|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Query Network Interface IP | Check the IP address assigned to the active network interface. | IP address information returned. |
| 3 | Validate IP Address | Verify that the IP address is a valid, non-zero, non-APIPA address in the correct subnet. | Device is assigned a valid IP address on the active network interface. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 5

**Priority** : High

**Release Version** : M91<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
