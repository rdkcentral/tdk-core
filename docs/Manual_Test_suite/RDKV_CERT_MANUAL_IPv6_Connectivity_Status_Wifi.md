## TestCase ID
RDKV_MANUAL_IPV6_01
## TestCase Name
RDKV_CERT_MANUAL_IPv6_Connectivity_Status_Wifi

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the DUT reports a fully connected IPv6 status when connected to a Wi-Fi SSID that supports IPv6. This test exercises the RDK network manager, IPv6 address assignment stack (`ip` / `ifconfig` commands), and the router Advertisement handler to validate dual-stack network connectivity. The test confirms that the response should confirm IPv6 connectivity. Expected response: {"jsonrpc":"2.0","id":42,"result":{"ipversion":"IPv6","interface":"wlan0","connected":true,"state":3,"status":"FULLY_CONNECTED","success":true}}.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Connect HDMI display | Connect the HDMI display to the DUT and select the correct HDMI input source on the display. | The HDMI display should be connected and the correct HDMI input source should be selected on the display. |
| 2 | Connect DUT to IPv6-supporting Wi-Fi SSID | Connect the DUT to a Wi-Fi SSID that supports IPv6 prior to the test. | The DUT should be connected to an IPv6-supporting Wi-Fi SSID with a valid IPv6 address assigned. |
| 3 | Ensure SSH or console access | Ensure that SSH access or serial console access to the DUT is available from the PC/laptop. | SSH or serial console access should be available and functional on the DUT. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Query IPv6 internet connectivity status | Execute the following curl command in the DUT SSH terminal or serial console to query the IPv6 internet connectivity status.<br>Command: `curl -d '{ "jsonrpc": "2.0", "id": 42, "method": "org.rdk.NetworkManager.1.IsConnectedToInternet", "params": { "ipversion": "IPv6" } }' http://127.0.0.1:9998/jsonrpc` | The response should confirm IPv6 connectivity. Expected response: {"jsonrpc":"2.0","id":42,"result":{"ipversion":"IPv6","interface":"wlan0","connected":true,"state":3,"status":"FULLY_CONNECTED","success":true}} |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
