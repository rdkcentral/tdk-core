## TestCase ID
RDKV_PERFORMANCE_24
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
To validate that there are no zombie processes running on the device under test, by querying the process list via SSH and verifying the zombie process count is zero.

<a name="head.Precondition"></a>
## Preconditions
|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm device is accessible via SSH | The device under test must be accessible via SSH with valid credentials configured. | SSH connection to the device should be established successfully. |
| 2 | Configure device reboot preference | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Establish SSH connection to device | Obtain SSH connection parameters for the device under test to enable remote command execution. | SSH parameters should be retrieved successfully and the connection should be established. |
| 2 | Query zombie process count | SSH into the device and execute the command to count the number of zombie processes present in the current process list: <br>`top -b1 -n1 \| grep Z \| wc -l` | The command should return the count of zombie processes without an exception. |
| 3 | Validate no zombie processes are running | Parse the zombie process count from the command output and verify that it equals zero. | The zombie process count should be 0, confirming that there are no zombie processes running on the device. If any zombie processes are found, the test should report failure. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 4 mins

**Priority** : High

**Release Version** : M107<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
