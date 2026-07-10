## TestCase ID
RDKV_MANUAL_SYSTEM_02
## TestCase Name
RDKV_CERT_MANUAL_SYSTEM_SSH_ACCESS

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate SSH access to the DUT by establishing a remote login session from the PC/laptop using the DUT IP address and valid credentials, and to ensure that the device command prompt is displayed successfully after login.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 |  Connect Ethernet cable  | Connect the Ethernet cable to the DUT. | The Ethernet cable should be connected and the network interface should be active on the DUT. |
| 2 |  Ensure DUT and PC on same network  | Ensure that the DUT and the PC/laptop are connected to the same network. | The DUT and PC/laptop should be on the same network and reachable from each other. |
| 3 |  Obtain DUT Ethernet IP address  | Obtain the DUT's Ethernet IP address using at least one of the following methods: serial terminal access to execute the ifconfig command and obtain the eth0 IP address, or RDK UI access to navigate to Settings → Network Configuration → Network Information and retrieve the Ethernet IP address. | The DUT's Ethernet IP address should be identified and noted for use in the SSH session. |
| 4 |  Ensure SSH service running on DUT  | Ensure that the SSH service is enabled and running on the DUT. | The SSH service should be active and accepting connections on the DUT. |
| 5 |  Install SSH client on PC  | Install an SSH client on the PC/laptop (e.g., PuTTY, OpenSSH, Tera Term). | The SSH client should be installed and ready for use on the PC/laptop. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 |  Connect serial port and power on DUT  | Power on the DUT and connect the serial port of the DUT to the PC/laptop using a serial cable. | The DUT should power on and the RDK UI should be displayed on the TV. |
| 2 |  Access device serial console  | Access the device serial console from the PC/laptop using the configured serial terminal utility. | The serial console should be accessible, and the device prompt should be displayed. |
| 3 |  Obtain DUT IP via ifconfig  | Execute the command to validate the Ethernet interface details and obtain the DUT IP address.<br>Command: `ifconfig eth0` | The eth0 interface details should be displayed along with a valid Ethernet IP address. |
| 4 |  Establish SSH session  | Establish an SSH session from the PC/laptop to the DUT using the obtained IP address and valid login credentials.<br>Command: `ssh root@<DUT_IP_Address>` | The SSH session should be established successfully and the device command prompt should be displayed. |
| 5 |  Validate firmware version via SSH  | Execute the command to display the firmware version information via SSH.<br>Command: `cat /version.txt` | The image name/version information should be displayed successfully. |
| 6 |  Exit SSH session  | Exit the SSH session.<br>Command: `exit` | A logout message and "Connection to <DUT_IP> closed." message should be displayed. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
