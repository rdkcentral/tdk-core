## TestCase ID
RDKV_PERFORMANCE_3
## TestCase Name
RDKV_CERT_PVS_Functional_DiskUsage

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the disk usage of the configured partition on the device under test does not exceed 90%, ensuring sufficient disk space is available for normal device operation.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm device is accessible via SSH | The device under test must be accessible via SSH with valid credentials configured. | SSH connection to the device should be established successfully. |
| 2 | Configure device reboot preference | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 3 | Configure DISK_PARTITION in device config | `DISK_PARTITION` must be set to the partition name to be checked (e.g., /dev/root) in the device-specific config file. | The partition name should be correctly configured. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Establish SSH connection and read partition config | Obtain SSH connection parameters and retrieve the `DISK_PARTITION` value from the device-specific config file. | SSH parameters and the partition name should be retrieved successfully. |
| 2 | Query disk usage of the configured partition | SSH into the device and execute the disk usage command to obtain the usage percentage for the configured partition: <br>`df -h \| grep "<DISK_PARTITION>" \| awk '{print $5}'` | The disk usage percentage for the configured partition should be returned successfully without an exception. |
| 3 | Validate disk usage is below threshold | Parse the disk usage percentage from the command output and verify it is less than 90%. | The disk usage of the configured partition should be less than 90%. If usage is 90% or above, the test should report failure indicating critically high disk usage. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 5 mins

**Priority** : High

**Release Version** : M84<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
