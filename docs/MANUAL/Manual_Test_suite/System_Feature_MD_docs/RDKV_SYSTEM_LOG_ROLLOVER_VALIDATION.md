## TestCase ID
RDKV_MANUAL_SYSTEM_04
## TestCase Name
RDKV_CERT_MANUAL_SYSTEM_LOG_ROLLOVER_VALIDATION

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the log rollover mechanism is functioning as expected on the DUT, ensuring that logs are preserved in the PreviousLogs directory after a reboot.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 |  Ensure console access to DUT  | Ensure that either SSH or serial console access to the DUT is available to execute commands. | SSH or serial console access should be available and functional on the DUT. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 |  Establish SSH session  | Establish an SSH session from the PC/laptop to the DUT using the DUT IP address and valid login credentials.<br>Command: `ssh root@<DUT_IP_Address>` | The SSH session should be established successfully and the device command prompt should be displayed. |
| 2 |  Validate log files in /opt/logs  | Validate that log files are available under the /opt/logs directory.<br>Command: `ls -l /opt/logs` | The /opt/logs directory should be accessible, and the required log files (e.g., ctrlm_log.txt, dcmscript.log, wpeframework.log, dropbear.log) along with PreviousLogs and PreviousLogs_Backup subfolders should be present. |
| 3 |  Validate log file readability  | Execute the command to validate the contents and readability of a log file.<br>Command: `tail -n 50 /opt/logs/wpeframework.log` | The selected log file should be accessible, and recent device log entries should be displayed successfully without any read or permission errors. |
| 4 |  Reboot DUT  | Reboot the DUT using the supported reboot method and wait until the device completes the boot-up process.<br>Command: `reboot` | The DUT should reboot successfully and become reachable over the network. |
| 5 |  Validate previouslogs after reboot  | Access the DUT through SSH console and validate that previous log files are available in /opt/logs/PreviousLogs.<br>Command: `cat /opt/logs/PreviousLogs/wpeframework.log` | The PreviousLogs folder should contain log files, and the log entries captured before the reboot should be present in the respective log file. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
