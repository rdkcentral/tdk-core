## TestCase ID
RDKV_MANUAL_IPV6_07
## TestCase Name
RDKV_CERT_MANUAL_IPv6_Ping_Api_Wifi_No_Eth

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that IPv6 ping functionality is operational on the DUT when connected to an IPv6-supporting Wi-Fi SSID with Ethernet disconnected. This test confirms that ping packets are successfully transmitted and received over the IPv6 Wi-Fi connection with no packet loss, ensuring IPv6 ping capability meets certification requirements.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Connect HDMI display | Connect the HDMI display to the DUT and select the correct HDMI input source on the display. | The HDMI display should be connected and the correct HDMI input source should be selected on the display.|
| 2 | Connect DUT to IPv6-supporting Wi-Fi SSID | Connect the DUT to a Wi-Fi SSID that supports IPv6 prior to the test. | The DUT should be connected to an IPv6-supporting Wi-Fi SSID with a valid IPv6 address assigned.|
| 3 | Disconnect Ethernet cable from DUT | Disconnect the Ethernet cable from the DUT after connecting to the Wi-Fi SSID. | The Ethernet cable should be disconnected from the DUT.|
| 4 | Ensure SSH or console access | Ensure that SSH access or serial console access to the DUT is available from the PC/laptop. | SSH or serial console access should be available and functional on the DUT.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Ping Google DNS IPv6 endpoint | Execute the following curl command to ping the Google DNS IPv6 endpoint with 3 packets.<br>Command: `curl -d '{ "jsonrpc": "2.0", "id": 42, "method": "org.rdk.NetworkManager.1.Ping", "params": { "endpoint": "2001:4860:4860::8888", "ipversion": "IPv6", "packets": 3 } }' http://127.0.0.1:9998/jsonrpc` | The Ping API should return a successful response. All 3 packets should be transmitted and received with zero packet loss, and valid round-trip time statistics (minimum, maximum, average, and standard deviation) should be present in the response.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
