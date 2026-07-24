## TestCase ID
RDKV_MANUAL_IPV6_06
## TestCase Name
RDKV_CERT_MANUAL_IPv6_Trace_Api_Wifi_No_Eth

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that IPv6 traceroute functionality is operational on the DUT when connected to an IPv6-supporting Wi-Fi SSID with Ethernet disconnected. This test confirms that the traceroute completes successfully with a valid hop path to the destination, ensuring IPv6 trace capability meets certification requirements.

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
| 1 | Perform IPv6 traceroute to Google DNS | Execute the following curl command to perform an IPv6 traceroute to the Google DNS endpoint.<br>Command: `curl -d '{ "jsonrpc": "2.0", "id": 42, "method": "org.rdk.NetworkManager.1.Trace", "params": { "endpoint": "2001:4860:4860::8888", "ipversion": "IPv6", "packets": 3 } }' http://127.0.0.1:9998/jsonrpc` | The traceroute should complete successfully. The response should contain "success":true and a results array listing the hop information to the destination 2001:4860:4860::8888.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
