## TestCase ID
RDKV_MANUAL_WIFI_17
## TestCase Name
RDKV_CERT_MANUAL_WIFI_FALLBACK_ON_WRONG_CRED

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the DUT automatically falls back to the previously connected SSID when a connection attempt to a new SSID fails due to incorrect credentials.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 |  Connect HDMI display  | Connect the HDMI display to the DUT and select the correct HDMI input source on the display. | The HDMI display should be connected and the correct HDMI input source should be selected on the display. |
| 2 |  Disconnect Ethernet cable  | Disconnect the Ethernet cable from the DUT. | The Ethernet cable should be disconnected from the DUT. |
| 3 |  Pair bluetooth remote  | Pair and connect the Bluetooth remote to the DUT. | The Bluetooth remote should be paired and connected to the DUT successfully. |
| 4 |  Connect serial cable  | Connect the required serial cable or USB-to-serial adapter between the DUT and the PC/laptop and ensure the appropriate drivers are installed. | The serial cable or USB-to-serial adapter should be connected and the drivers should be installed and recognized. |
| 5 |  Configure serial terminal  | Install and configure a serial terminal utility (such as Minicom, TeraTerm, or equivalent) on the PC/laptop. | The serial terminal utility should be installed, properly configured, and ready to connect to the DUT. |
| 6 |  Install SSH client  | Install an SSH client (such as TeraTerm or PuTTY) on the PC/laptop. | The SSH client should be installed and ready for use on the PC/laptop. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 |  Connect to SSID a  | Navigate to Settings > Network Configuration > Network Interface > WiFi and connect to an SSID (referred to as SSID 'A'). | The password entry screen should launch. Upon entering the correct credentials, SSID 'A' should connect and a tick mark should appear next to it. |
| 2 |  Disconnect Ethernet and verify SSID a  | Disconnect the Ethernet cable and navigate to Settings > Network Configuration > Network Info. | The SSID details of SSID 'A' should be listed in the Network Info screen. |
| 3 |  Test internet access on SSID a  | Navigate to "Test Internet Access" and press OK. | The connection status should be displayed as "Connected". |
| 4 |  Validate content playback on SSID a  | Navigate to the RDK UI Home screen, open any application that requires internet, and play any content. | The application should open and content playback should start with proper audio and video output. |
| 5 |  Attempt connection to SSID b with wrong password  | Navigate to Settings > Network Configuration > Network Interface > WiFi and attempt to connect to a different SSID (referred to as SSID 'B') using an incorrect password. | The following should occur: a Wi-Fi State Disconnected error message should be displayed; an Authentication Failure error message should be displayed; the tick mark next to SSID 'A' should be temporarily removed; after a few seconds, the DUT should automatically reconnect to SSID 'A'. |
| 6 |  Verify fallback to SSID a  | Navigate to Settings > Network Configuration > Network Info and verify the details. | The SSID details of SSID 'A' should be listed in the Network Info screen, confirming fallback to the previous connection. |
| 7 |  Test internet access after fallback  | Navigate to "Test Internet Access" and press OK. | The connection status should be displayed as "Connected". |
| 8 |  Validate content playback after fallback  | Navigate to the RDK UI Home screen, open any application that requires internet, and play any content. | The application should open and content playback should start with proper audio and video output. |
| 9 |  Reboot DUT  | Reboot the DUT. | The DUT should reboot successfully and the RDK UI Home screen should be displayed. |
| 10 |  Verify network info after reboot  | Navigate to Settings > Network Configuration > Network Info and verify the details. | The SSID details of SSID 'A' should be listed in the Network Info screen. |
| 11 |  Test internet access after reboot  | Navigate to "Test Internet Access" and press OK. | The connection status should be displayed as "Connected". |
| 12 |  Validate content playback after reboot  | Navigate to the RDK UI Home screen, open any application that requires internet, and play any content. | The application should open successfully and content playback should start with proper audio and video output. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
