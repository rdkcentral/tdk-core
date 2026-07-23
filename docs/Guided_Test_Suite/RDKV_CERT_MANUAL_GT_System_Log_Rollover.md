## TestCase ID
RDKV_MANUAL_GT_SYSTEM_03
## TestCase Name
RDKV_CERT_MANUAL_GT_System_Log_Rollover

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Preconditions](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the log rollover mechanism on the DUT functions correctly by confirming that previous session log files are present in the designated rollover directory following a device reboot. This test ensures the RDK log management subsystem correctly rotates log files during device boot cycles, which is essential for post-failure diagnostics and system auditability.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify test script files on DUT | Copy the test script (`System_Automated.sh`), the configuration file (`device.conf`), and the helper script (`generic_functions.sh`) to the working directory of the DUT and ensure all files are accessible. Configure the `device.conf` file with all the correct test environment values specific to this test case prior to execution. | The files `System_Automated.sh`, `device.conf`, and `generic_functions.sh` must be present and accessible in the DUT's working directory. The `device.conf` file must be populated with all the correct test environment values specific to this test case prior to execution. |
| 2 | Reboot DUT before test | Reboot the DUT prior to test execution to trigger the log rollover mechanism. | The DUT should complete the reboot and be accessible before test execution begins. |

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
