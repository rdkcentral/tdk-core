## TestCase ID
RDKV_PERFORMANCE_135
## TestCase Name
RDKV_CERT_PVS_Functional_Zombie_Processes
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that no zombie processes are present on the device, ensuring proper process lifecycle management.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Query Running Processes | Run `ps aux` or equivalent on the device to list all processes and check for zombie state (`Z` status). | Process list retrieved. |
| 3 | Validate No Zombie Processes | Verify that no processes are in the zombie state (state `Z`). | No zombie processes are present on the device. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 4

**Priority** : High

**Release Version** : M107<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
