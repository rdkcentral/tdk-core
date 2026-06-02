## TestCase ID
RDKV_STABILITY_30
## TestCase Name
RDKV_CERT_RVS_SSH
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate device stability by repeatedly establishing SSH connections to the device and running system commands for ssh_max_count iterations, verifying the device remains accessible and CPU/memory usage stays within expected limits.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|DeviceInfo plugin must be activated for resource usage validation.|
|3|SSH access must be enabled on the device; SSH credentials (host, port, username, password) must be retrievable via `rdkservice_getSSHParams`.|
|4|ssh_max_count must be configured in StabilityTestVariables (default: 30 iterations).|
|5|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using `check_device_state`. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of DeviceInfo plugin. Activate DeviceInfo if not already active. | DeviceInfo plugin should be activated. |
| 3 | Get SSH credentials | Retrieve SSH connection parameters (host, port, username, password) for the device via `rdkservice_getSSHParams`. | SSH credentials should be retrieved successfully. |
| 4 | SSH connection loop (repeat for ssh_max_count iterations) | For each iteration: <br>Establish SSH connection to the device using retrieved credentials. <br>Execute `uptime` command on the device via `rdkservice_getRequiredLog(ssh, 'uptime')`. <br>Verify the command output contains "users" to confirm successful execution. <br>Close the SSH connection. <br>Validate CPU load and memory usage via `rdkservice_validateResourceUsage`. | SSH connection should be established and `uptime` command should return output containing "users" in each iteration. CPU load and memory usage should remain within expected limits. |
| 5 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all iteration data. |
| 6 | Revert plugins | Restore plugins to their original state using `rdkservice_setPluginStatus`. | Plugins should be reverted to their pre-test states. |
| 7 | Check device state post-condition | Verify the device is still in a stable state after completing the test using `check_device_state`. | Device should remain stable after the SSH stress test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, RPI-HYB, Video_Accelerator

**Estimated duration** : 240

**Priority** : High

**Release Version** : M88<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
