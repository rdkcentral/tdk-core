## TestCase ID
RDKV_MANUAL_GT_SYSTEM_02
## TestCase Name
RDKV_CERT_MANUAL_GT_System_WPEFramework_Process_Status

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that all required WPEFramework processes — `WPEProcess`, `WPEFramework`, `WPENetworkProcess`, and `WPEWebProcess` — are actively running on the DUT as part of the RDK middleware stack. This test confirms that the core WPEFramework process group is healthy and operational, which is a critical prerequisite for RDK service functionality and application execution.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify test script files on DUT | Copy the test script (`System_Automated.sh`), the configuration file (`device.conf`), and the helper script (`generic_functions.sh`) to the working directory of the DUT and ensure all files are accessible. Configure the `device.conf` file with all the correct test environment values specific to this test case prior to execution. | The files `System_Automated.sh`, `device.conf`, and `generic_functions.sh` must be present and accessible in the DUT's working directory. The `device.conf` file must be populated with all the correct test environment values specific to this test case prior to execution. |
| 2 | Verify Ethernet connectivity | Verify that the DUT has a valid IPv4 address assigned to the Ethernet interface.<br>Command: `ip -4 addr show eth0 \| awk '/inet / {split($2,a,"/"); print a[1]}'` | The DUT should have a valid IPv4 address assigned to the eth0 interface before test execution begins. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify WPEFramework processes | Execute the command to verify the running status of all WPEFramework processes on the DUT.<br>Command: `pgrep -l '^WPE'` | All WPEFramework processes should be found and running on the DUT. The following processes should be listed:<br>- WPEProcess<br>- WPEFramework<br>- WPENetworkProcess<br>- WPEWebProcess |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
