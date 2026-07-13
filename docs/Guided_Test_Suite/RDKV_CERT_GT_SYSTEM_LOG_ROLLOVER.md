## TestCase ID
RDKV_MANUAL_SYSTEM_03
## TestCase Name
RDKV_CERT_GT_SYSTEM_LOG_ROLLOVER

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the log rollover mechanism is functioning correctly on the DUT by verifying that the PreviousLogs directory exists and contains non-empty log files.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot DUT before test | Reboot the DUT prior to test execution to trigger the log rollover mechanism. | The DUT should complete the reboot and be accessible before test execution begins. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check PreviousLogs directory | Navigate to the /opt/logs/ directory and verify that the PreviousLogs subdirectory exists.<br>Command: `cd /opt/logs/` | The /opt/logs/PreviousLogs directory should exist on the DUT. |
| 2 | Verify log files in PreviousLogs | Verify that non-empty `.log` files are present in the PreviousLogs directory.<br>Command: `find /opt/logs/PreviousLogs -maxdepth 1 -name "*.log" -type f -size +0c` | The PreviousLogs directory should contain at least one non-empty `.log` file. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
