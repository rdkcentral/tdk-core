## TestCase ID
RDKV_PERFORMANCE_151
## TestCase Name
RDKV_CERT_PVS_HibernateRestore_DiskUsage
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the disk usage of the `/dev/root` partition does not exceed the acceptable threshold after a hibernate and restore cycle.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Device must support hibernation (power state transitions to LIGHT_SLEEP or DEEP_SLEEP).|
|3|`org.rdk.System` plugin should be available for power state management.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Record Baseline Disk Usage | Query the disk usage of `/dev/root` before hibernation. | Baseline disk usage recorded. |
| 3 | Enter Hibernate State | Set device power state to hibernate (DEEP_SLEEP or LIGHT_SLEEP): <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.System.1.setPowerState","params":{"powerState":"DEEP_SLEEP","standbyReason":"TDKTest"}}` | Device enters hibernate state. |
| 4 | Restore Device | Restore device from hibernate state to On: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.System.1.setPowerState","params":{"powerState":"ON","standbyReason":""}}` | Device restored from hibernate. |
| 5 | Record Disk Usage After Restore | Query the disk usage of `/dev/root` after restore. | Post-restore disk usage recorded. |
| 6 | Validate Disk Usage | Verify that disk usage of `/dev/root` is below 90% after hibernate and restore cycle. | Disk usage of `/dev/root` partition is within acceptable limits after hibernate and restore. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M130<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
