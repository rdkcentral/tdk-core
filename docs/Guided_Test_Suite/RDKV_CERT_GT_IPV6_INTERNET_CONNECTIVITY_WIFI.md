## TestCase ID
RDKV_MANUAL_IPV6_01
## TestCase Name
RDKV_CERT_GT_IPV6_INTERNET_CONNECTIVITY_WIFI

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the DUT has IPv6 internet connectivity via the WiFi interface when connected to an IPv6-supported SSID with Ethernet disconnected.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Connect HDMI display to DUT | Connect an HDMI display/TV to the DUT and ensure the correct HDMI input source is selected on the display. | The HDMI display/TV should be connected to the DUT and the RDK UI should be visible on the screen. |
| 2 | Connect DUT to IPv6 WiFi SSID | Connect the DUT to an IPv6-supported WiFi SSID configured as `<ipv6_conf_SSID>`. | The DUT should be connected to the configured IPv6-supported WiFi SSID and a valid IPv6 address should be assigned to the wlan0 interface. |
| 3 | Disconnect Ethernet cable | Disconnect the Ethernet cable from the DUT to ensure only WiFi connectivity is active. | The Ethernet interface (eth0) should have no IPv4 address assigned on the DUT. |
| 4 | Verify IPv6 SSID connection | Verify the DUT is connected to the correct IPv6 SSID using the NetworkManager API.<br>Command: `curl -d '{"jsonrpc":"2.0","id":42,"method":"org.rdk.NetworkManager.1.GetConnectedSSID"}' http://127.0.0.1:9998/jsonrpc` | The DUT should be connected to `<ipv6_conf_SSID>` and a valid IPv6 address should be present on the wlan0 interface with Ethernet disconnected. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify IPv6 internet connectivity via WiFi | Execute the curl command to verify IPv6 internet connectivity via the WiFi interface (wlan0).<br>Command: `curl -d '{"jsonrpc":"2.0","id":42,"method":"org.rdk.NetworkManager.1.IsConnectedToInternet","params":{"ipversion":"IPv6"}}' http://127.0.0.1:9998/jsonrpc` | The API response should return interface=wlan0, connected=true, and status=FULLY_CONNECTED, confirming IPv6 internet connectivity via WiFi. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
