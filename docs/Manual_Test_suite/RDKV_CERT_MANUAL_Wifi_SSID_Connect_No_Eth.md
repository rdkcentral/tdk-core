## TestCase ID
RDKV_MANUAL_WIFI_08
## TestCase Name
RDKV_CERT_MANUAL_Wifi_SSID_Connect_No_Eth

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the DUT can successfully connect to a new Wi-Fi SSID when no Ethernet cable is connected. This test exercises the RDK UI Network Configuration settings, the Wi-Fi connection manager (`wpa_supplicant`), and the network interface stack to validate the targeted Wi-Fi connectivity behaviour. The test confirms that the application should open successfully and content playback should start with proper audio and video output.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Connect HDMI display | Connect the HDMI display to the DUT and select the correct HDMI input source on the display. | The HDMI display should be connected and the correct HDMI input source should be selected on the display.|
| 2 | Confirm no Wi-Fi connection | Ensure the DUT is not connected to any Wi-Fi network prior to the test. | The DUT should not be connected to any Wi-Fi network prior to the test.|
| 3 | Disconnect Ethernet cable | Disconnect the Ethernet cable from the DUT. | The Ethernet cable should be disconnected from the DUT.|
| 4 | Pair Bluetooth remote | Pair and connect the Bluetooth remote to the DUT. | The Bluetooth remote should be paired and connected to the DUT successfully.|
| 5 | Connect serial cable | Connect the required serial cable or USB-to-serial adapter between the DUT and the PC/laptop and ensure the appropriate drivers are installed. | The serial cable or USB-to-serial adapter should be connected and the drivers should be installed and recognized.|
| 6 | Configure serial terminal | Install and configure a serial terminal utility (such as Minicom, TeraTerm, or equivalent) on the PC/laptop. | The serial terminal utility should be installed, properly configured, and ready to connect to the DUT.|
| 7 | Install SSH client | Install an SSH client (such as TeraTerm or PuTTY) on the PC/laptop. | The SSH client should be installed and ready for use on the PC/laptop.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Open network configuration | Navigate to Settings > Network Configuration from the RDK UI Home screen. | The Network Configuration screen should load with the Network Interface value displayed as WiFi.|
| 2 | Open network info | Select "Network Info" and press OK. | The Network Info screen should load with Status displayed as "Disconnected" and all other fields as N/A.|
| 3 | Navigate to network interface | Press Back, navigate to "Network Interface", and press OK. | The Network Interface selection screen should launch listing WiFi and Ethernet as options.|
| 4 | Select WiFi interface | Select "WiFi". | The Wi-Fi network selection screen should load with the Wi-Fi On/Off toggle in the ON state. All available SSIDs (both 2.4 GHz and 5 GHz) should be listed.|
| 5 | Select SSID and connect | Select any available SSID, enter the correct password using the on-screen keyboard, and press Connect. | The DUT should connect to the selected SSID. The Wi-Fi network selection screen should reload with the connected SSID in a ticked state.|
| 6 | Navigate back to settings | Press the Back button twice. | The Network Configuration screen should load with the Network Interface value as WiFi.|
| 7 | Verify network info | Navigate to "Network Info" and press OK. | The Network Info screen should load displaying the Wi-Fi IP address and SSID details with all fields correctly populated.|
| 8 | Verify internet status | Press Back, navigate to "Test Internet Status", and press OK. | The connection status should be displayed as "Connected" (provided internet access is available).|
| 9 | SSH via wlan0 IP | SSH to the DUT using the wlan0 IP address obtained in Step 7. | The SSH connection should be established successfully.|
| 10 | Verify internet via ping | In the SSH console, execute the ping command.<br>Command: `ping google.com` | Ping packets should be transmitted and received successfully.|
| 11 | Launch app and play content | On the RDK UI Home screen, open any application that requires internet and play any content. | The application should open successfully and content playback should start with proper audio and video output.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
