## TestCase ID
RDKV_MANUAL_WIFI_13
## TestCase Name
RDKV_CERT_MANUAL_Wifi_Mobile_Hotspot_Connect

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the DUT can successfully connect to and use a mobile hotspot as a Wi-Fi network. This test confirms that internet connectivity is established via the hotspot and content playback resumes successfully, ensuring mobile hotspot Wi-Fi connectivity meets certification requirements.
<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 |  Connect HDMI display  | Connect the HDMI display to the DUT and select the correct HDMI input source on the display. | The HDMI display should be connected and the correct HDMI input source should be selected on the display.|
| 2 |  Connect Ethernet cable  | Connect the Ethernet cable to the DUT and ensure a valid Ethernet IP address is available. | The Ethernet cable should be connected and a valid IP address should be assigned to the DUT.|
| 3 |  Ensure two mobile hotspots available  | Ensure at least two mobile hotspot SSIDs are available and accessible for connection. | At least two mobile hotspot SSIDs should be available and visible in the Wi-Fi network list.|
| 4 |  Pair bluetooth remote  | Pair and connect the Bluetooth remote to the DUT. | The Bluetooth remote should be paired and connected to the DUT successfully.|
| 5 |  Connect serial cable  | Connect the required serial cable or USB-to-serial adapter between the DUT and the PC/laptop and ensure the appropriate drivers are installed. | The serial cable or USB-to-serial adapter should be connected and the drivers should be installed and recognized.|
| 6 |  Configure serial terminal  | Install and configure a serial terminal utility (such as Minicom, TeraTerm, or equivalent) on the PC/laptop. | The serial terminal utility should be installed, properly configured, and ready to connect to the DUT.|
| 7 |  Install SSH client  | Install an SSH client (such as TeraTerm or PuTTY) on the PC/laptop. | The SSH client should be installed and ready for use on the PC/laptop.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 |  Connect to hotspot a  | Navigate to Settings > Network Configuration > Network Interface > WiFi and connect to a mobile hotspot SSID (referred to as Hotspot 'A'). | The password entry screen should launch. Upon entering the correct credentials, Hotspot 'A' should connect and a tick mark should appear next to it.|
| 2 |  Disconnect Ethernet and verify hotspot a  | Disconnect the Ethernet cable and navigate to Settings > Network Configuration > Network Info. | Upon disconnecting Ethernet, the SSID details of Hotspot 'A' should be listed in the Network Info screen.|
| 3 |  Test internet access on hotspot a  | Navigate to "Test Internet Access" and press OK. | The connection status should be displayed as "Connected".|
| 4 |  Validate content playback on hotspot a  | Navigate to the RDK UI Home screen, open any application that requires internet, and play any content. | The application should open successfully and content playback should start with proper audio and video output.|
| 5 |  Connect to hotspot b  | Navigate to Settings > Network Configuration > Network Interface > WiFi and connect to a different mobile hotspot SSID (referred to as Hotspot 'B'). | The password entry screen should launch. Upon entering the correct credentials, Hotspot 'B' should connect and a tick mark should appear next to it.|
| 6 |  Verify network info on hotspot b  | Navigate to Settings > Network Configuration > Network Info and verify the details. | The SSID details of Hotspot 'B' should be listed in the Network Info screen.|
| 7 |  Test internet access on hotspot b  | Navigate to "Test Internet Access" and press OK. | The connection status should be displayed as "Connected".|
| 8 |  Validate content playback on hotspot b  | Navigate to the RDK UI Home screen, open any application that requires internet, and play any content. | The application should open successfully and content playback should start with proper audio and video output.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
