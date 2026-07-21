## TestCase ID
RDKV_MANUAL_WIFI_09
## TestCase Name
RDKV_CERT_MANUAL_Wifi_SSID_Persist_After_Reboot

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the DUT retains its Wi-Fi SSID connection and IP address after a reboot when no Ethernet cable is connected. This test confirms that the DUT automatically reconnects to the Wi-Fi SSID after reboot and content playback is functional, ensuring Wi-Fi connection persistence across reboots meets certification requirements.
<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Connect HDMI display | Connect the HDMI display to the DUT and select the correct HDMI input source on the display. | The HDMI display should be connected and the correct HDMI input source should be selected on the display.|
| 2 | Disconnect Ethernet cable | Disconnect the Ethernet cable from the DUT. | The Ethernet cable should be disconnected from the DUT.|
| 3 | Confirm Wi-Fi with valid IP | Ensure the DUT is already connected to a Wi-Fi network with a valid IP address prior to the test. | The DUT should be connected to a Wi-Fi network with a valid IP address.|
| 4 | Confirm internet access | Confirm that internet access is functional on the DUT prior to the test. | Internet access should be confirmed as functional on the DUT.|
| 5 | Pair Bluetooth remote | Pair and connect the Bluetooth remote to the DUT. | The Bluetooth remote should be paired and connected to the DUT successfully.|
| 6 | Connect serial cable | Connect the required serial cable or USB-to-serial adapter between the DUT and the PC/laptop and ensure the appropriate drivers are installed. | The serial cable or USB-to-serial adapter should be connected and the drivers should be installed and recognized.|
| 7 | Configure serial terminal | Install and configure a serial terminal utility (such as Minicom, TeraTerm, or equivalent) on the PC/laptop. | The serial terminal utility should be installed, properly configured, and ready to connect to the DUT.|
| 8 | Install SSH client | Install an SSH client (such as TeraTerm or PuTTY) on the PC/laptop. | The SSH client should be installed and ready for use on the PC/laptop.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot DUT | Reboot the DUT. | The DUT should reboot successfully and the RDK UI Home screen should be displayed.|
| 2 | Verify network info after reboot | Navigate to Settings > Network Configuration > Network Info and verify the details. | The SSID, IP address, and all other details of the previously connected Wi-Fi network should be populated correctly.|
| 3 | SSH via wlan0 IP | SSH to the DUT using the wlan0 IP address. | The SSH connection should be established successfully using the wlan0 IP address.|
| 4 | Verify internet via ping | In the SSH console, execute the ping command.<br>Command: `ping google.com` | Ping packets should be transmitted and received successfully, confirming internet connectivity is maintained after reboot.|
| 5 | Launch app and play content | On the RDK UI Home screen, open any application that requires internet and play any content. | The application should open successfully and content playback should start with proper audio and video output.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
