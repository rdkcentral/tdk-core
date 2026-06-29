## TestCase ID
RDKV_PERFORMANCE_7
## TestCase Name
RDKV_CERT_PVS_Functional_ResourceUsage_TopCommand

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that no individual process on the device exceeds 90% CPU utilization or 90% memory utilization, by executing the top command with CPU and memory sorting and verifying the process resource consumption.

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
| 2 | Check for processes with CPU usage above 90% | SSH into the device and execute the top command sorted by CPU usage. Filter output to list only processes consuming more than 90% CPU: <br>`top -b -n 1 -o +%CPU -w 512 \| awk '/PID USER/,0' \| awk '{print $9,$12}' \| awk '{if($1>90)print $1,$2}'` | The command output should be returned successfully. Ideally, no processes should have CPU usage greater than 90%. |
| 3 | Validate no process exceeds 90% CPU | Parse the command output and verify that no process appears in the filtered list. If any process has CPU usage above 90%, print the process details and report failure. | No individual process should have a CPU usage percentage greater than 90%. |
| 4 | Check for processes with memory usage above 90% | SSH into the device and execute the top command sorted by memory usage. Filter output to list only processes consuming more than 90% memory: <br>`top -b -n 1 -o +%MEM -w 512 \| awk '/PID USER/,0' \| awk '{print $10,$12}' \| awk '{if($1>90)print $1,$2}'` | The command output should be returned successfully. Ideally, no processes should have memory usage greater than 90%. |
| 5 | Validate no process exceeds 90% memory | Parse the command output and verify that no process appears in the filtered list. If any process has memory usage above 90%, print the process details and report failure. | No individual process should have a memory usage percentage greater than 90%. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 5 mins

**Priority** : High

**Release Version** : M84<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
