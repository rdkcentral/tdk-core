## TestCase ID
RDKV_PERFORMANCE_218
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
To validate that all log files present in the /opt/logs directory on the device under test are within the configured size limit, and to identify any log files whose size exceeds the threshold or their individual logrotate-defined limits.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Configure device reboot preference | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 3 | Configure SIZE_LIMIT in device config | `SIZE_LIMIT` must be set in the device-specific config file to define the maximum acceptable log file size in bytes. | The size limit should be configured correctly. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Establish SSH connection and read size limit | Obtain SSH connection parameters for the device and retrieve the `SIZE_LIMIT` configuration value from the device config file. | SSH parameters and the size limit value should be retrieved successfully. |
| 2 | List all log files in /opt/logs | SSH into the device and retrieve the list of all log files present in the /opt/logs directory along with their sizes. | The list of log files and their sizes should be returned successfully. |
| 3 | Validate each log file size against threshold | For each log file in /opt/logs, compare its size against the configured `SIZE_LIMIT`. Identify and list all files whose size exceeds the generic threshold. | All log files should have a size within the configured `SIZE_LIMIT`. Any files exceeding the limit should be identified and reported. |
| 4 | Cross-validate oversized logs against logrotate config | For any log file found to exceed the generic size limit, retrieve its corresponding logrotate size limit defined in /etc/logrotate.properties and compare the actual size against the logrotate-specific threshold. | Log files that exceed the generic threshold should also be checked against their individual logrotate configuration values. All log file sizes should ultimately be within their respective logrotate-defined limits. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10 mins

**Priority** : High

**Release Version** : M123<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
