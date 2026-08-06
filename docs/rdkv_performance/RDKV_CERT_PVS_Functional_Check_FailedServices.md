## TestCase ID
RDKV_PERFORMANCE_1
## TestCase Name
RDKV_CERT_PVS_Functional_Check_FailedServices

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that no systemd services have failed on the device by running the systemctl failed services check and printing the list of any failed services found.

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
| 2 | Query all failed systemd services | SSH into the device and execute the systemctl failed services command to retrieve the list of all failed services: <br>`systemctl --failed` | The command output should be returned successfully without an exception. |
| 3 | Validate the failed services list | Parse the command output to count the number of failed services and print the complete list of any failed services found on the device. | The number of failed services and the list of service names should be printed. Ideally, no services should be in a failed state on the device. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 10 mins

**Priority** : High

**Release Version** : M111<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
