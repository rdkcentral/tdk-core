## TestCase ID
RDKV_MANUAL_IPV6_05
## TestCase Name
RDKV_CERT_MANUAL_IPv6_Internet_Access_Wifi_No_Eth

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that internet access is functional on the DUT when connected to an IPv6-supporting Wi-Fi SSID with Ethernet disconnected. This test exercises the RDK network manager, IPv6 address assignment stack (`ip` / `ifconfig` commands), and the router Advertisement handler to validate dual-stack network connectivity. The test confirms that the selected video content A/V playback should start successfully, confirming internet access is functional via IPv6 over Wi-Fi.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Connect HDMI display | Connect the HDMI display to the DUT and select the correct HDMI input source on the display. | The HDMI display should be connected and the correct HDMI input source should be selected on the display.|
| 2 | Connect DUT to IPv6-supporting Wi-Fi SSID | Connect the DUT to a Wi-Fi SSID that supports IPv6 prior to the test. | The DUT should be connected to an IPv6-supporting Wi-Fi SSID with a valid IPv6 address assigned.|
| 3 | Disconnect Ethernet cable from DUT | Disconnect the Ethernet cable from the DUT after connecting to the Wi-Fi SSID. | The Ethernet cable should be disconnected from the DUT.|
| 4 | Pair Bluetooth remote | Pair and connect the Bluetooth remote to the DUT. | The Bluetooth remote should be paired and connected to the DUT successfully.|
| 5 | Ensure SSH or console access | Ensure that SSH access or serial console access to the DUT is available from the PC/laptop. | SSH or serial console access should be available and functional on the DUT.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Query IPv6 internet connectivity status | Execute the following curl command in the DUT SSH terminal or serial console to query the IPv6 internet connectivity status.<br>Command: `curl -d '{ "jsonrpc": "2.0", "id": 42, "method": "org.rdk.NetworkManager.1.IsConnectedToInternet", "params": { "ipversion": "IPv6" } }' http://127.0.0.1:9998/jsonrpc` | The response should confirm IPv6 connectivity via the Wi-Fi interface.|
| 2 | Launch YouTube app | Select the YouTube application tile (or any other application that requires internet) from the My Apps / Recommended Apps section and press Enter/OK on the remote. | The YouTube application should launch successfully (cold launch or hot launch based on the app's previous state).|
| 3 | Select video and initiate YouTube playback | Select any video content from the YouTube application and initiate playback. | The selected video content A/V playback should start successfully, confirming internet access is functional via IPv6 over Wi-Fi.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
