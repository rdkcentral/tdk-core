## TestCase ID
RDKV_MANUAL_WIFI_16
## TestCase Name
RDKV_CERT_MANUAL_Wifi_UI_Disconnect_Reconnect_Reboot

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that after manually disconnecting from a Wi-Fi SSID via the RDK UI, the DUT automatically reconnects to that SSID upon reboot. This test confirms that the DUT reconnects to the prior SSID after reboot and content playback is functional, ensuring Wi-Fi auto-reconnect behavior after manual disconnect meets certification requirements.
<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 |  Connect HDMI display  | Connect the HDMI display to the DUT and select the correct HDMI input source on the display. | The HDMI display should be connected and the correct HDMI input source should be selected on the display.|
| 2 |  Disconnect Ethernet cable  | Disconnect the Ethernet cable from the DUT. | The Ethernet cable should be disconnected from the DUT.|
| 3 |  Pair bluetooth remote  | Pair and connect the Bluetooth remote to the DUT. | The Bluetooth remote should be paired and connected to the DUT successfully.|
| 4 |  Connect serial cable  | Connect the required serial cable or USB-to-serial adapter between the DUT and the PC/laptop and ensure the appropriate drivers are installed. | The serial cable or USB-to-serial adapter should be connected and the drivers should be installed and recognized.|
| 5 |  Configure serial terminal  | Install and configure a serial terminal utility (such as Minicom, TeraTerm, or equivalent) on the PC/laptop. | The serial terminal utility should be installed, properly configured, and ready to connect to the DUT.|
| 6 |  Install SSH client  | Install an SSH client (such as TeraTerm or PuTTY) on the PC/laptop. | The SSH client should be installed and ready for use on the PC/laptop.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 |  Connect to SSID a  | Navigate to Settings > Network Configuration > Network Interface > WiFi and connect to an SSID (referred to as SSID 'A'). | The password entry screen should launch. Upon entering the correct credentials, SSID 'A' should connect and a tick mark should appear next to it.|
| 2 |  Disconnect Ethernet and verify SSID a  | Disconnect the Ethernet cable and navigate to Settings > Network Configuration > Network Info. | The SSID details of SSID 'A' should be listed in the Network Info screen.|
| 3 |  Test internet access on SSID a  | Navigate to "Test Internet Access" and press OK. | The connection status should be displayed as "Connected".|
| 4 |  Validate content playback on SSID a  | Navigate to the RDK UI Home screen, open any application that requires internet, and play any content. | The application should open and content playback should start with proper audio and video output.|
| 5 |  Select connected SSID a for disconnect  | Navigate to Settings > Network Configuration > Network Interface > WiFi and select the already-connected SSID 'A'. | The next screen should open displaying the Disconnect button.|
| 6 |  Disconnect from SSID a  | Press the Disconnect button. | A "Wi-Fi Disconnected" notification should be displayed and the tick mark next to SSID 'A' should be removed.|
| 7 |  Verify disconnected network info  | Navigate to Settings > Network Configuration > Network Info. | The SSID details should not be available. The Connection Status should display as "Disconnected" and all other fields should display as N/A.|
| 8 |  Verify internet access is disconnected  | Navigate to "Test Internet Access" and press OK. | The Internet Access status should display as "Disconnected".|
| 9 |  Verify no internet on Home screen  | Navigate to the RDK UI Home screen and attempt to open any application that requires internet. | The application should not open and should display an error message such as "No Internet Connection. Please check your network and try again."|
| 10 |  Reboot DUT  | Reboot the DUT. | The DUT should reboot successfully and the RDK UI Home screen should be displayed.|
| 11 |  Verify SSID a auto-reconnects after reboot  | Navigate to Settings > Network Configuration > Network Interface > WiFi and verify which SSID is in a ticked state. | SSID 'A', which was manually disconnected prior to reboot, should now be in a ticked/connected state.|
| 12 |  Verify network info after reboot  | Navigate to Settings > Network Configuration > Network Info and verify the details. | The details of SSID 'A' should be populated in the Network Info screen.|
| 13 |  Test internet access after reboot  | Navigate to "Test Internet Access" and press OK. | The connection status should be displayed as "Connected".|
| 14 |  Validate content playback after reboot  | Navigate to the RDK UI Home screen, open any application that requires internet, and play any content. | The application should open successfully and content playback should start with proper audio and video output.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
