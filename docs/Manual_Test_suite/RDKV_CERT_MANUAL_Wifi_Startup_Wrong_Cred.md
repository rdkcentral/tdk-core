## TestCase ID
RDKV_MANUAL_WIFI_02
## TestCase Name
RDKV_CERT_MANUAL_Wifi_Startup_Wrong_Cred

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that an appropriate connection failure error message is displayed when incorrect credentials are entered during Wi-Fi SSID connection from the startup network selection screen. This test exercises the RDK UI Network Configuration settings, the Wi-Fi connection manager (`wpa_supplicant`), and the network interface stack to validate the targeted Wi-Fi connectivity behaviour. The test confirms that the Wi-Fi network selection screen should be displayed with a clear CONNECTION_FAILED error message explicitly indicating that the failure was due to incorrect credentials.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 |  Connect HDMI display  | Connect the HDMI display to the DUT and select the correct HDMI input source on the display. | The HDMI display should be connected and the correct HDMI input source should be selected on the display.|
| 2 |  Flash DUT or factory reset  | Flash the DUT freshly prior to the test. If Wi-Fi is being tested after other tests have already been conducted, perform a factory reset via Settings > Other Settings > Advanced Settings > Device to restore the startup screens on the next boot. | The DUT should be freshly flashed or factory reset, and the startup screens should be restored on the next boot.|
| 3 |  Connect Ethernet cable  | Connect the Ethernet cable to the DUT and ensure a valid Ethernet IP address is available. | The Ethernet cable should be connected and a valid IP address should be assigned to the DUT.|
| 4 |  Pair bluetooth remote  | Pair and connect the Bluetooth remote to the DUT. Refer to the Bluetooth Remote test module for pairing instructions. | The Bluetooth remote should be paired and connected to the DUT successfully.|
| 5 |  Complete language selection  | Complete language selection from the startup screen and navigate to the Network Configuration screen. | The language selection should be completed and the Network Configuration screen should be displayed.|
| 6 |  Connect serial cable  | Connect the required serial cable or USB-to-serial adapter between the DUT and the PC/laptop and ensure the appropriate drivers are installed. | The serial cable or USB-to-serial adapter should be connected and the drivers should be installed and recognized.|
| 7 |  Configure serial terminal  | Install and configure a serial terminal utility (such as Minicom, TeraTerm, or equivalent) on the PC/laptop. | The serial terminal utility should be installed, properly configured, and ready to connect to the DUT.|
| 8 |  Install SSH client  | Install an SSH client (such as TeraTerm or PuTTY) on the PC/laptop. | The SSH client should be installed and ready for use on the PC/laptop.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 |  Select WiFi interface  | Select "WiFi" on the Network Configuration screen. | The Wi-Fi network selection screen should be displayed, listing all available SSIDs (both 2.4 GHz and 5 GHz bands).|
| 2 |  Select available SSID  | Select any available SSID from the list. | The password entry screen should launch with an on-screen keyboard and Connect/Cancel buttons.|
| 3 |  Enter wrong password and connect  | Enter an incorrect password using the on-screen keyboard and press the Connect button. | The Wi-Fi network selection screen should be displayed with a clear CONNECTION_FAILED error message explicitly indicating that the failure was due to incorrect credentials.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
