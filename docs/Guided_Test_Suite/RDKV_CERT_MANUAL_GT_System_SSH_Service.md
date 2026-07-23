## TestCase ID
RDKV_MANUAL_GT_SYSTEM_01
## TestCase Name
RDKV_CERT_MANUAL_GT_System_SSH_Service

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Preconditions](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the SSH Dropbear service is active and running, and that the device firmware is correctly identified as a valid RDK build on the DUT. This test confirms that both the SSH daemon availability and the firmware identity are in their expected operational states, which are prerequisites for remote access and certification validation.

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
| 1 | Verify SSH Dropbear service | Execute the commands to verify the SSH Dropbear service active state and sub-state on the DUT.<br>Command: `systemctl show -p ActiveState --value dropbear`<br>Command: `systemctl show -p SubState --value dropbear` | The Dropbear SSH service should be active and in running state on the DUT. |
| 2 | Validate device build version | Execute the command to retrieve and validate the build version of the device.<br>Command: `grep -i "imagename" /version.txt \| cut -d: -f2- \| xargs` | The build version should be retrieved successfully and the image name should contain the RDK build identifier. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
