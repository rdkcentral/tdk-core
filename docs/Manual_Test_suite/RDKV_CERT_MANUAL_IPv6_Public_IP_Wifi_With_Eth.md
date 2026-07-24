## TestCase ID
RDKV_MANUAL_IPV6_02
## TestCase Name
RDKV_CERT_MANUAL_IPv6_Public_IP_Wifi_With_Eth

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the DUT returns the correct public IPv6 address via the Ethernet interface when both an IPv6-supporting Wi-Fi SSID and Ethernet are connected. This test confirms that the returned IPv6 address is associated with the Ethernet interface in a dual-connection configuration, ensuring IPv6 public IP retrieval with both interfaces active meets certification requirements.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Connect HDMI display | Connect the HDMI display to the DUT and select the correct HDMI input source on the display. | The HDMI display should be connected and the correct HDMI input source should be selected on the display.|
| 2 | Connect DUT to IPv6-supporting Wi-Fi SSID | Connect the DUT to a Wi-Fi SSID that supports IPv6 prior to the test. | The DUT should be connected to an IPv6-supporting Wi-Fi SSID with a valid IPv6 address assigned.|
| 3 | Connect Ethernet cable to DUT | Connect the Ethernet cable to the DUT and ensure it remains connected throughout the test. | The Ethernet cable should be connected to the DUT throughout the test.|
| 4 | Ensure SSH or console access | Ensure that SSH access or serial console access to the DUT is available from the PC/laptop. | SSH or serial console access should be available and functional on the DUT.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Query public IPv6 address via API | Execute the following curl command to retrieve the public IPv6 IP address.<br>Command: `curl -d '{ "jsonrpc": "2.0", "id": 42, "method": "org.rdk.NetworkManager.1.GetPublicIP", "params": { "ipversion": "IPv6" } }' http://127.0.0.1:9998/jsonrpc` | The public IPv6 address should be returned via the Ethernet interface. The API response should return `"success":true` with a valid public IPv6 address in the `publicIP` field. The `interface` field should be `eth0` since Ethernet is connected.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
