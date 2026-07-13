## TestCase ID
RDKV_MANUAL_SYSTEM_02
## TestCase Name
RDKV_CERT_GT_SYSTEM_WPEFRAMEWORK_PROCESS_STATUS

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that all WPEFramework processes are running successfully on the DUT.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify Ethernet connectivity | Verify that the DUT has a valid IPv4 address assigned to the Ethernet interface.<br>Command: `ip -4 addr show eth0 \| awk '/inet / {split($2,a,"/"); print a[1]}'` | The DUT should have a valid IPv4 address assigned to the eth0 interface before test execution begins. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify WPE framework processes | Execute the command to verify the running status of all WPEFramework processes on the DUT.<br>Command: `pgrep -l '^WPE'` | All WPEFramework processes should be found and running on the DUT. The following processes should be listed:<br>- WPEProcess<br>- WPEFramework<br>- WPENetworkProcess<br>- WPEWebProcess |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
