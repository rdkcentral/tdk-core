## TestCase ID
RDKV_MANUAL_WIFI_14
## TestCase Name
RDKV_CERT_MANUAL_Wifi_Hotspot_Persist_After_Reboot

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the DUT automatically reconnects to the last connected mobile hotspot SSID after a reboot. This test exercises the RDK UI Network Configuration settings, the Wi-Fi connection manager (`wpa_supplicant`), and the network interface stack to validate the targeted Wi-Fi connectivity behaviour. The test confirms that the application should open successfully and content playback should start with proper audio and video output.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 |  Connect HDMI display  | Connect the HDMI display to the DUT and select the correct HDMI input source on the display. | The HDMI display should be connected and the correct HDMI input source should be selected on the display. |
| 2 |  Connect Ethernet cable  | Connect the Ethernet cable to the DUT and ensure a valid Ethernet IP address is available. | The Ethernet cable should be connected and a valid IP address should be assigned to the DUT. |
| 3 |  Ensure hotspot remains active after reboot  | Ensure the last connected mobile hotspot remains active and available after the DUT reboot. | The mobile hotspot should remain active and available for reconnection after the DUT reboots. |
| 4 |  Pair bluetooth remote  | Pair and connect the Bluetooth remote to the DUT. | The Bluetooth remote should be paired and connected to the DUT successfully. |
| 5 |  Connect serial cable  | Connect the required serial cable or USB-to-serial adapter between the DUT and the PC/laptop and ensure the appropriate drivers are installed. | The serial cable or USB-to-serial adapter should be connected and the drivers should be installed and recognized. |
| 6 |  Configure serial terminal  | Install and configure a serial terminal utility (such as Minicom, TeraTerm, or equivalent) on the PC/laptop. | The serial terminal utility should be installed, properly configured, and ready to connect to the DUT. |
| 7 |  Install SSH client  | Install an SSH client (such as TeraTerm or PuTTY) on the PC/laptop. | The SSH client should be installed and ready for use on the PC/laptop. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 |  Connect to hotspot a  | Navigate to Settings > Network Configuration > Network Interface > WiFi and connect to a mobile hotspot SSID (referred to as Hotspot 'A'). | The password entry screen should launch. Upon entering the correct credentials, Hotspot 'A' should connect and a tick mark should appear next to it. |
| 2 |  Disconnect Ethernet and verify hotspot a  | Disconnect the Ethernet cable and navigate to Settings > Network Configuration > Network Info. | Upon disconnecting Ethernet, the SSID details of Hotspot 'A' should be listed in the Network Info screen. |
| 3 |  Test internet access on hotspot a  | Navigate to "Test Internet Access" and press OK. | The connection status should be displayed as "Connected". |
| 4 |  Validate content playback on hotspot a  | Navigate to the RDK UI Home screen, open any application that requires internet, and play any content. | The application should open successfully and content playback should start with proper audio and video output. |
| 5 |  Reboot DUT with hotspot active  | Reboot the DUT. Ensure that Hotspot 'A' remains active after the reboot. | The DUT should reboot successfully. |
| 6 |  Verify hotspot a reconnection after reboot  | Navigate to Settings > Network Configuration > Network Info and verify the details. | The SSID details of Hotspot 'A' should be listed in the Network Info screen, confirming automatic reconnection after reboot. |
| 7 |  Test internet access after reboot  | Navigate to "Test Internet Access" and press OK. | The connection status should be displayed as "Connected". |
| 8 |  Validate content playback after reboot  | Navigate to the RDK UI Home screen, open any application that requires internet, and play any content. | The application should open successfully and content playback should start with proper audio and video output. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
