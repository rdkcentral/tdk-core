## TestCase ID
TC_SYSTEM_MANUAL_01
## TestCase Name
RDKV_SYSTEM_SSH_SERVICE_GT

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the SSH Dropbear service is active and running on the DUT and that the device build version is correctly identified as an RDK build.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify Ethernet connectivity | Verify that the DUT has a valid IPv4 address assigned to the Ethernet interface.<br>Command: `ip -4 addr show eth0 \| awk '/inet / {split($2,a,"/"); print a[1]}'` | The DUT should have a valid IPv4 address assigned to the eth0 interface before test execution begins. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify SSH Dropbear service | Execute the commands to verify the SSH Dropbear service active state and sub-state on the DUT.<br>Command: `systemctl show -p ActiveState --value dropbear`<br>Command: `systemctl show -p SubState --value dropbear` | The Dropbear SSH service should be active and in running state on the DUT. |
| 2 | Validate device build version | Execute the command to retrieve and validate the build version of the device.<br>Command: `grep -i "imagename" /version.txt \| cut -d: -f2- \| xargs` | The build version should be retrieved successfully and the image name should contain the RDK build identifier. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
