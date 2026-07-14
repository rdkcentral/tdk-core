## TestCase ID
RDKV_GT_SYSTEM_03
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
To validate that the log rollover mechanism on the DUT is functioning correctly by verifying that the `/opt/logs/PreviousLogs` directory exists and contains non-empty `.log` files following a device reboot, as tested by the `System_Automated.sh` script. The test navigates to `/opt/logs/` and uses `find /opt/logs/PreviousLogs -maxdepth 1 -name '*.log' -type f -size +0c` to confirm that valid log files were rolled over from the current session to the PreviousLogs directory during boot. This test confirms the RDK log management subsystem correctly executes the log rotation process during device reboot cycles.

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
