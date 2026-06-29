## TestCase ID
RDKV_PERFORMANCE_4
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
To validate that the CPU I/O wait time on the device does not exceed the acceptable threshold calculated as (1 / number of CPU cores), confirming that the CPU cores are not waiting excessively for the disk subsystem.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm device is accessible via SSH | The device under test must be accessible via SSH with valid credentials configured. | SSH connection to the device should be established successfully. |
| 2 | Configure device reboot preference | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Establish SSH connection to device | Obtain SSH connection parameters for the device under test to enable remote command execution. | SSH parameters should be retrieved successfully and the connection should be established. |
| 2 | Determine the number of CPU cores | SSH into the device and query the number of available CPU cores by reading the processor entries from the CPU info file: <br>`grep -c processor /proc/cpuinfo` | The number of CPU cores should be returned successfully. |
| 3 | Measure CPU I/O wait percentage | SSH into the device and retrieve the current I/O wait percentage using the iostat tool: <br>`iostat -c \| sed -n '4p' \| sed 's/  */ /g' \| cut -d ' ' -f5` | The iowait percentage value should be returned successfully without an exception. |
| 4 | Validate I/O wait time against CPU core threshold | Calculate the acceptable iowait threshold as `(1 / number_of_CPU_cores)` and compare the measured iowait percentage against this threshold. The iowait percentage must not exceed this value. | The iowait percentage should be less than or equal to `(1 / number_of_CPU_cores)`. If iowait exceeds this threshold, the CPU cores are waiting excessively for the disk subsystem and the test should report failure. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10 mins

**Priority** : High

**Release Version** : M107<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
