## TestCase ID
RDKV_MANUAL_WIFI_12
## TestCase Name
RDKV_CERT_MANUAL_Wifi_Prev_SSID_Reconnect

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the DUT can successfully reconnect to a previously connected Wi-Fi SSID after switching to a different SSID. This test confirms that the DUT reconnects to the prior SSID and content playback resumes successfully, ensuring Wi-Fi SSID re-connection after switching meets certification requirements.
<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Connect HDMI display | Connect the HDMI display to the DUT and select the correct HDMI input source on the display. | The HDMI display should be connected and the correct HDMI input source should be selected on the display.|
| 2 | Connect Ethernet cable | Connect the Ethernet cable to the DUT and ensure a valid Ethernet IP address is available. | The Ethernet cable should be connected and a valid IP address should be assigned to the DUT.|
| 3 | Pair Bluetooth remote | Pair and connect the Bluetooth remote to the DUT. | The Bluetooth remote should be paired and connected to the DUT successfully.|
| 4 | Connect serial cable | Connect the required serial cable or USB-to-serial adapter between the DUT and the PC/laptop and ensure the appropriate drivers are installed. | The serial cable or USB-to-serial adapter should be connected and the drivers should be installed and recognized.|
| 5 | Configure serial terminal | Install and configure a serial terminal utility (such as Minicom, TeraTerm, or equivalent) on the PC/laptop. | The serial terminal utility should be installed, properly configured, and ready to connect to the DUT.|
| 6 | Install SSH client | Install an SSH client (such as TeraTerm or PuTTY) on the PC/laptop. | The SSH client should be installed and ready for use on the PC/laptop.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Connect to first SSID A | Navigate to Settings > Network Configuration > Network Interface > WiFi and connect to an SSID (referred to as SSID 'A'). | The password entry screen should launch. Upon entering the correct credentials, SSID 'A' should connect and a tick mark should appear next to it.|
| 2 | Disconnect Ethernet and verify SSID A | Disconnect the Ethernet cable and navigate to Settings > Network Configuration > Network Info. | Upon disconnecting Ethernet, the SSID details of SSID 'A' should be listed in the Network Info screen.|
| 3 | Verify internet access | Navigate to "Test Internet Access" and press OK. | The connection status should be displayed as "Connected".|
| 4 | Launch app and play content | Navigate to the RDK UI Home screen, open any application that requires internet, and play any content. | The application should open successfully and content playback should start with proper audio and video output.|
| 5 | Connect to second SSID B | Navigate to Settings > Network Configuration > Network Interface > WiFi and connect to a different SSID (referred to as SSID 'B'). | The password entry screen should launch. Upon entering the correct credentials, SSID 'B' should connect and a tick mark should appear next to it.|
| 6 | Verify SSID B network info | Navigate to Settings > Network Configuration > Network Info and verify the details. | The SSID details of SSID 'B' should be listed in the Network Info screen.|
| 7 | Verify internet access | Navigate to "Test Internet Access" and press OK. | The connection status should be displayed as "Connected".|
| 8 | Launch app and play content | Navigate to the RDK UI Home screen, open any application that requires internet, and play any content. | The application should open successfully and content playback should start with proper audio and video output.|
| 9 | Reconnect to first SSID A | Navigate to Settings > Network Configuration > Network Interface > WiFi and reconnect to SSID 'A'. | The password entry screen should launch. Upon entering the correct credentials, SSID 'A' should reconnect and a tick mark should appear next to it.|
| 10 | Verify SSID A network info | Navigate to Settings > Network Configuration > Network Info and verify the details. | The SSID details of SSID 'A' should be listed in the Network Info screen.|
| 11 | Verify internet access | Navigate to "Test Internet Access" and press OK. | The connection status should be displayed as "Connected".|
| 12 | Launch app and play content | Navigate to the RDK UI Home screen, open any application that requires internet, and play any content. | The application should open successfully and content playback should start with proper audio and video output.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
