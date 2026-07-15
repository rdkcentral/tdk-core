## TestCase ID
RDKV_MANUAL_WIFI_11
## TestCase Name
RDKV_CERT_MANUAL_Wifi_Dual_Band_SSID_Connect

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the DUT can successfully connect to both a 2.4 GHz and a 5 GHz Wi-Fi SSID sequentially, with internet access confirmed for both bands. This test exercises the RDK UI Network Configuration settings, the Wi-Fi connection manager (`wpa_supplicant`), and the network interface stack to validate the targeted Wi-Fi connectivity behaviour. The test confirms that the application should launch successfully and video playback should start with proper audio and video output.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Connect HDMI display | Connect the HDMI display to the DUT and select the correct HDMI input source on the display. | The HDMI display should be connected and the correct HDMI input source should be selected on the display. |
| 2 | Connect Ethernet cable | Connect the Ethernet cable to the DUT and ensure a valid Ethernet IP address is available. | The Ethernet cable should be connected and a valid IP address should be assigned to the DUT. |
| 3 | Confirm Wi-Fi with valid IP | Ensure the DUT is already connected to a Wi-Fi network with a valid IP address prior to the test. | The DUT should be connected to a Wi-Fi network with a valid IP address. |
| 4 | Confirm internet access | Confirm that internet access is functional on the DUT prior to the test. | Internet access should be confirmed as functional on the DUT. |
| 5 | Pair Bluetooth remote | Pair and connect the Bluetooth remote to the DUT. | The Bluetooth remote should be paired and connected to the DUT successfully. |
| 6 | Connect serial cable | Connect the required serial cable or USB-to-serial adapter between the DUT and the PC/laptop and ensure the appropriate drivers are installed. | The serial cable or USB-to-serial adapter should be connected and the drivers should be installed and recognized. |
| 7 | Configure serial terminal | Install and configure a serial terminal utility (such as Minicom, TeraTerm, or equivalent) on the PC/laptop. | The serial terminal utility should be installed, properly configured, and ready to connect to the DUT. |
| 8 | Install SSH client | Install an SSH client (such as TeraTerm or PuTTY) on the PC/laptop. | The SSH client should be installed and ready for use on the PC/laptop. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot DUT | Reboot the DUT. | The DUT should reboot successfully and the RDK UI Home screen should be displayed. |
| 2 | Navigate to Settings | Navigate to Settings (gear icon at top right of the RDK UI Home screen) using the remote. | The Settings screen should launch. |
| 3 | Open network configuration | Select "Network Configuration" from the Settings menu. | The Network Configuration screen should load with the Network Interface value displayed as ETHERNET. |
| 4 | Select network interface | Select "Network Interface". | The Network Interface selection screen should launch. |
| 5 | Select WiFi interface | Select "WiFi" from the Network Interface screen. | The Wi-Fi network selection screen should load with the Wi-Fi On/Off toggle in the ON state. All available SSIDs (both 2.4 GHz and 5 GHz) should be listed. The previously connected SSID should be in a ticked state. |
| 6 | Select 2.4 GHz SSID | Select a 2.4 GHz Wi-Fi SSID and press OK. | The password entry screen should launch. |
| 7 | Enter password and connect | Enter the correct password using the on-screen keyboard and press the Connect button. | The DUT should connect to the selected 2.4 GHz SSID. The Wi-Fi network selection screen should reload with the connected SSID in a ticked state. |
| 8 | Navigate back to settings | Press the Back button twice. | The Network Configuration screen should load with the Network Interface value still displayed as ETHERNET. |
| 9 | Open network info | Navigate to "Network Info" and press OK. | The Network Info screen should launch displaying the Ethernet IP address and details. |
| 10 | Verify internet via Ethernet | SSH to the DUT using the Ethernet IP address and execute the ping command.<br>Command: `ping google.com` | The SSH connection should be established via the Ethernet IP address. Ping packets should be transmitted and received successfully. |
| 11 | Disconnect Ethernet cable | Disconnect the Ethernet cable from the DUT. | The Network Info screen should automatically update to display the 2.4 GHz Wi-Fi IP address and SSID details. All fields should be populated with proper values. |
| 12 | Verify Wi-Fi via wlan0 ping | SSH to the DUT using the wlan0 IP address and execute the ping command.<br>Command: `ping google.com` | The SSH connection should be established via the wlan0 IP address. Ping packets should be transmitted and received successfully. |
| 13 | Launch video app on 2.4 GHz | Navigate to the RDK UI Home screen and install any video app (like YouTube), launch it and play any video. | The application should be installed and launch successfully and video playback should start with proper audio and video output. |
| 14 | Navigate to Settings | Navigate to Settings using the remote. | The Settings screen should launch. |
| 15 | Open network configuration | Select "Network Configuration" from the Settings menu. | The Network Configuration screen should load with the Network Interface value displayed as WiFi. |
| 16 | Select network interface | Select "Network Interface". | The Network Interface selection screen should launch. |
| 17 | Select WiFi interface | Select "WiFi" from the Network Interface screen. | The Wi-Fi network selection screen should load with the Wi-Fi On/Off toggle in the ON state. All available SSIDs (both 2.4 GHz and 5 GHz) should be listed. |
| 18 | Select 5 GHz SSID | Select a 5 GHz Wi-Fi SSID and press OK. | The password entry screen should launch. |
| 19 | Enter password and connect | Enter the correct password using the on-screen keyboard and press the Connect button. | The DUT should connect to the selected 5 GHz SSID. The Wi-Fi network selection screen should reload with the connected SSID in a ticked state. |
| 20 | Navigate back to settings | Press the Back button twice. | The Network Configuration screen should load with the Network Interface value displayed as WiFi. |
| 21 | Open network info | Navigate to "Network Info" and press OK. | The Network Info screen should launch displaying the 5 GHz Wi-Fi SSID and details. |
| 22 | Verify 5 GHz via wlan0 ping | SSH to the DUT using the wlan0 IP address and execute the ping command.<br>Command: `ping google.com` | The SSH connection should be established via the wlan0 IP address. Ping packets should be transmitted and received successfully. |
| 23 | Launch video app on 5 GHz | Navigate to the RDK UI Home screen, launch any video app (such as YouTube) and play any video. | The application should launch successfully and video playback should start with proper audio and video output. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
