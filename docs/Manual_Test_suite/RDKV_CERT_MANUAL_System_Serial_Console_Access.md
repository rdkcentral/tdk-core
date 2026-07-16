## TestCase ID
RDKV_MANUAL_SYSTEM_01
## TestCase Name
RDKV_CERT_MANUAL_System_Serial_Console_Access

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate serial terminal access to the DUT and ensure that the required commands can be executed successfully from the serial console with the expected responses. This test exercises shell commands executed over a serial console or SSH session (such as `systemctl`, `cat`, `ifconfig`, and `journalctl`) to validate the targeted system-level functionality. The test confirms that the eth0 interface details should be displayed along with a valid Ethernet IP address.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 |  Power on DUT and connect HDMI  | Power on the DUT and connect it to a TV via HDMI. | The DUT should be powered on and the RDK UI should be visible on the TV screen.|
| 2 |  Connect serial cable  | Connect the required serial cable or USB-to-serial adapter between the DUT and the PC/laptop. | The serial cable or USB-to-serial adapter should be physically connected between the DUT and PC/laptop.|
| 3 |  Install serial/usb drivers  | Install the appropriate serial/USB-to-serial drivers on the PC/laptop. | The serial/USB drivers should be installed and the COM port should be recognized on the PC/laptop.|
| 4 |  Connect Ethernet cable  | Connect the Ethernet cable to the DUT as per the required test setup. | The Ethernet cable should be connected and the network interface should be active on the DUT.|
| 5 |  Install serial terminal utility  | Install a serial terminal utility such as Minicom, Tera Term, or an equivalent utility on the PC/laptop. | The serial terminal utility should be installed and ready to use on the PC/laptop.|
| 6 |  Configure serial terminal  | Configure the serial terminal as per the device specification, including COM port, baud rate, data bits, parity, stop bits, and flow control. | The serial terminal should be configured correctly and ready to establish a connection to the DUT.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 |  Connect serial port and power on DUT  | Power on the DUT and connect the serial port of the DUT to the PC/laptop using a serial cable. | The DUT should power on and the RDK UI should be displayed on the TV.|
| 2 |  Access device serial console  | Access the device serial console from the PC/laptop using the configured serial terminal utility. | The serial console should be accessible, and the device prompt should be displayed.|
| 3 |  Validate firmware version  | Execute the command to display the firmware version information.<br>Command: `cat /version.txt` | The image name/version information should be displayed successfully.|
| 4 |  Validate Ethernet interface  | Execute the command to validate the Ethernet interface details and IP address.<br>Command: `ifconfig eth0` | The eth0 interface details should be displayed along with a valid Ethernet IP address.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
