## TestCase ID
RDKV_MANUAL_IPV6_08
## TestCase Name
RDKV_CERT_MANUAL_IPv6_Eth_Iface_IPv6_Not_Returned

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the DUT correctly handles IPv6 address queries per network interface when only the Wi-Fi interface has a global IPv6 address and Ethernet does not. This test confirms that interface-specific IP queries return accurate, isolated results without cross-reporting from other interfaces, ensuring correct IPv6 address resolution behavior meets certification requirements.

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
| 1 | Query public IPv6 address for eth0 interface | Execute the following curl command to query the public IPv6 address specifically for the Ethernet (eth0) interface.<br>Command: `curl -d '{ "jsonrpc": "2.0", "id": 42, "method": "org.rdk.NetworkManager.1.GetPublicIP", "params": {"interface": "eth0", "ipversion": "IPv6" } }' http://127.0.0.1:9998/jsonrpc` | The API response should return `"success":false` or an empty `publicIP` field, confirming that no global IPv6 address is available on the eth0 interface. The wlan0 IPv6 address should not be returned when eth0 is explicitly queried.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
