## TestCase ID
RDKV_MANUAL_WIFI_10
## TestCase Name
RDKV_CERT_MANUAL_WIFI_IP_ON_ETH_DISCONNECT_POST_REBOOT

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the DUT acquires and displays the Wi-Fi IP address after a reboot when the Ethernet cable is subsequently disconnected.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 |  Connect HDMI display  | Connect the HDMI display to the DUT and select the correct HDMI input source on the display. | The HDMI display should be connected and the correct HDMI input source should be selected on the display. |
| 2 |  Connect Ethernet cable  | Connect the Ethernet cable to the DUT and ensure a valid Ethernet IP address is available. | The Ethernet cable should be connected and a valid IP address should be assigned to the DUT. |
| 3 |  Ensure DUT connected to Wi-Fi  | Ensure that the DUT is already connected to a Wi-Fi network prior to the test. | The DUT should have an active Wi-Fi connection with a valid IP address assigned. |
| 4 |  Confirm internet access  | Confirm that internet access is functional on the DUT prior to the test. | Internet access should be confirmed as working on the DUT. |
| 5 |  Pair bluetooth remote  | Pair and connect the Bluetooth remote to the DUT. | The Bluetooth remote should be paired and connected to the DUT successfully. |
| 6 |  Connect serial cable  | Connect the required serial cable or USB-to-serial adapter between the DUT and the PC/laptop and ensure the appropriate drivers are installed. | The serial cable or USB-to-serial adapter should be connected and the drivers should be installed and recognized. |
| 7 |  Configure serial terminal  | Install and configure a serial terminal utility (such as Minicom, TeraTerm, or equivalent) on the PC/laptop. | The serial terminal utility should be installed, properly configured, and ready to connect to the DUT. |
| 8 |  Install SSH client  | Install an SSH client (such as TeraTerm or PuTTY) on the PC/laptop. | The SSH client should be installed and ready for use on the PC/laptop. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 |  Reboot DUT  | Reboot the DUT. | The DUT should reboot successfully and the RDK UI Home screen should be displayed. |
| 2 |  Verify Ethernet network info  | Navigate to Settings > Network Configuration > Network Info and verify the details. | The Ethernet IP address and all interface details should be populated correctly. |
| 3 |  Disconnect Ethernet and verify Wi-Fi  | Disconnect the Ethernet cable from the DUT and navigate back to Settings > Network Configuration > Network Info. | The Wi-Fi SSID, IP address, and all details of the connected Wi-Fi network should be populated correctly. |
| 4 |  SSH via Wi-Fi IP  | SSH to the DUT using the wlan0 IP address. | The SSH connection should be established successfully using the wlan0 IP address. |
| 5 |  Verify internet via ping  | In the SSH console, execute the ping command.<br>Command: `ping google.com` | Ping packets should be transmitted and received successfully, confirming internet connectivity via Wi-Fi. |
| 6 |  Validate content playback  | On the RDK UI Home screen, open any application that requires internet and play any content. | The application should open successfully and content playback should start with proper audio and video output. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
