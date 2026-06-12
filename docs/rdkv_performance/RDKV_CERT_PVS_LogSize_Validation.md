## TestCase ID
RDKV_PERFORMANCE_144
## TestCase Name
RDKV_CERT_PVS_LogSize_Validation
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the size of the device log files does not exceed the acceptable threshold, ensuring proper log management.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Log file path and size threshold must be configured in device config.|
|3|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Query Log File Sizes | Retrieve the sizes of relevant log files from the configured log file paths on the device. | Log file size data retrieved. |
| 3 | Validate Log File Sizes | Compare the size of each log file against the configured acceptable size threshold. | All log file sizes are within the configured threshold limits. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M123<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
