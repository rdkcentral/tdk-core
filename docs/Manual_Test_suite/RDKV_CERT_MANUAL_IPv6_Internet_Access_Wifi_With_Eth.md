## TestCase ID
RDKV_MANUAL_IPV6_04
## TestCase Name
RDKV_CERT_MANUAL_IPv6_Internet_Access_Wifi_With_Eth

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that internet access is functional on the DUT when connected to an IPv6-supporting Wi-Fi SSID with Ethernet also connected. This test confirms that A/V content playback starts successfully in a dual-interface configuration, ensuring IPv6 internet access is functional for certification.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Connect HDMI display | Connect the HDMI display to the DUT and select the correct HDMI input source on the display. | The HDMI display should be connected and the correct HDMI input source should be selected on the display.|
| 2 | Connect DUT to IPv6-supporting Wi-Fi SSID | Connect the DUT to a Wi-Fi SSID that supports IPv6 prior to the test. | The DUT should be connected to an IPv6-supporting Wi-Fi SSID with a valid IPv6 address assigned.|
| 3 | Connect Ethernet cable to DUT | Connect the Ethernet cable to the DUT and ensure it remains connected throughout the test. | The Ethernet cable should be connected to the DUT throughout the test.|
| 4 | Pair Bluetooth remote | Pair and connect the Bluetooth remote to the DUT. | The Bluetooth remote should be paired and connected to the DUT successfully.|
| 5 | Ensure SSH or console access | Ensure that SSH access or serial console access to the DUT is available from the PC/laptop. | SSH or serial console access should be available and functional on the DUT.|
| 6 | Install required application | Navigate to the Recommended Apps row on the RDK UI Home screen (or the More Apps tab if the required application is not visible), select the required application tile, and press Enter/OK on the remote. Verify that a buffering/loading indicator appears on the tile. On successful installation, a green tick icon should appear on the tile for approximately 2 seconds. | The required application should be installed successfully on the DUT.|
| 7 | Verify app listed on home screen | Verify that the installed application is listed under the My Apps section/row and on the App Info page of the RDK UI Home screen, confirming it is ready to launch. | The installed application should be visible in the My Apps section and ready to launch.|
| 8 | Sign in to premium application | If the installed application is a premium application (such as YouTube or Amazon Prime), sign in with valid user credentials and verify A/V playback is functional prior to test execution. | Sign-in should succeed and A/V playback should be functional.|
| 9 | Verify app launch and content access | Verify that all installed applications launch correctly from the RDK UI, and that any purchased content and premium features are accessible prior to test execution. | All installed applications should launch correctly and content should be accessible.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Query IPv6 internet connectivity status | Execute the following curl command in the DUT SSH terminal or serial console to query the IPv6 internet connectivity status.<br>Command: `curl -d '{ "jsonrpc": "2.0", "id": 42, "method": "org.rdk.NetworkManager.1.IsConnectedToInternet", "params": { "ipversion": "IPv6" } }' http://127.0.0.1:9998/jsonrpc` | The response should confirm IPv6 connectivity via the Ethernet interface.|
| 2 | Launch YouTube app | Select the YouTube application tile (or any other application that requires internet) from the My Apps / Recommended Apps section and press Enter/OK on the remote. | The YouTube application should launch successfully (cold launch or hot launch based on the app's previous state).|
| 3 | Select video and initiate YouTube playback | Select any video content from the YouTube application and initiate playback. | The selected video content A/V playback should start successfully, confirming internet access is functional via IPv6.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
